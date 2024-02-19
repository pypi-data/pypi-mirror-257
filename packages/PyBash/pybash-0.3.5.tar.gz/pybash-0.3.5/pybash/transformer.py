import re
import shlex
from typing import Callable, Union

import token_utils


class InvalidInterpolation(Exception):
    pass


class Processor:
    command_char = "$"

    def __init__(self, token: token_utils.Token) -> None:
        self.token = token
        self.token_line = token.line
        self.parse()

    def parse(self) -> None:
        self.parsed_line = shlex.split(self.token_line)
        self.command = Commander.get_bash_command(self.parsed_line, command_char=self.command_char)

    def transform(self) -> token_utils.Token:
        raise NotImplementedError

    def interpolate(self) -> None:
        self.token.string = Processor.fstring_interpolate(self.token_line, self.token.string)
        self.token.string = Processor.direct_interpolate(self.token.string)

    @staticmethod
    def fstring_interpolate(token_string: str, parsed_command: str) -> str:
        """Process f{ dynamic interpolations } and substitute.
            Dynamic interpolations are denotated by a f{ } with any expression inside.
            Substitution in the parsed command string happens relative to the order of the
            interpolations in the original command string.

        Args:
            token_string (str): Original command string
            parsed_command (str): Parsed command string

        Returns:
            str: Interpolated parsed command string
        """
        pattern = r'f{(.+?)}'
        subs = re.findall(pattern, token_string)

        if not subs:
            return parsed_command

        for sub in subs:
            parsed_command = re.sub(pattern, '" + f\"\"\"{' + sub + '}\"\"\" + "', parsed_command, 1)

        return parsed_command.replace('"" + f"""', 'f"""').replace('""" + ""', '"""')

    @staticmethod
    def direct_interpolate(token_string: str) -> str:
        """Process {{ static interpolations }} and substitute.
            Static interpolations are denotated by a {{ }} with a variable or a function call inside.
            Substitution happens directly on the parsed command string. Therefore, certain characters
            cannot be interpolated as they get parsed out before substitution.

        Args:
            string (str): String to interpolate

        Returns:
            str: Interpolated or given token string
        """

        # validate interpolation
        invalid_chars = [' ', '"', "'"]
        matches = re.findall(r'{{(.+?)}}', token_string)
        if not matches:
            return token_string

        if any(any(bad_char in match for bad_char in invalid_chars) for match in matches):
            raise InvalidInterpolation

        interpolated = re.sub(r'{{(.+?)}}', r'" + \1 + "', token_string)
        return interpolated.replace(',"" + ', ',').replace(' + ""', '')


class Shelled(Processor):
    # >ls .github/*
    command_char = ">"

    def transform(self) -> token_utils.Token:
        command_str = " ".join(self.command)
        self.token.string = Commander.build_subprocess_str_cmd("run", command_str, shell=True) + '\n'
        return self.token


class Execed(Processor):
    # $ls -la
    def transform(self) -> token_utils.Token:
        pipeline_command = Pipeline(self.command).parse_command()
        if pipeline_command != self.command:
            self.token.string = pipeline_command + '\n'
        else:
            # no pipers
            self.token.string = Commander.build_subprocess_list_cmd("run", self.command) + '\n'
        return self.token


class Variablized(Processor):
    # a = $cat test.txt
    def parse(self) -> None:
        self.parsed_line = shlex.split(self.token.line)
        self.start_index = Commander.get_start_index(self.parsed_line)
        self.command = Commander.get_bash_command(self.parsed_line, start_index=self.start_index)

    def transform(self) -> None:
        pipeline_command = Pipeline(self.command).parse_command(variablized=True)

        if pipeline_command != self.command:
            self.token.string = pipeline_command
            self.token.string += ';' if pipeline_command[-1] != ';' else ''
            self.token.string += ' '.join(self.parsed_line[: self.start_index]) + ' cmd1\n'
        else:
            self.token.string = ' '.join(self.parsed_line[: self.start_index]) + ' '
            self.token.string += Commander.build_subprocess_list_cmd("check_output", self.command) + '\n'


class Wrapped(Processor):
    # print($cat test.txt)
    def parse(self) -> None:
        self.parsed_line = shlex.split(self.token.line)
        self.raw_line = [tok for tok in self.token.line.split(' ') if tok]
        self.start_index = Commander.get_start_index(self.parsed_line)
        self.command = Commander.get_bash_command(self.parsed_line, start_index=self.start_index, wrapped=True)

    def transform(self) -> token_utils.Token:
        # shlex strips out single quotes and double quotes-- use raw_line for the code around the wrapped command
        self.token.string = (
            ' '.join(self.raw_line[: self.start_index])
            + self.raw_line[self.start_index][: self.raw_line[self.start_index].index('$')]
        )
        self.token.string += (
            Commander.build_subprocess_list_cmd("check_output", self.command)
            + self.raw_line[-1][self.raw_line[-1].index(')') :]
            + '\n'
        )

        return self.token


