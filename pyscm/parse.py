from dataclasses import dataclass
from enum import Enum, unique
from typing import Union

List = list


@unique
class TokenType(Enum):
    PLUS = 1
    MINUS = 2
    MULTIPLY = 3
    DIVIDE = 4

    GREATER_THAN = 5
    LESS_THAN = 6
    GREATER_EQUAL = 7
    LESS_EQUAL = 8
    EQUAL = 9

    SQRT = 10
    FLOOR = 11
    CEIL = 12
    ROUND = 13
    MAX = 14
    MIN = 15
    ABS = 16

    IF = 17
    DEFINE = 18
    LET = 19
    SET = 20

    STRING = 21
    INT = 22
    FLOAT = 23
    BOOLEAN = 24
    IDENT = 25


@dataclass
class Token:
    token_type: TokenType
    literal: Union[str, int, float]

    def __str__(self):
        return str(self.literal)

    def __repr__(self):
        return str(self.literal)


@dataclass
class Parse:
    # recursive descent parsing
    def parse(self, exp: List):
        """
        Takes a list of tokens and recursively parses it
        Returns
        ------
        (status of parsing, parsed list or error message)
        """
        f = exp.pop(0)
        if f == "(":
            parsed = []
            while len(exp) > 0 and exp[0] != ")":
                ret, res = self.parse(exp)
                if ret:
                    parsed.append(res)
            # ')' next
            if len(exp) > 0:
                exp.pop(0)
                return True, parsed
            else:
                return False, "expected closing paranthesis"
        elif f == ")":
            return False, "unexpected closing paranthesis"
        else:
            return True, self.get_token(f)

    def get_token(self, t):
        try:
            return Token(TokenType.INT, int(t))
        except ValueError:
            try:
                return Token(TokenType.FLOAT, float(t))
            except ValueError:
                pass

        if t == "+":
            return Token(TokenType.PLUS, t)
        elif t == "-":
            return Token(TokenType.MINUS, t)
        elif t == "*":
            return Token(TokenType.MULTIPLY, t)
        elif t == "/":
            return Token(TokenType.DIVIDE, t)
        elif t == ">":
            return Token(TokenType.GREATER_THAN, t)
        elif t == "<":
            return Token(TokenType.LESS_THAN, t)
        elif t == ">=":
            return Token(TokenType.GREATER_EQUAL, t)
        elif t == "<=":
            return Token(TokenType.LESS_EQUAL, t)
        elif t == "=":
            return Token(TokenType.EQUAL, t)
        elif t == "sqrt":
            return Token(TokenType.SQRT, t)
        elif t == "floor":
            return Token(TokenType.FLOOR, t)
        elif t == "ceiling":
            return Token(TokenType.CEIL, t)
        elif t == "round":
            return Token(TokenType.ROUND, t)
        elif t == "max":
            return Token(TokenType.MAX, t)
        elif t == "min":
            return Token(TokenType.MIN, t)
        elif t == "abs":
            return Token(TokenType.ABS, t)
        elif t == "if":
            return Token(TokenType.IF, t)
        elif t == "define":
            return Token(TokenType.DEFINE, t)
        elif t == "set!":
            return Token(TokenType.SET, t)
        elif t[0] == "'" or t[0] == '"':
            return Token(TokenType.STRING, t)
        elif t == "#t" or t == "#f":
            return Token(TokenType.BOOLEAN, t)
        return Token(TokenType.IDENT, t)
