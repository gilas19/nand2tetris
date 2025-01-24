"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing
import os


class CodeWriter:
    """Translates VM commands into Hack assembly code."""

    DICT_COMMANDS = {'add': 'M=M+D', 'sub': 'M=M-D', 'and': 'M=M&D', 'or': 'M=M|D', 'neg': 'M=-M', 'not': 'M=!M', 'shiftleft': 'M=M<<', 'shiftright': 'M=M>>','eq': 'JEQ', 'gt': 'JGT', 'lt': 'JLT'}
    DICT_SEGMENT = {'local': 'LCL', 'argument': 'ARG', 'this': 'THIS', 'that': 'THAT', 'pointer': '3', 'temp': '5', 'static': '16'}

    def __init__(self, output_file: typing.TextIO) -> None:
        """Initializes the CodeWriter.

        Args:
            output_file (typing.TextIO): output stream.
        """
        self.output_file = output_file
        self.file_name = ''
        self.label_counter = 0
        self.curr_func = ''


    def set_file_name(self, filename: str) -> None:
        """Informs the code writer that the translation of a new VM file is 
        started.

        Args:
            filename (str): The name of the VM file.
        """
        self.file_name, extension = os.path.splitext(os.path.basename(filename))


    def write_arithmetic(self, command: str) -> None:
        """Writes assembly code that is the translation of the given 
        arithmetic command.

        Args:
            command (str): the arithmetic command to translate.
        """
        output = ['//'+command+'\n']
        if command in ['add', 'sub', 'and', 'or']:
            output.append('@SP\n')
            output.append('AM=M-1\n')
            output.append('D=M\n')
            output.append('A=A-1\n')
            output.append(self.DICT_COMMANDS[command]+'\n')
        elif command in ['neg', 'not']:
            output.append('@SP\n')
            output.append('A=M-1\n')
            output.append(self.DICT_COMMANDS[command]+'\n')
        elif command in ['eq', 'gt', 'lt']:
            output.append('@SP\n')
            output.append('AM=M-1\n')
            output.append('D=M\n')
            if command == 'eq':
                output.append('A=A-1\n')
                output.append('D=M-D\n')
            else:
                output.append('@POSITIVE'+str(self.label_counter)+'\n')
                output.append('D;JGT\n')
                output.append('@SP\n')
                output.append('A=M-1\n')
                output.append('D=M\n')
                output.append('@SPACIAL'+str(self.label_counter)+'\n')
                output.append('D;JGT\n')
                output.append('@CONTINUE'+str(self.label_counter)+'\n')
                output.append('0;JMP\n')
                output.append('(POSITIVE'+str(self.label_counter)+')\n')
                output.append('@SP\n')
                output.append('A=M-1\n')
                output.append('D=M\n')
                output.append('@SPACIAL'+str(self.label_counter)+'\n')
                output.append('D;JLT\n')
                output.append('(CONTINUE'+str(self.label_counter)+')\n')
                output.append('@SP\n')
                output.append('A=M\n')
                output.append('D=D-M\n')
                output.append('(SPACIAL'+str(self.label_counter)+')\n')
            output.append('@TRUE'+str(self.label_counter)+'\n')
            output.append('D;'+self.DICT_COMMANDS[command]+'\n')
            output.append('D=0\n')
            output.append('@FALSE'+str(self.label_counter)+'\n')
            output.append('0;JMP\n')
            output.append('(TRUE'+str(self.label_counter)+')\n')
            output.append('D=-1\n')
            output.append('(FALSE'+str(self.label_counter)+')\n')
            output.append('@SP\n')
            output.append('A=M-1\n')
            output.append('M=D\n')
            self.label_counter += 1
        elif command in ['shiftleft', 'shiftright']:
            output.append('@SP\n')
            output.append('A=M-1\n')
            output.append(self.DICT_COMMANDS[command]+'\n')
        self.output_file.writelines(output)


    def write_push_pop(self, command: str, segment: str, index: int) -> None:
        """Writes assembly code that is the translation of the given 
        command, where command is either C_PUSH or C_POP.

        Args:
            command (str): the command to translate.
            segment (str): the segment to push or pop.
            index (int): the index to push or pop.
        """
        output = ['//'+command+' '+segment+' '+str(index)+'\n']
        if command == 'C_PUSH':
            if segment == 'constant':
                output.append('@'+str(index)+'\n')
                output.append('D=A\n')
            elif segment == 'static':
                output.append('@'+self.file_name+'.'+str(index)+'\n')
                output.append('D=M\n')
            elif segment in ['local', 'argument', 'this', 'that']:
                output.append('@'+str(index)+'\n')
                output.append('D=A\n')
                output.append('@'+self.DICT_SEGMENT[segment]+'\n')
                output.append('A=D+M\n')
                output.append('D=M\n')
            elif segment in ['pointer', 'temp']:
                output.append('@'+str(index)+'\n')
                output.append('D=A\n')
                output.append('@'+self.DICT_SEGMENT[segment]+'\n')
                output.append('A=D+A\n')
                output.append('D=M\n')
            output.append('@SP\n')
            output.append('M=M+1\n')
            output.append('A=M-1\n')
            output.append('M=D\n')
        elif command == 'C_POP':
            if segment == 'static':
                output.append('@SP\n')
                output.append('AM=M-1\n')
                output.append('D=M\n')
                output.append('@'+self.file_name+'.'+str(index)+'\n')
            elif segment in ['local', 'argument', 'this', 'that']:
                output.append('@'+str(index)+'\n')
                output.append('D=A\n')
                output.append('@'+self.DICT_SEGMENT[segment]+'\n')
                output.append('D=D+M\n')
                output.append('@R13\n')
                output.append('M=D\n')
                output.append('@SP\n')
                output.append('AM=M-1\n')
                output.append('D=M\n')
                output.append('@R13\n')
                output.append('A=M\n')
            elif segment in ['pointer', 'temp']:
                output.append('@'+str(index)+'\n')
                output.append('D=A\n')
                output.append('@'+self.DICT_SEGMENT[segment]+'\n')
                output.append('D=D+A\n')
                output.append('@R13\n')
                output.append('M=D\n')
                output.append('@SP\n')
                output.append('AM=M-1\n')
                output.append('D=M\n')
                output.append('@R13\n')
                output.append('A=M\n')
            output.append('M=D\n')
        self.output_file.writelines(output)


    def write_label(self, label: str) -> None:
        """Writes assembly code that affects the label command. 
        Let "Xxx.foo" be a function within the file Xxx.vm. The handling of
        each "label bar" command within "Xxx.foo" generates and injects the symbol
        "Xxx.foo$bar" into the assembly code stream.
        When translating "goto bar" and "if-goto bar" commands within "foo",
        the label "Xxx.foo$bar" must be used instead of "bar".

        Args:
            label (str): the label to write.
        """
        # This is irrelevant for project 7,
        # you will implement this in project 8!
        pass
    
    def write_goto(self, label: str) -> None:
        """Writes assembly code that affects the goto command.

        Args:
            label (str): the label to go to.
        """
        # This is irrelevant for project 7,
        # you will implement this in project 8!
        pass
    
    def write_if(self, label: str) -> None:
        """Writes assembly code that affects the if-goto command. 

        Args:
            label (str): the label to go to.
        """
        # This is irrelevant for project 7,
        # you will implement this in project 8!
        pass
    
    def write_function(self, function_name: str, n_vars: int) -> None:
        """Writes assembly code that affects the function command. 
        The handling of each "function Xxx.foo" command within the file Xxx.vm
        generates and injects a symbol "Xxx.foo" into the assembly code stream,
        that labels the entry-point to the function's code.
        In the subsequent assembly process, the assembler translates this 
        symbol into the physical address where the function code starts.

        Args:
            function_name (str): the name of the function.
            n_vars (int): the number of local variables of the function.
        """
        # This is irrelevant for project 7,
        # you will implement this in project 8!
        # The pseudo-code of "function function_name n_vars" is:
        # (function_name)       // injects a function entry label into the code
        # repeat n_vars times:  // n_vars = number of local variables
        #   push constant 0     // initializes the local variables to 0
        pass
    
    def write_call(self, function_name: str, n_args: int) -> None:
        """Writes assembly code that affects the call command. 
        Let "Xxx.foo" be a function within the file Xxx.vm.
        The handling of each "call" command within Xxx.foo's code generates and
        injects a symbol "Xxx.foo$ret.i" into the assembly code stream, where
        "i" is a running integer (one such symbol is generated for each "call"
        command within "Xxx.foo").
        This symbol is used to mark the return address within the caller's 
        code. In the subsequent assembly process, the assembler translates this
        symbol into the physical memory address of the command immediately
        following the "call" command.

        Args:
            function_name (str): the name of the function to call.
            n_args (int): the number of arguments of the function.
        """
        # This is irrelevant for project 7,
        # you will implement this in project 8!
        # The pseudo-code of "call function_name n_args" is:
        # push return_address   // generates a label and pushes it to the stack
        # push LCL              // saves LCL of the caller
        # push ARG              // saves ARG of the caller
        # push THIS             // saves THIS of the caller
        # push THAT             // saves THAT of the caller
        # ARG = SP-5-n_args     // repositions ARG
        # LCL = SP              // repositions LCL
        # goto function_name    // transfers control to the callee
        # (return_address)      // injects the return address label into the code
        pass
    
    def write_return(self) -> None:
        """Writes assembly code that affects the return command."""
        # This is irrelevant for project 7,
        # you will implement this in project 8!
        # The pseudo-code of "return" is:
        # frame = LCL                   // frame is a temporary variable
        # return_address = *(frame-5)   // puts the return address in a temp var
        # *ARG = pop()                  // repositions the return value for the caller
        # SP = ARG + 1                  // repositions SP for the caller
        # THAT = *(frame-1)             // restores THAT for the caller
        # THIS = *(frame-2)             // restores THIS for the caller
        # ARG = *(frame-3)              // restores ARG for the caller
        # LCL = *(frame-4)              // restores LCL for the caller
        # goto return_address           // go to the return address
        pass