import unittest

from pyscm.env import global_env
from pyscm.parse import Token
from pyscm.pyscm import Interpret

SUCCESS = True
FAILURE = False


class TestSchemeInterpreter(unittest.TestCase):
    def setUp(self):
        self.interpreter = Interpret(global_env)

    def test_basic1(self):
        status, result = self.interpreter.interpret("42")
        self.assertEqual(status, SUCCESS)
        self.assertIsInstance(result, Token)

        # this is just to please the typechecker
        if isinstance(result, Token):
            self.assertEqual(result.literal, 42)

    def test_basic2(self):
        status, result = self.interpreter.interpret("#t")
        self.assertEqual(status, SUCCESS)
        self.assertIsInstance(result, Token)

        if isinstance(result, Token):
            self.assertEqual(result.literal, "#t")

    def test_basic3(self):
        status, result = self.interpreter.interpret("'abcd'")
        self.assertEqual(status, SUCCESS)
        self.assertIsInstance(result, Token)

        if isinstance(result, Token):
            self.assertEqual(result.literal, "'abcd'")

    def test_abs(self):
        status, result = self.interpreter.interpret("(abs -35)")
        self.assertEqual(status, SUCCESS)
        self.assertIsInstance(result, Token)

        if isinstance(result, Token):
            self.assertEqual(result.literal, 35)

    def test_ceiling1(self):
        status, result = self.interpreter.interpret("(ceiling 13.92)")
        self.assertEqual(status, SUCCESS)
        self.assertIsInstance(result, Token)

        if isinstance(result, Token):
            self.assertEqual(result.literal, 14)

    def test_ceiling2(self):
        status, result = self.interpreter.interpret("(ceiling (/ 2 18))")
        self.assertEqual(status, SUCCESS)
        self.assertIsInstance(result, Token)

        if isinstance(result, Token):
            self.assertEqual(result.literal, 1)

    def test_ceiling3(self):
        status, result = self.interpreter.interpret("(ceiling (/ 934.2 2.45))")
        self.assertEqual(status, SUCCESS)
        self.assertIsInstance(result, Token)

        if isinstance(result, Token):
            self.assertEqual(result.literal, 382)

    def test_define(self):
        status, result = self.interpreter.interpret(
            "(define x (if (< 2 4) (+ 2 (* 4 8)) (if #t 'if' 'else'))) x"
        )
        self.assertEqual(status, SUCCESS)
        self.assertIsInstance(result, Token)

        if isinstance(result, Token):
            self.assertEqual(result.literal, 34)

    def test_division1(self):
        status, result = self.interpreter.interpret("(/ 2 18)")
        self.assertEqual(status, SUCCESS)
        self.assertIsInstance(result, Token)

        if isinstance(result, Token):
            self.assertEqual(result.literal, "1/9")

    def test_division2(self):
        status, result = self.interpreter.interpret("(/ 8.8 2.2)")
        self.assertEqual(status, SUCCESS)
        self.assertIsInstance(result, Token)

        if isinstance(result, Token):
            self.assertEqual(result.literal, 4)

    def test_equal(self):
        status, result = self.interpreter.interpret("(= (+ 2 2) (* 2 2))")
        self.assertEqual(status, SUCCESS)
        self.assertIsInstance(result, Token)

        if isinstance(result, Token):
            self.assertEqual(result.literal, "#t")

    def test_floor1(self):
        status, result = self.interpreter.interpret("(floor 13.92)")
        self.assertEqual(status, SUCCESS)
        self.assertIsInstance(result, Token)

        if isinstance(result, Token):
            self.assertEqual(result.literal, 13.0)

    def test_floor2(self):
        status, result = self.interpreter.interpret("(floor (/ 2 18))")
        self.assertEqual(status, SUCCESS)
        self.assertIsInstance(result, Token)

        if isinstance(result, Token):
            self.assertEqual(result.literal, 0)

    def test_floor3(self):
        status, result = self.interpreter.interpret("(floor (/ 934.2 2.45))")
        self.assertEqual(status, SUCCESS)
        self.assertIsInstance(result, Token)

        if isinstance(result, Token):
            self.assertEqual(result.literal, 381)

    def test_ge(self):
        status, result = self.interpreter.interpret("(>= 4 4)")
        self.assertEqual(status, SUCCESS)
        self.assertIsInstance(result, Token)

        if isinstance(result, Token):
            self.assertEqual(result.literal, "#t")

    def test_le(self):
        status, result = self.interpreter.interpret("(<= 18 18)")
        self.assertEqual(status, SUCCESS)
        self.assertIsInstance(result, Token)

        if isinstance(result, Token):
            self.assertEqual(result.literal, "#t")

    def test_min_max(self):
        status, result = self.interpreter.interpret(
            "(min 1 2 3 4 (max -98 -96 -12 -4))"
        )
        self.assertEqual(status, SUCCESS)
        self.assertIsInstance(result, Token)

        if isinstance(result, Token):
            self.assertEqual(result.literal, -4)

    def test_minus(self):
        status, result = self.interpreter.interpret("(- 2 14)")
        self.assertEqual(status, SUCCESS)
        self.assertIsInstance(result, Token)

        if isinstance(result, Token):
            self.assertEqual(result.literal, -12)

    def test_multiply(self):
        status, result = self.interpreter.interpret("(* 1 2 3 4 5)")
        self.assertEqual(status, SUCCESS)
        self.assertIsInstance(result, Token)

        if isinstance(result, Token):
            self.assertEqual(result.literal, 120)

    def test_plus(self):
        status, result = self.interpreter.interpret("(+ 1 2 3 4 5)")
        self.assertEqual(status, SUCCESS)
        self.assertIsInstance(result, Token)

        if isinstance(result, Token):
            self.assertEqual(result.literal, 15)

    def test_round(self):
        status, result = self.interpreter.interpret("(round (/ 15 4))")
        self.assertEqual(status, SUCCESS)
        self.assertIsInstance(result, Token)

        if isinstance(result, Token):
            self.assertEqual(result.literal, 4)

    def test_set1(self):
        status, result = self.interpreter.interpret(
            "(define f 10) (set! f (+ f f 6)) f"
        )
        self.assertEqual(status, SUCCESS)
        self.assertIsInstance(result, Token)

        if isinstance(result, Token):
            self.assertEqual(result.literal, 26)

    def test_set2(self):
        status, _ = self.interpreter.interpret("(set! name 'siddharth')")
        self.assertEqual(status, FAILURE)

    def test_sqrt(self):
        status, result = self.interpreter.interpret("(sqrt (* 4 4))")
        self.assertEqual(status, SUCCESS)
        self.assertIsInstance(result, Token)

        if isinstance(result, Token):
            self.assertEqual(result.literal, 4.0)

    def test_begin(self):
        status, result = self.interpreter.interpret(
            "(define y 10) (begin (set! y (+ y 5)) y)"
        )
        self.assertEqual(status, SUCCESS)
        self.assertIsInstance(result, Token)

        if isinstance(result, Token):
            self.assertEqual(result.literal, 15)