class Pipers:
    """Handles the logic of chaining operators"""

    OPS = ['|', '>', '>>', '<', '&&']

    @classmethod
    def get_piper(cls, op: str) -> Callable:
        if op == '|':
            # Pipe output to next command
            return cls.chain_pipe_command
        elif op == '>':
            # Write to out file
            return cls.chain_sredirect_command
        elif op == '>>':
            # Append to out file
            return cls.chain_dredirect_command
        elif op == '<':
            # Redirect file as input to command
            return cls.chain_iredirect_command
        elif op == '&&':
            # Run next command only if previous succeeds
            return cls.chain_and_command

        raise NotImplementedError

    @classmethod
    def chain_iredirect_command(
        cls, command: list, pipeline: list, start_index: int = 0, fmode: str = "r", fvar: str = "fout", **kwargs
    ) -> str:
        first_idx, _ = pipeline.pop(0)
        pre_command = command[start_index:first_idx]
        filename = command[first_idx + 1 : first_idx + 2][0]

        fout = f'open("{filename}", "{fmode}")'

        if not pipeline:
            # out to file
            cmd1 = Commander.build_subprocess_list_cmd("run", pre_command, stdin=fvar, **kwargs)
            return f"{fvar} = {fout}; cmd1 = {cmd1}"

        cmd1 = Commander.build_subprocess_list_cmd("Popen", pre_command, stdin=fvar, stdout="subprocess.PIPE", **kwargs)

        out = f"{fvar} = {fout}; cmd1 = {cmd1};"
        while pipeline:
            idx, piper = pipeline[0]
            fvar = f"fout{idx}"
            cmd = ""
            if piper == '>':
                # $sort < test.txt > test2.txt
                cmd = cls.write_to_file(
                    command, pipeline, reader='cmd1.stdout.read()', start_index=first_idx + 1, fmode="wb"
                )
            elif piper == '>>':
                # $sort < test.txt >> test2.txt
                cmd = cls.write_to_file(
                    command, pipeline, reader='cmd1.stdout.read()', start_index=first_idx + 1, fmode="ab"
                )
            elif piper == '|':
                # $sort < test.txt | grep "HELLO"
                cmd = cls.get_piper(piper)(
                    command, pipeline, start_index=first_idx + 1, stdin="cmd1.stdout", chained=True
                )
            out += cmd
            first_idx = idx

        return out

    @classmethod
    def write_to_file(
        cls, command: list, pipeline: list, reader: str, start_index: int = 0, fvar: str = 'fout', fmode: str = 'wb'
    ) -> str:
        first_idx, _ = pipeline.pop(0)
        filename = command[first_idx + 1 : first_idx + 2][0]
        return f'{fvar} = open("{filename}", "{fmode}"); {fvar}.write({reader});'

    @classmethod
    def chain_and_command(cls, command: list, pipeline: list, **kwargs):
        raise NotImplementedError

    @classmethod
    def chain_pipe_command(
        cls, command: list, pipeline: list, start_index: int = 0, chained: bool = False, **kwargs
    ) -> str:
        first_idx, _ = pipeline.pop(0)
        pre_command = command[start_index:first_idx]
        cmd1 = (
            ""
            if chained
            else Commander.build_subprocess_list_cmd('Popen', pre_command, stdout='subprocess.PIPE', **kwargs)
        )
        cmd2 = ""
        if not pipeline:
            ## No other pipes
            post_command = command[first_idx + 1 :]

            cmd2 = Commander.build_subprocess_list_cmd('run', post_command, stdin='cmd1.stdout')

            return f"cmd2 = {cmd2}" if chained else f"cmd1 = {cmd1}; cmd2 = {cmd2}"
        out = "" if chained else f"cmd1 = {cmd1};"
        while pipeline:
            idx, piper = pipeline[0]
            cmd = cls.get_piper(piper)(command, pipeline, start_index=first_idx + 1, stdin="cmd1.stdout")
            out += cmd
            first_idx = idx

        return out

    @classmethod
    def chain_redirect(
        cls,
        command: list,
        pipeline: list,
        start_index: int = 0,
        fvar: str = "fout",
        fmode: str = "wb",
        chained: bool = False,
        **kwargs,
    ) -> str:
        first_idx, _ = pipeline.pop(0)
        pre_command = command[start_index:first_idx]
        filename = command[first_idx + 1 : first_idx + 2][0]

        if chained:
            # file-to-file redirection so cat from source file
            pre_command.insert(0, 'cat')

        # out to file
        fout = f'open("{filename}", "{fmode}")'
        cmd1 = Commander.build_subprocess_list_cmd("run", pre_command, stdout=fvar, **kwargs)

        if not pipeline:
            return f"{fvar} = {fout}; cmd1 = {cmd1}"

        out = f"{fvar} = {fout}; cmd1 = {cmd1};"
        while pipeline:
            idx, piper = pipeline[0]
            fvar = f"fout{idx}"
            if piper in ['>', '>>']:
                cmd = cls.get_piper(piper)(command, pipeline, start_index=first_idx + 1, fvar=fvar, chained=True)
            else:
                cmd = cls.get_piper(piper)(command, pipeline, start_index=first_idx + 1, stdin=fvar)
            out += cmd
            first_idx = idx

        return out

    @classmethod
    def chain_sredirect_command(
        cls, command: list, pipeline: list, start_index: int = 0, fvar: str = "fout", chained: bool = False, **kwargs
    ) -> str:
        return cls.chain_redirect(command, pipeline, start_index, fmode="wb", fvar=fvar, chained=chained, **kwargs)

    @classmethod
    def chain_dredirect_command(
        cls, command: list, pipeline: list, start_index: int = 0, fvar: str = "fout", chained: bool = False, **kwargs
    ) -> str:
        return cls.chain_redirect(command, pipeline, start_index, fmode="ab", fvar=fvar, chained=chained, **kwargs)


