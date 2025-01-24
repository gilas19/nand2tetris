"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing


class VMWriter:
    """
    Writes VM commands into a file. Encapsulates the VM command syntax.
    """

    def __init__(self, output_stream: typing.TextIO) -> None:
        """Creates a new file and prepares it for writing VM commands."""
        self.output_stream = output_stream

    def __handle_segment(self, segment: str) -> str:
        """Handles the segment name to match the VM syntax.

        Args:
            segment (str): the segment to handle.

        Returns:
            str: the handled segment.
        """
        if segment == "CONST":
            segment = "constant"
        elif segment == "ARG":
            segment = "argument"
        elif segment == "VAR":
            segment = "local"
        elif segment == "FIELD":
            segment = "this"
        else:
            segment = segment.lower()
        return segment

    def write_push(self, segment: str, index: int) -> None:
        """Writes a VM push command.

        Args:
            segment (str): the segment to push to, can be "CONST", "ARG",
            "LOCAL", "STATIC", "THIS", "THAT", "POINTER", "TEMP"
            index (int): the index to push to.
        """
        self.output_stream.write(f"push {self.__handle_segment(segment)} {index}\n")

    def write_pop(self, segment: str, index: int) -> None:
        """Writes a VM pop command.

        Args:
            segment (str): the segment to pop from, can be "CONST", "ARG",
            "LOCAL", "STATIC", "THIS", "THAT", "POINTER", "TEMP".
            index (int): the index to pop from.
        """
        self.output_stream.write(f"pop {self.__handle_segment(segment)} {index}\n")

    def write_arithmetic(self, command: str) -> None:
        """Writes a VM arithmetic command.

        Args:
            command (str): the command to write, can be "ADD", "SUB", "NEG",
            "EQ", "GT", "LT", "AND", "OR", "NOT", "SHIFTLEFT", "SHIFTRIGHT".
        """
        self.output_stream.write(f"{command.lower()}\n")

    def write_label(self, label: str) -> None:
        """Writes a VM label command.

        Args:
            label (str): the label to write.
        """
        self.output_stream.write(f"label {label}\n")

    def write_goto(self, label: str) -> None:
        """Writes a VM goto command.

        Args:
            label (str): the label to go to.
        """
        self.output_stream.write(f"goto {label}\n")

    def write_if(self, label: str) -> None:
        """Writes a VM if-goto command.

        Args:
            label (str): the label to go to.
        """
        self.output_stream.write(f"if-goto {label}\n")

    def write_call(self, name: str, n_args: int) -> None:
        """Writes a VM call command.

        Args:
            name (str): the name of the function to call.
            n_args (int): the number of arguments the function receives.
        """
        self.output_stream.write(f"call {name} {n_args}\n")

    def write_function(self, name: str, n_locals: int) -> None:
        """Writes a VM function command.

        Args:
            name (str): the name of the function.
            n_locals (int): the number of local variables the function uses.
        """
        self.output_stream.write(f"function {name} {n_locals}\n")

    def write_return(self) -> None:
        """Writes a VM return command."""
        self.output_stream.write("return\n")

    def comment(self, comment: str) -> None:
        """Writes a comment into the output file.

        Args:
            comment (str): the comment to write.
        """
        self.output_stream.write(f"// {comment}\n")