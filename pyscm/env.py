import math
import operator as op

from .parse import TokenType
from .procedure import ceiling, divide, reduce

global_env = {
    TokenType.PLUS: lambda *args: reduce(op.add, *args),
    TokenType.MINUS: op.sub,
    TokenType.MULTIPLY: lambda *args: reduce(op.mul, *args),
    TokenType.DIVIDE: lambda a, b: divide(a, b),
    TokenType.GREATER_THAN: op.gt,
    TokenType.LESS_THAN: op.lt,
    TokenType.GREATER_EQUAL: op.ge,
    TokenType.LESS_EQUAL: op.le,
    TokenType.EQUAL: op.eq,
    TokenType.SQRT: math.sqrt,
    TokenType.FLOOR: math.floor,
    TokenType.CEIL: lambda n: ceiling(n),
    TokenType.ROUND: round,
    TokenType.MAX: max,
    TokenType.MIN: min,
    TokenType.ABS: abs,
    "#t": True,
    "#f": False,
}
