from fractions import Fraction
import math
import operator as op


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


def ceiling(n):
    try:
        return math.ceil(n)
    except TypeError:
        return math.ceil(Fraction(n))


def floor(n):
    try:
        return math.floor(n)
    except TypeError:
        return math.floor(Fraction(n))


def divide(a, b):
    try:
        return Fraction(a, b)
    except TypeError:
        return op.truediv(a, b)


def scm_round(n):
    try:
        round(n)
    except TypeError:
        return round(Fraction(n))
