"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
from JackTokenizer import JackTokenizer

class CompilationEngine:
    """Gets input from a JackTokenizer and emits its parsed structure into an
    output stream.
    """
    SYM_EX = ["+", "-", "*", "/", "&", "|", "<", ">", "=", "~", "^", "#"]
    ELEMENT_TYPE = {"KEYWORD": "keyword", "SYMBOL": "symbol", "IDENTIFIER": "identifier",
                "INT_CONST": "integerConstant", "STRING_CONST": "stringConstant"}


    def __init__(self, input_stream: "JackTokenizer", output_stream) -> None:
        """
        Creates a new compilation engine with the given input and output. The
        next routine called must be compileClass()
        :param input_stream: The input stream.
        :param output_stream: The output stream.
        """
        self.tokenizer = input_stream
        self.output_stream = output_stream
        self.tokenizer.advance()


    def compile_class(self) -> None:
        """Compiles a complete class."""
        self.tag("class", True)
        self.writer("KEYWORD", "class")
        self.writer("IDENTIFIER")
        self.writer("SYMBOL", "{")
        while self.tokenizer.token_type() == "KEYWORD" and self.tokenizer.keyword() in ["static", "field"]:
            self.compile_class_var_dec()
        while self.tokenizer.token_type() == "KEYWORD" and self.tokenizer.keyword() in ["constructor", "function", "method"]:
            self.compile_subroutine()
        self.writer("SYMBOL", "}")
        self.tag("class", False)

    def compile_class_var_dec(self) -> None:
        """Compiles a static declaration or a field declaration."""
        self.tag("classVarDec", True)
        self.writer("KEYWORD")
        self.valid_id()
        self.writer("IDENTIFIER")
        while self.tokenizer.token_type() == "SYMBOL" and self.tokenizer.symbol() == ",":
            self.writer("SYMBOL", ",")
            self.writer("IDENTIFIER")
        self.writer("SYMBOL", ";")
        self.tag("classVarDec", False)

    def compile_subroutine(self) -> None:
        """
        Compiles a complete method, function, or constructor.
        You can assume that classes with constructors have at least one field,
        you will understand why this is necessary in project 11.
        """
        self.tag("subroutineDec", True)
        self.writer("KEYWORD")
        self.valid_id()
        self.writer("IDENTIFIER")
        self.writer("SYMBOL", "(")
        self.compile_parameter_list()
        self.writer("SYMBOL", ")")
        self.compile_subroutine_body()
        self.tag("subroutineDec", False)
    
    def compile_subroutine_body(self) -> None:
        """Compiles a subroutine's body."""
        self.tag("subroutineBody", True)
        self.writer("SYMBOL", "{")
        while self.tokenizer.token_type() == "KEYWORD" and self.tokenizer.keyword() == "var":
            self.compile_var_dec()
        self.compile_statements()
        self.writer("SYMBOL", "}")
        self.tag("subroutineBody", False)

    def compile_parameter_list(self) -> None:
        """Compiles a (possibly empty) parameter list, not including the 
        enclosing "()".
        """
        self.tag("parameterList", True)
        while True:
            self.valid_id()
            if self.tokenizer.token_type() == "IDENTIFIER":
                self.writer("IDENTIFIER")
            if self.tokenizer.token_type() == "SYMBOL" and self.tokenizer.symbol() == ",":
                self.writer("SYMBOL", ",")
                continue
            break
        self.tag("parameterList", False)

    def compile_var_dec(self) -> None:
        """Compiles a var declaration."""
        self.tag("varDec", True)
        self.writer("KEYWORD", "var")
        self.valid_id()
        self.writer("IDENTIFIER")
        while self.tokenizer.token_type() == "SYMBOL" and self.tokenizer.symbol() == ",":
            self.writer("SYMBOL", ",")
            self.writer("IDENTIFIER")
        self.writer("SYMBOL", ";")
        self.tag("varDec", False)

    def compile_statements(self) -> None:
        """Compiles a sequence of statements, not including the enclosing 
        "{}".
        """
        self.tag("statements", True)
        while self.tokenizer.token_type() == "KEYWORD" and self.tokenizer.keyword() in ["let", "if", "while", "do", "return"]:
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
        self.tag("statements", False)

    def compile_do(self) -> None:
        """Compiles a do statement."""
        self.tag("doStatement", True)
        self.writer("KEYWORD", "do")
        self.writer("IDENTIFIER")
        if self.tokenizer.token_type() == "SYMBOL" and self.tokenizer.symbol() == ".": 
            self.writer("SYMBOL", ".")
            self.writer("IDENTIFIER")
        self.writer("SYMBOL", "(")
        self.compile_expression_list()
        self.writer("SYMBOL", ")")
        self.writer("SYMBOL", ";")
        self.tag("doStatement", False)

    def compile_let(self) -> None:
        """Compiles a let statement."""
        self.tag("letStatement", True)
        self.writer("KEYWORD", "let")
        self.valid_id()
        if self.tokenizer.token_type() == "SYMBOL" and self.tokenizer.symbol() == "[":
            self.writer("SYMBOL", "[")
            self.compile_expression()
            self.writer("SYMBOL", "]")
        self.writer("SYMBOL", "=")
        self.compile_expression()
        self.writer("SYMBOL", ";")
        self.tag("letStatement", False)

    def compile_while(self) -> None:
        """Compiles a while statement."""
        self.tag("whileStatement", True)
        self.writer("KEYWORD", "while")
        self.writer("SYMBOL", "(")
        self.compile_expression()
        self.writer("SYMBOL", ")")
        self.writer("SYMBOL", "{")
        self.compile_statements()
        self.writer("SYMBOL", "}")
        self.tag("whileStatement", False)

    def compile_return(self) -> None:
        """Compiles a return statement."""
        self.tag("returnStatement", True)
        self.writer("KEYWORD", "return")
        if self.tokenizer.token_type() == "SYMBOL" and self.tokenizer.symbol() == ";":
            self.writer("SYMBOL", ";")
        else:
            self.compile_expression()
            self.writer("SYMBOL", ";")
        self.tag("returnStatement", False)

    def compile_if(self) -> None:
        """Compiles a if statement, possibly with a trailing else clause."""
        self.tag("ifStatement", True)
        self.writer("KEYWORD", "if")
        self.writer("SYMBOL", "(")
        self.compile_expression()
        self.writer("SYMBOL", ")")
        self.writer("SYMBOL", "{")
        self.compile_statements()
        self.writer("SYMBOL", "}")
        if self.tokenizer.token_type() == "KEYWORD" and self.tokenizer.keyword() == "else":
            self.writer("KEYWORD", "else")
            self.writer("SYMBOL", "{")
            self.compile_statements()
            self.writer("SYMBOL", "}")
        self.tag("ifStatement", False)

    def compile_expression(self) -> None:
        """Compiles an expression."""
        self.tag("expression", True)
        self.compile_term()
        while self.tokenizer.token_type() == "SYMBOL" and self.tokenizer.symbol() in ["+", "-", "*", "/", "&", "|", "<", ">", "="]:
            self.writer("SYMBOL")
            self.compile_term()
        self.tag("expression", False)

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
        self.tag("term", True)
        if self.tokenizer.token_type() == "KEYWORD":
            self.writer("KEYWORD")
        elif self.tokenizer.token_type() == "INT_CONST":
            self.writer("INT_CONST")
        elif self.tokenizer.token_type() == "STRING_CONST":
            self.writer("STRING_CONST")
        elif self.tokenizer.token_type() == "SYMBOL" and self.tokenizer.symbol() == "(":
            self.writer("SYMBOL","(")
            self.compile_expression()
            self.writer("SYMBOL",")")
        elif self.tokenizer.token_type() == "SYMBOL" and self.tokenizer.symbol() in ["-", "~", "^", "#"]:
            self.writer("SYMBOL", self.tokenizer.symbol())
            self.compile_term()
        elif self.tokenizer.token_type() == "IDENTIFIER":
            self.writer("IDENTIFIER")
            if self.tokenizer.token_type() == "SYMBOL" and self.tokenizer.symbol() == "[":
                self.writer("SYMBOL", "[")
                self.compile_expression()
                self.writer("SYMBOL", "]")
            elif self.tokenizer.token_type() == "SYMBOL" and self.tokenizer.symbol() == "(":
                self.writer("SYMBOL", "(")
                self.compile_expression_list()
                self.writer("SYMBOL", ")")
            elif self.tokenizer.token_type() == "SYMBOL" and self.tokenizer.symbol() == ".":
                self.writer("SYMBOL", ".")
                self.writer("IDENTIFIER")
                self.writer("SYMBOL", "(")
                self.compile_expression_list()
                self.writer("SYMBOL", ")")
        self.tag("term", False)

    def compile_expression_list(self) -> None:
        """Compiles a (possibly empty) comma-separated list of expressions."""
        self.tag("expressionList", True)
        if self.tokenizer.token_type() == "SYMBOL" and self.tokenizer.symbol() == ")":
            self.tag("expressionList", False)
            return
        self.compile_expression()
        while self.tokenizer.token_type() == "SYMBOL" and self.tokenizer.symbol() == ",":
            self.writer("SYMBOL", ",")
            self.compile_expression()
        self.tag("expressionList", False)

    def valid_id(self):
        if self.tokenizer.token_type() == "KEYWORD":
            self.writer("KEYWORD")
        elif self.tokenizer.token_type() == "IDENTIFIER":
            self.writer("IDENTIFIER")

    def xml_symbols(self, token):
        token = token.replace("&", "&amp;")
        token = token.replace("<", "&lt;")
        token = token.replace(">", "&gt;")
        return token

    def writer(self, type, token=None):
        token_type = self.tokenizer.token_type()
        if type == "SYMBOL" and token_type == "SYMBOL": 
            if not token:
                token = self.tokenizer.symbol()
            elif token != self.tokenizer.symbol():
                raise SyntaxError(f"Expected {token} but got {self.tokenizer.symbol()}")
            token = self.xml_symbols(token)
        elif type == "KEYWORD" and token_type == "KEYWORD":
            if not token:
                token = self.tokenizer.keyword()
            elif token != self.tokenizer.keyword():
                raise SyntaxError(f"Expected {token} but got {self.tokenizer.keyword()}")
        elif type == "IDENTIFIER" and token_type == "IDENTIFIER":
            token = self.tokenizer.identifier()
        elif type == "INT_CONST" and token_type == "INT_CONST":
            token = self.tokenizer.int_val()
        elif type == "STRING_CONST" and token_type == "STRING_CONST":
            token = self.tokenizer.string_val()
        else:
            raise SyntaxError(f"Expected {type} but got {token_type} and {token}")
        type = self.ELEMENT_TYPE[type]
        self.output_stream.write(f'<{type}> {token} </{type}>\n')
        self.tokenizer.advance()
    
    def tag(self, token, flag):
        if flag:
            self.output_stream.write(f'<{token}>\n')
        else:
            self.output_stream.write(f'</{token}>\n')
