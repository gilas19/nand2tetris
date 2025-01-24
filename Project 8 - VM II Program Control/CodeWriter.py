"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing


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
        self.count_func = 0
        


    def set_file_name(self, filename: str) -> None:
        """Informs the code writer that the translation of a new VM file is 
        started.

        Args:
            filename (str): The name of the VM file.
        """
        self.file_name = filename


    def write_arithmetic(self, command: str) -> None:
        """Writes assembly code that is the translation of the given 
        arithmetic command.

        Args:
            command (str): the arithmetic command to translate.
        """
        output = ['//'+command+'\n']
        if command in ['add', 'sub', 'and', 'or']:
            output.extend(self.pop())
            output.append('A=A-1\n')
            output.append(self.DICT_COMMANDS[command]+'\n')
        elif command in ['neg', 'not']:
            output.append('@SP\n')
            output.append('A=M-1\n')
            output.append(self.DICT_COMMANDS[command]+'\n')
        elif command in ['eq', 'gt', 'lt']:
            label = self.file_name+'$'+str(self.label_counter)
            output.extend(self.pop())
            if command == 'eq':
                output.append('A=A-1\n')
                output.append('D=M-D\n')
            else:
                output.append(f'@POSITIVE.{label}\n')
                output.append('D;JGT\n')
                output.append('@SP\n')
                output.append('A=M-1\n')
                output.append('D=M\n')
                output.append(f'@SPACIAL.{label}\n')
                output.append('D;JGT\n')
                output.append(f'@CONTINUE.{label}\n')
                output.append('0;JMP\n')
                output.append(f'(POSITIVE.{label})\n')
                output.append('@SP\n')
                output.append('A=M-1\n')
                output.append('D=M\n')
                output.append(f'@SPACIAL.{label}\n')
                output.append('D;JLT\n')
                output.append(f'(CONTINUE.{label})\n')
                output.append('@SP\n')
                output.append('A=M\n')
                output.append('D=D-M\n')
                output.append(f'(SPACIAL.{label})\n')
            output.append(f'@TRUE.{label}\n')
            output.append('D;'+self.DICT_COMMANDS[command]+'\n')
            output.append('D=0\n')
            output.append(f'@FALSE.{label}\n')
            output.append('0;JMP\n')
            output.append(f'(TRUE.{label})\n')
            output.append('D=-1\n')
            output.append(f'(FALSE.{label})\n')
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
            output.extend(self.push())
        elif command == 'C_POP':
            if segment == 'static':
                output.extend(self.pop())
                output.append('@'+self.file_name+'.'+str(index)+'\n')
            elif segment in ['local', 'argument', 'this', 'that']:
                output.append('@'+str(index)+'\n')
                output.append('D=A\n')
                output.append('@'+self.DICT_SEGMENT[segment]+'\n')
                output.append('D=D+M\n')
                output.append('@R13\n')
                output.append('M=D\n')
                output.extend(self.pop())
                output.append('@R13\n')
                output.append('A=M\n')
            elif segment in ['pointer', 'temp']:
                output.append('@'+str(index)+'\n')
                output.append('D=A\n')
                output.append('@'+self.DICT_SEGMENT[segment]+'\n')
                output.append('D=D+A\n')
                output.append('@R13\n')
                output.append('M=D\n')
                output.extend(self.pop())
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
        output = [f'//({label})\n']
        output.append('(' + self.curr_func + '$' + label + ')\n')
        self.output_file.writelines(output)
        
    
    def write_goto(self, label: str) -> None:
        """Writes assembly code that affects the goto command.

        Args:
            label (str): the label to go to.
        """
        output = [f'//goto {label}\n']
        output.extend(self.goto(label))
        self.output_file.writelines(output)


    def write_if(self, label: str) -> None:
        """Writes assembly code that affects the if-goto command. 

        Args:
            label (str): the label to go to.
        """
        output = [f'//if-goto {label}\n']
        output.extend(self.if_goto(label))
        self.output_file.writelines(output)


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
        output = [f'//function {function_name} {str(n_vars)}\n']
        output.append('(' + function_name + ')\n') # function entry label
        output.append('D=0\n')
        for i in range(n_vars):
            output.extend(self.push()) # initialize local variables to 0
        self.output_file.writelines(output) # write to output file
        self.curr_func = function_name # update current function


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
        output = [f'//call {function_name} {str(n_args)}\n']
        output.append(f'@{function_name}$ret.{str(self.count_func)}\n') # generate a label and push it to the stack
        output.append('D=A\n') # push return_address
        output.extend(self.push())
        segments = ['LCL', 'ARG', 'THIS', 'THAT'] # push LCL, ARG, THIS, THAT
        for segment in segments:
            output.extend([f'@{segment}\n', 'D=M\n']) 
            output.extend(self.push())
        output.extend(['@SP\n', 'D=M\n', f'@{5+n_args} \n', 'D=D-A\n', '@ARG\n', 'M=D\n']) # ARG = SP-5-n_args
        output.extend(['@SP\n', 'D=M\n', '@LCL\n', 'M=D\n']) # LCL = SP
        output.extend([f'@{function_name}\n', '0;JMP\n']) # goto function_name
        output.append(f'({function_name}$ret.{str(self.count_func)})\n') # (return_address)
        self.output_file.writelines(output) # write to output file
        self.count_func += 1 # increment the counter

    
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
        output = ['//return\n']
        output.extend(['@LCL\n', 'D=M\n', '@R13\n', 'M=D\n']) # frame = LCL
        output.extend(['@5\n', 'D=D-A\n', 'A=D\n', 'D=M\n', '@R14\n', 'M=D\n']) # return_address = *(frame-5)
        output.extend(self.pop()) # *ARG = pop()
        output.extend(['@ARG\n', 'A=M\n', 'M=D\n'])
        output.extend(['@ARG\n', 'D=M+1\n', '@SP\n', 'M=D\n']) # SP = ARG + 1
        segments = ['THAT', 'THIS', 'ARG', 'LCL'] # restore THAT, THIS, ARG, LCL
        ind = 1
        for segment in segments:
            output.extend(['@R13\n', 'D=M\n', f'@{ind}\n', 'A=D-A\n', 'D=M\n', '@' + segment + '\n', 'M=D\n'])    
            ind += 1 
        output.extend(['@R14\n', 'A=M\n', '0;JMP\n']) # goto return_address
        self.output_file.writelines(output) # write to output file


    def write_init(self) -> None:
        """Writes assembly code that effects the VM initialization, also
        called bootstrap code. This code must be placed at the 
        beginning of the output file.
        """
        output = ['//init\n']
        output.append('@256\n')
        output.append('D=A\n')
        output.append('@SP\n')
        output.append('M=D\n')
        self.output_file.writelines(output)
        self.write_call('Sys.init', 0)

    def pop(self) -> None:
        """Writes assembly code that pops the top stack element."""
        return ['@SP\n', 'AM=M-1\n', 'D=M\n']
    
    def push(self) -> None:
        """Writes assembly code that pushes the top stack element."""
        return ['@SP\n', 'A=M\n', 'M=D\n', '@SP\n', 'M=M+1\n']
    
    def goto(self, label: str) -> None:
        """Writes assembly code that affects the goto command."""
        output = ['@' + self.curr_func + '$' + label + '\n']
        output.append('0;JMP\n')
        return output

    def if_goto(self, label: str) -> None:
        """Writes assembly code that affects the if-goto command."""
        output = self.pop()
        output.extend(['@' + self.curr_func + '$' + label + '\n'])
        output.append('D;JNE\n')
        return output

    def label(self, label: str) -> None:
        """Writes assembly code that affects the label command."""
        output = '(' + self.curr_func + '$' + label + ')\n'
        return output

    def close(self) -> None:
        """Closes the output file."""
        self.output_file.close()

    def write_init(self) -> None:
        """Writes assembly code that effects the VM initialization, also
        called bootstrap code. This code must be placed at the 
        beginning of the output file.
        """
        output = ['//init\n']
        output.append('@256\n')
        output.append('D=A\n')
        output.append('@SP\n')
        output.append('M=D\n')
        self.output_file.writelines(output)
        self.write_call('Sys.init', 0)