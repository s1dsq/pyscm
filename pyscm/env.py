from fractions import Fraction
import math
import operator as op

from .parse import TokenType


def reduce(f, *iterable):
    """
    f is a function which takes 2 arguments. The result is calculated by
    applying f on first two elements of iterable, then applying f to that
    result and the 3rd element etc. Inspired from clojure
    """
    if len(iterable) == 0:
        return f
    elif len(iterable) == 1:
        return iterable[0]
    result = f(iterable[0], iterable[1])
    for e in iterable[2:]:
        result = f(result, e)
    return result


global_env = {
    TokenType.PLUS: lambda *args: reduce(op.add, *args),
    TokenType.MINUS: op.sub,
    TokenType.MULTIPLY: lambda *args: reduce(op.mul, *args),
    TokenType.DIVIDE: lambda a, b: Fraction(a, b),
    TokenType.GREATER_THAN: op.gt,
    TokenType.LESS_THAN: op.lt,
    TokenType.GREATER_EQUAL: op.ge,
    TokenType.LESS_EQUAL: op.le,
    TokenType.EQUAL: op.eq,
    TokenType.SQRT: math.sqrt,
    TokenType.FLOOR: math.floor,
    TokenType.CEIL: math.ceil,
    TokenType.ROUND: round,
    TokenType.MAX: max,
    TokenType.MIN: min,
    TokenType.ABS: abs,
    "#t": True,
    "#f": False,
}
