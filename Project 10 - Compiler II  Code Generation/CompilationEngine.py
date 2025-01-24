"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import JackTokenizer
import SymbolTable
import VMWriter


class CompilationEngine:
    """Gets input from a JackTokenizer and emits its parsed structure into an
    output stream.
    # """

    SYS_EX = {"+": "ADD", "-": "SUB", "*": "Math.multiply", "neg": "NEG",
              "/": "Math.divide", "&": "AND", "|": "OR", "<": "LT", ">": "GT",
              "=": "EQ", "~": "NOT", "^": "SHIFTLEFT", "#": "SHIFTRIGHT"}
    ELEMENT_TYPE = {"KEYWORD": "keyword", "SYMBOL": "symbol", "IDENTIFIER": "identifier",
                    "INT_CONST": "integerConstant", "STRING_CONST": "stringConstant"}


    def __init__(self, input_stream: "JackTokenizer", symbol_table: "SymbolTable",
                 vmwriter: "VMWriter") -> None:
        """
        Creates a new compilation engine with the given input and output. The
        next routine called must be compileClass()
        :param input_stream: The input stream.
        :param output_stream: The output stream.
        """
        self.tokenizer = input_stream
        self.symbol_table = symbol_table
        self.vmwriter = vmwriter
        self.class_name = ""
        self.subroutine_prop = {"name": "", "type": "", "kind": "", "n_args": 0, "while:": 0, "if:": 0}
        self.tokenizer.advance()
        self.compile_class()


    # 'class' className '{' classVarDec* subroutineDec* '}'
    def compile_class(self) -> None:
        """Compiles a complete class."""
        self.line()

        self.writer("KEYWORD", "class")
        self.class_name = self.writer('IDENTIFIER')

        self.writer("SYMBOL", "{")
        while (self.tokenizer.token_type() == "KEYWORD" and
               self.tokenizer.keyword() in ["static", "field"]):
            self.compile_class_var_dec()
        while self.tokenizer.token_type() == "KEYWORD" and self.tokenizer.keyword() in ["constructor", "function", "method"]:
            self.compile_subroutine()
        self.writer("SYMBOL", "}")


    # ('static' | 'field') type varName (',' varName)* ';'
    def compile_class_var_dec(self) -> None:
        """Compiles a static declaration or a field declaration."""
        kind = self.writer("KEYWORD")
        type = self.valid_id()
        name = self.writer("IDENTIFIER")
        self.symbol_table.define(name, type, kind)

        while self.tokenizer.token_type() == "SYMBOL" and self.tokenizer.symbol() == ",":
            self.writer("SYMBOL", ",")
            name = self.writer("IDENTIFIER")
            self.symbol_table.define(name, type, kind)
        self.writer("SYMBOL", ";")


    # ('constructor' | 'function' | 'method') ('void' | type) subroutineName '(' parameterList ')' subroutineBody
    def compile_subroutine(self) -> None:
        """
        Compiles a complete method, function, or constructor.
        You can assume that classes with constructors have at least one field,
        you will understand why this is necessary in project 11.
        """
        self.line()

        # reset subroutine properties
        self.subroutine_prop["type"] = self.writer("KEYWORD")
        self.subroutine_prop["kind"] = self.valid_id()
        self.subroutine_prop["name"] = self.writer("IDENTIFIER")
        self.subroutine_prop["while"] = self.subroutine_prop["if"] = 0

        # reset symbol table
        self.symbol_table.start_subroutine()
        if self.subroutine_prop["type"] == "method":
            self.symbol_table.define("this", self.class_name, "ARG")

        self.writer("SYMBOL", "(")
        self.compile_parameter_list()
        self.writer("SYMBOL", ")")
        self.compile_subroutine_body()


    # ((expression (',' expression)*)?)
    def compile_parameter_list(self) -> None:
        """Compiles a (possibly empty) parameter list, not including the
        enclosing "()".
        """
        while True:
            type = self.valid_id()
            if self.tokenizer.token_type() == "IDENTIFIER":
                name = self.writer("IDENTIFIER")
                self.symbol_table.define(name, type, "ARG")
            if self.tokenizer.token_type() == "SYMBOL" and self.tokenizer.symbol() == ",":
                self.writer("SYMBOL", ",")
                continue
            break


    # var type varName (',' varName)* ';'
    def compile_subroutine_body(self) -> None:
        """Compiles a subroutine's body."""
        self.writer("SYMBOL", "{")
        while self.tokenizer.token_type() == "KEYWORD" and self.tokenizer.keyword() == "var":
            self.compile_var_dec()
        self.vm_subroutine_dec()
        self.compile_statements()
        self.writer("SYMBOL", "}")


    # var type varName (',' varName)* ';'
    def compile_var_dec(self) -> None:
        """Compiles a var declaration."""
        self.writer("KEYWORD", "var")
        type = self.valid_id()
        name = self.writer("IDENTIFIER")
        self.symbol_table.define(name, type, "VAR")

        while self.tokenizer.token_type() == "SYMBOL" and self.tokenizer.symbol() == ",":
            self.writer("SYMBOL", ",")
            name = self.writer("IDENTIFIER")
            self.symbol_table.define(name, type, "VAR")
        self.writer("SYMBOL", ";")


    # statement*
    def compile_statements(self) -> None:
        """Compiles a sequence of statements, not including the enclosing
        "{}".
        """
        while (self.tokenizer.token_type() == "KEYWORD" and
               self.tokenizer.keyword() in ["let", "if", "while", "do", "return"]):
            self.line()
            if self.tokenizer.keyword() == "let":
                self.compile_let()
            elif self.tokenizer.keyword() == "if":
                self.compile_if()
            elif self.tokenizer.keyword() == "while":
                self.compile_while()
            elif self.tokenizer.keyword() == "do":
                self.compile_do()
            elif self.tokenizer.keyword() == "return":
                self.compile_return()


    # 'do' subroutineCall ';'
    def compile_do(self) -> None:
        """Compiles a do statement."""
        self.writer("KEYWORD", "do")
        name = self.writer("IDENTIFIER")
        self.compile_subroutine_call(name)
        self.vmwriter.write_pop("TEMP", 0)
        self.writer("SYMBOL", ";")


    # subroutineName '(' expressionList ')' | (className | varName) '.' subroutineName '(' expressionList ')'
    def compile_subroutine_call(self, name: str) -> None:

        """Compiles a subroutine call.

        Args:
            name: The name of the subroutine.
        """
        n_args = 0
        # (className | varName) '.' subroutineName
        if self.tokenizer.token_type() == "SYMBOL" and self.tokenizer.symbol() == ".":
            self.writer("SYMBOL", ".")
            subroutine_name = self.writer("IDENTIFIER")
            if self.symbol_table.kind_of(name) is not None:
                self.vmwriter.write_push(*self.symbol_table_call(name))
                name = f"{self.symbol_table.type_of(name)}.{subroutine_name}"
                n_args += 1
            else:
                name = f'{name}.{subroutine_name}'

        # subroutineName '(' expressionList ')'
        else:
            name = f'{self.class_name}.{name}'
            n_args += 1
            self.vmwriter.write_push("POINTER", 0)

        self.writer("SYMBOL", "(")
        n_args += self.compile_expression_list()
        self.writer("SYMBOL", ")")
        self.vmwriter.write_call(name, n_args)


    # 'let' varName ('[' expression ']')? '=' expression ';'
    def compile_let(self) -> None:
        """Compiles a let statement."""
        is_array = False
        self.writer("KEYWORD", "let")
        var_name = self.valid_id()

        if self.tokenizer.token_type() == "SYMBOL" and self.tokenizer.symbol() == "[":
            is_array = True
            self.compile_array(var_name)

        self.writer("SYMBOL", "=")
        self.compile_expression()
        self.writer("SYMBOL", ";")

        if is_array:
            self.vmwriter.write_pop("TEMP", 0) # pop expression 2 result to temp 0
            self.vmwriter.write_pop("POINTER", 1)
            self.vmwriter.write_push("TEMP", 0)
            self.vmwriter.write_pop("THAT", 0)
        else:
            self.vmwriter.write_pop(*self.symbol_table_call(var_name))


    # 'while' '(' expression ')' '{' statements '}'
    def compile_while(self) -> None:
        """Compiles a while statement."""
        curr_label = self.subroutine_prop["while"]
        self.subroutine_prop["while"] += 1

        self.writer("KEYWORD", "while")
        self.vmwriter.write_label(f"WHILE_EXP{curr_label}")
        self.writer("SYMBOL", "(")
        self.compile_expression()
        self.writer("SYMBOL", ")")

        self.vmwriter.write_arithmetic("NOT")
        self.vmwriter.write_if(f"WHILE_END{curr_label}")

        self.writer("SYMBOL", "{")
        self.compile_statements()
        self.writer("SYMBOL", "}")

        self.vmwriter.write_goto(f"WHILE_EXP{curr_label}")
        self.vmwriter.write_label(f"WHILE_END{curr_label}")


    # 'return' expression? ';'
    def compile_return(self) -> None:
        """Compiles a return statement."""
        self.writer("KEYWORD", "return")
        if (self.tokenizer.token_type() == "SYMBOL" and self.tokenizer.symbol() == ";" and self.subroutine_prop["kind"] == "void"):
            self.vmwriter.write_push("constant", 0)
        else:
            self.compile_expression()

        self.writer("SYMBOL", ";")
        self.vmwriter.write_return()


    # 'if' '(' expression ')' '{' statements '}' ('else' '{' statements '}')?
    def compile_if(self) -> None:
        """Compiles a if statement, possibly with a trailing else clause."""
        curr_label = self.subroutine_prop["if"]
        self.subroutine_prop["if"] += 1

        self.writer("KEYWORD", "if")
        self.writer("SYMBOL", "(")
        self.compile_expression()
        self.writer("SYMBOL", ")")

        self.vmwriter.write_if(f"IF_TRUE{curr_label}")
        self.vmwriter.write_goto(f"IF_FALSE{curr_label}")
        self.vmwriter.write_label(f"IF_TRUE{curr_label}")

        self.writer("SYMBOL", "{")
        self.compile_statements()
        self.writer("SYMBOL", "}")
        if self.tokenizer.token_type() == "KEYWORD" and self.tokenizer.keyword() == "else":
            self.vmwriter.write_goto(f"IF_END{curr_label}")
            self.vmwriter.write_label(f"IF_FALSE{curr_label}")
            self.writer("KEYWORD", "else")
            self.writer("SYMBOL", "{")
            self.compile_statements()
            self.writer("SYMBOL", "}")
            self.vmwriter.write_label(f"IF_END{curr_label}")
        else:
            self.vmwriter.write_label(f"IF_FALSE{curr_label}")


    # term (op term)*
    def compile_expression(self) -> None:
        """Compiles an expression."""
        self.compile_term()
        while self.tokenizer.token_type() == "SYMBOL" and self.tokenizer.symbol() in ["+", "-", "*", "/", "&", "|", "<", ">", "="]:
            op_token = self.writer("SYMBOL")
            self.compile_term()
            if op_token in ["*", "/"]:
                self.vmwriter.write_call(self.SYS_EX[op_token], 2)
            else:
                self.vmwriter.write_arithmetic(self.SYS_EX[op_token])


    # integerConstant | stringConstant | keywordConstant | varName |
    def compile_term(self) -> None:
        """Compiles a term.
        This routine is faced with a slight difficulty when
        trying to decide between some of the alternative parsing rules.
        Specifically, if the current token is an identifier, the routing must
        distinguish between a variable, an array entry, and a subroutine call.
        A single look-ahead token, which may be one of "[", "(", or "." suffices
        to distinguish between the three possibilities. Any other token is not
        part of this term and should not be advanced over.
        """
        if self.tokenizer.token_type() == "KEYWORD":
            token = self.writer("KEYWORD")
            if token == "this":
                self.vmwriter.write_push("POINTER", 0)
            elif token == "true":
                # self.vmwriter.write_push("CONST", 1)
                # self.vmwriter.write_arithmetic("NEG")
                self.vmwriter.write_push("CONST", 0)
                self.vmwriter.write_arithmetic("NOT")
            elif token in ["false", "null"]:
                self.vmwriter.write_push("CONST", 0)

        elif self.tokenizer.token_type() == "INT_CONST":
            int_token = self.writer("INT_CONST")
            self.vmwriter.write_push("CONST", int_token)

        elif self.tokenizer.token_type() == "STRING_CONST":
            string_token = self.writer("STRING_CONST")
            self.vm_string_constant(string_token)

        elif self.tokenizer.token_type() == "SYMBOL" and self.tokenizer.symbol() == "(":
            self.writer("SYMBOL","(")
            self.compile_expression()
            self.writer("SYMBOL",")")
        elif self.tokenizer.token_type() == "SYMBOL" and self.tokenizer.symbol() in ["-", "~", "^", "#"]:
            unary_op = self.writer("SYMBOL", self.tokenizer.symbol()).replace('-', 'neg')
            self.compile_term()
            self.vmwriter.write_arithmetic(self.SYS_EX[unary_op])

        elif self.tokenizer.token_type() == "IDENTIFIER":
            var_name = self.writer("IDENTIFIER")
            if self.tokenizer.token_type() == "SYMBOL" and self.tokenizer.symbol() == "[":
                self.compile_array(var_name)
                self.vmwriter.write_pop("POINTER", 1)
                self.vmwriter.write_push("THAT", 0)
            elif self.tokenizer.token_type() == "SYMBOL" and self.tokenizer.symbol() in ["(", "."]:
                self.compile_subroutine_call(var_name)
            else:
                self.vmwriter.write_push(*self.symbol_table_call(var_name))


    # (expression (',' expression)* )?
    def compile_expression_list(self) -> int:
        """Compiles a (possibly empty) comma-separated list of expressions."""
        args_count = 0

        # If there are no expressions, return
        if self.tokenizer.token_type() == "SYMBOL" and self.tokenizer.symbol() == ")":
            return args_count

        self.compile_expression()
        while self.tokenizer.token_type() == "SYMBOL" and self.tokenizer.symbol() == ",":
            self.writer("SYMBOL", ",")
            self.compile_expression()
            args_count += 1

        return args_count+1

    def symbol_table_call(self, name: str) -> tuple[str, int]:
        """ Finds kind and index of a variable in the symbol table.

        Args:
            name: The name of the variable.

        Returns:
            Tuple[str, int]: The kind and index of the variable.
        """
        return (self.symbol_table.kind_of(name), self.symbol_table.index_of(name))

    def valid_id(self) -> str:
        """Checks if the current token is a valid keyword or identifier.

        Returns:
            str: The current token."""
        token = ""
        if self.tokenizer.token_type() == "KEYWORD":
            token = self.tokenizer.keyword()
            self.writer("KEYWORD")
        elif self.tokenizer.token_type() == "IDENTIFIER":
            token = self.tokenizer.identifier()
            self.writer("IDENTIFIER")
        return token

    def writer(self, type: str, token=None) -> str:
        """Writes the current token to the output file.

        Args:
            type: The type of token to write.
            token: The token to write. If None, the current token is written.

        Returns:
            str: The token that was written.
        """
        token = self.token_valid(type, token)
        self.tokenizer.advance()
        return token

    def token_valid(self, input_type: str, input_token=None):
        """Checks if the current token matches the expected token.

        Args:
            type: The type of token to check.
            token: The token (string ot list) to check. If None, the current token is checked.

        Raises:
            SyntaxError: If the token does not match the expected token.
        """
        tokenizer_type = self.tokenizer.token_type()
        tokenizer_token = self.curr_token_data(tokenizer_type)

        if not input_token:
            input_token = tokenizer_token
        if isinstance(input_token, list) and tokenizer_token in input_token:
            return tokenizer_token
        if input_type == tokenizer_type and input_token == tokenizer_token:
            return input_token
        raise SyntaxError(f"Expected {input_token} but got {tokenizer_token}")

    def curr_token_data(self, type: str) -> str:
        """Gets the current token data.

        Args:
            type: The type of token to get.
            token: The token to get. If None, the current token is returned.

        Returns:
            str: The token data.
        """
        if type == "KEYWORD":
            return self.tokenizer.keyword()
        if type == "SYMBOL":
            return self.tokenizer.symbol()
        if type == "IDENTIFIER":
            return self.tokenizer.identifier()
        if type == "INT_CONST":
            return self.tokenizer.int_val()
        if type == "STRING_CONST":
            return self.tokenizer.string_val()

    def vm_subroutine_dec(self) -> None:
        """Write subroutine declaration to VMWriter"""
        self.vmwriter.write_function(f'{self.class_name}.{self.subroutine_prop["name"]}',
                                        self.symbol_table.var_count("VAR"))
        if self.subroutine_prop["type"] == "method":
            self.vmwriter.write_push("ARG", 0)
            self.vmwriter.write_pop("POINTER", 0)
        elif self.subroutine_prop["type"] == "constructor":
            self.vmwriter.write_push("CONST", self.symbol_table.var_count("FIELD"))
            self.vmwriter.write_call("Memory.alloc", 1)
            self.vmwriter.write_pop("POINTER", 0)

    def vm_string_constant(self, token: str) -> None:
        """Write string constant to VMWriter

        Args:
            token: The string constant to write.
        """
        self.vmwriter.write_push("CONST", len(token))
        self.vmwriter.write_call("String.new", 1)
        for char in token:
            self.vmwriter.write_push("CONST", ord(char))
            self.vmwriter.write_call("String.appendChar", 2)

    def compile_array(self, var: str) -> None:
        """Compiles an array statement.

        Args:
            var: The name of the array variable.
        """
        self.writer("SYMBOL", "[")
        self.compile_expression()
        self.writer("SYMBOL", "]")
        self.vmwriter.write_push(*self.symbol_table_call(var))
        self.vmwriter.write_arithmetic("ADD") # add array index to base address

    def line(self) -> None:
        """Writes the current line to the output file."""
        # print(self.tokenizer.line_tokens)
        # self.vmwriter.comment(self.tokenizer.line_tokens)
        pass