class Pipeline:
    """Parses and transformers command chainings by generating pipers"""

    __slots__ = ['command', 'pipeline']

    def __init__(self, command: list[str]):
        self.command = command
        self.pipeline = [(i, arg) for i, arg in enumerate(self.command) if arg in Pipers.OPS]

    def parse_command(self, variablized: bool = False, **kwargs) -> Union[list[str], str]:
        if not self.pipeline:
            return self.command

        _, first_piper = self.pipeline[0]
        return Pipers.get_piper(first_piper)(self.command, self.pipeline, **kwargs)


class Commander:
    """Methods related to building and parsing commands"""

    @staticmethod
    def get_start_index(parsed_line: list) -> int:
        """Get the start index of first matching >

        Args:
            parsed_line (list): line to parse

        Returns:
            int: starting index
        """
        for i, val in enumerate(parsed_line):
            if '$' in val:
                return i

        return 0

    @staticmethod
    def get_bash_command(
        parsed_line: list,
        start_index: Union[int, None] = None,
        wrapped: Union[bool, None] = None,
        command_char: str = "$",
    ) -> list:
        """Parses line to bash command

        Args:
            parsed_line (list): line to parse
            start_index (int, optional): index to start parsing command from. Defaults to None.
            wrapped (bool, optional): input is surrounded by parentheses

        Returns:
            list: parsed command list
        """
        # find which arg index the $ is at
        if not start_index:
            start_index = Commander.get_start_index(parsed_line)

        # strip everything before that index-- not part of the command
        command = parsed_line[start_index:]

        # $ may be at the beginning or somewhere in the middle of this arg
        # examples: $ls, print(>cat => strip up to and including >
        command[0] = command[0][command[0].index(command_char) + 1 :].strip()
        if command[0] == '':
            del command[0]

        # remove everything after and including first )- not part of the command
        if wrapped:
            if ')' not in command[-1]:
                raise SyntaxError("Missing end parentheses")

            command[-1] = command[-1][: command[-1].index(')')]

        return command

    @staticmethod
    def build_subprocess_str_cmd(method: str, arg: str, **kwargs) -> str:
        """Builds subprocess command with string arg

        Args:
            method (str): subprocess method name
            arg (str): string arg

        Returns:
            str: subprocess command
        """
        command = f'subprocess.{method}("{arg}"'
        if kwargs:
            for k, v in kwargs.items():
                command += f", {k}={v}"
        command += ")"
        return command

    @staticmethod
    def build_subprocess_list_cmd(method: str, args: list, **kwargs) -> str:
        """Builds subprocess command with list args

        Args:
            method (str): subprocess method name
            args (list): list of args

        Returns:
            str: subprocess command
        """
        command = f'subprocess.{method}(['
        for arg in args:
            command += '\"' + arg + '\",'
        command = command[:-1]
        command += ']'
        if kwargs:
            for k, v in kwargs.items():
                command += f", {k}={v}"
        command += ")"
        return command


TOKENIZERS = {">": Shelled, "$": Execed}
GREEDY_TOKENIZERS = {"= $": Variablized, "($": Wrapped}


def transform(source, **_kwargs):
    """Convert >bash commands to subprocess calls"""
    new_tokens = []
    for line in token_utils.get_lines(source):
        token = token_utils.get_first(line)
        if not token:
            new_tokens.extend(line)
            continue

        if token_match := [tokenizer for match, tokenizer in TOKENIZERS.items() if token == match]:
            parser = token_match[0](token)
            parser.transform()
            parser.interpolate()
            new_tokens.append(parser.token)
            continue

        if greedy_match := [tokenizer for match, tokenizer in GREEDY_TOKENIZERS.items() if match in token.line]:
            parser = greedy_match[0](token)
            parser.transform()
            parser.interpolate()
            new_tokens.append(parser.token)
            continue

        # no match
        new_tokens.extend(line)

    return token_utils.untokenize(new_tokens)


if __name__ == "__main__":
    pyscript = transform("test = $ echo hi")
    print(pyscript)
