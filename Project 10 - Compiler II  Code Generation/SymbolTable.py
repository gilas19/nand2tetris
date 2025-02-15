"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""


class SymbolTable:
    """A symbol table that associates names with information needed for Jack
    compilation: type, kind and running index. The symbol table has two nested
    scopes (class/subroutine).
    """
    IDENTIFIER_KINDS = ['ARG', 'VAR', 'STATIC', 'FIELD']

    def __init__(self) -> None:
        """Creates a new empty symbol table."""
        self.class_table = {} # {kind: {name: (type, index)}
        self.table = {kind: {} for kind in self.IDENTIFIER_KINDS}

    def start_subroutine(self) -> None:
        """Starts a new subroutine scope (i.e., resets the subroutine's
        symbol table).
        """
        self.table['ARG'] = {}
        self.table['VAR'] = {}

    def define(self, name: str, type: str, kind: str) -> None:
        """Defines a new identifier of a given name, type and kind and assigns
        it a running index. "STATIC" and "FIELD" identifiers have a class scope,
        while "ARG" and "VAR" identifiers have a subroutine scope.

        Args:
            name (str): the name of the new identifier.
            type (str): the type of the new identifier.
            kind (str): the kind of the new identifier, can be:
            "STATIC", "FIELD", "ARG", "VAR".
        """
        kind = kind.upper()
        self.table[kind][name] = (type, self.var_count(kind))

    def var_count(self, kind: str) -> int:
        """
        Args:
            kind (str): can be "STATIC", "FIELD", "ARG", "VAR".

        Returns:
            int: the number of variables of the given kind already defined in
            the current scope.
        """
        return len(self.table[kind])

    def kind_of(self, name: str) -> str:
        """
        Args:
            name (str): name of an identifier.

        Returns:
            str: the kind of the named identifier in the current scope, or None
            if the identifier is unknown in the current scope.
        """
        for kind in self.IDENTIFIER_KINDS:
            if self.table[kind].get(name, None):
                return kind
        return None

    def type_of(self, name: str) -> str:
        """
        Args:
            name (str):  name of an identifier.

        Returns:
            str: the type of the named identifier in the current scope.
        """
        return self.table[self.kind_of(name)][name][0]

    def index_of(self, name: str) -> int:
        """
        Args:
            name (str):  name of an identifier.

        Returns:
            int: the index assigned to the named identifier.
        """
        return self.table[self.kind_of(name)][name][1]
