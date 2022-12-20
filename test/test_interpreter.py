from pyscm.pyscm import Interpret
from pyscm.env import global_env
import unittest

class TestSchemeInterpreter(unittest.TestCase):
    def setUp(self):
        self.interpreter = Interpret(global_env)

    def test_basic1(self):
        _, result = self.interpreter.interpret("42")
        self.assertEqual(result.literal, 42)

    def test_basic2(self):
        _, result = self.interpreter.interpret("#t")
        self.assertEqual(result.literal, "#t")

    def test_basic3(self):
        _, result = self.interpreter.interpret("'abcd'")
        self.assertEqual(result.literal, "'abcd'")

    def test_abs(self):
        _, result = self.interpreter.interpret("(abs -35)")
        self.assertEqual(result.literal, 35)

    def test_ceiling1(self):
        _, result = self.interpreter.interpret("(ceiling 13.92)")
        self.assertEqual(result.literal, 14)

    def test_ceiling2(self):
        _, result = self.interpreter.interpret("(ceiling (/ 2 18))")
        self.assertEqual(result.literal, 1)

    def test_ceiling3(self):
        _, result = self.interpreter.interpret("(ceiling (/ 934.2 2.45))")
        self.assertEqual(result.literal, 382)

    def test_define(self):
        _, result = self.interpreter.interpret("(define x (if (< 2 4) (+ 2 (* 4 8)) (if #t 'if' 'else')))")
        _, result = self.interpreter.interpret("x")
        self.assertEqual(result.literal, 34)

    def test_division1(self):
        _, result = self.interpreter.interpret("(/ 2 18)")
        self.assertEqual(result.literal, "1/9")

    def test_division2(self):
        _, result = self.interpreter.interpret("(/ 8.8 2.2)")
        self.assertEqual(result.literal, 4)

    def test_equal(self):
        _, result = self.interpreter.interpret("(= (+ 2 2) (* 2 2))")
        self.assertEqual(result.literal, "#t")

    def test_floor1(self):
        _, result = self.interpreter.interpret("(floor 13.92)")
        self.assertEqual(result.literal, 13.0)

    def test_floor2(self):
        _, result = self.interpreter.interpret("(floor (/ 2 18))")
        self.assertEqual(result.literal, 0)

    def test_floor3(self):
        _, result = self.interpreter.interpret("(floor (/ 934.2 2.45))")
        self.assertEqual(result.literal, 381)

    def test_ge(self):
        _, result = self.interpreter.interpret("(>= 4 4)")
        self.assertEqual(result.literal, "#t")

    def test_le(self):
        _, result = self.interpreter.interpret("(<= 18 18)")
        self.assertEqual(result.literal, "#t")

    def test_min_max(self):
        _, result = self.interpreter.interpret("(min 1 2 3 4 (max -98 -96 -12 -4))")
        self.assertEqual(result.literal, -4)

    def test_minus(self):
        _, result = self.interpreter.interpret("(- 2 14)")
        self.assertEqual(result.literal, -12)

    def test_multiply(self):
        _, result = self.interpreter.interpret("(* 1 2 3 4 5)")
        self.assertEqual(result.literal, 120)

    def test_plus(self):
        _, result = self.interpreter.interpret("(+ 1 2 3 4 5)")
        self.assertEqual(result.literal, 15)

    def test_round(self):
        _, result = self.interpreter.interpret("(round (/ 15 4))")
        self.assertEqual(result.literal, 4)

    def test_set1(self):
        _, result = self.interpreter.interpret("(define f 10)")
        _, result = self.interpreter.interpret("(set! f (+ f f 6))")
        _, result = self.interpreter.interpret("f")
        self.assertEqual(result.literal, 26)

    def test_set2(self):
        _, result = self.interpreter.interpret("(set! name 'siddharth')")
        self.assertEqual(result, "undefined variable name")

    def test_sqrt(self):
        _, result = self.interpreter.interpret("(sqrt (* 4 4))")
        self.assertEqual(result.literal, 4.0)
