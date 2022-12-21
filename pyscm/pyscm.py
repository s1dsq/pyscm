import sys
from typing import Tuple, Union

from .env import global_env
from .evaluate import EvalStatus, Evaluate
from .parse import Parse, Token

SUCCESS = True
FAILURE = False


class Interpret:
    def __init__(self, env: dict):
        self.env = env
        self.parser = Parse()
        self.evaluator = Evaluate(self.parser, self.env)

    def split_expression(self, exp: str):
        return exp.replace("(", " ( ").replace(")", " ) ").split()

    def interpret(self, exp: str) -> Tuple[bool, Union[Token, str, None]]:
        if not exp:
            return SUCCESS, None
        if exp.lstrip()[0] == ";":
            return SUCCESS, None

        to_parse = self.split_expression(exp)
        status = SUCCESS
        result = None
        while len(to_parse) > 0:
            ret, parsed_or_msg = self.parser.parse(to_parse)
            if not ret:
                return FAILURE, f"{parsed_or_msg}"
            else:
                evaluation = self.evaluator.evaluate(parsed_or_msg)
                status = evaluation.status
                result = evaluation.result
                if status == EvalStatus.FAILURE:
                    return FAILURE, result
        return SUCCESS, result


def run_repl():
    try:
        interpreter = Interpret(global_env)
        while True:
            exp = input("pyscm> ")
            status, result = interpreter.interpret(exp)
            if status == SUCCESS:
                if result:
                    print(result)
            else:
                print("error:", result)
    except (KeyboardInterrupt, EOFError):
        sys.exit(1)


def interpret_from_file(file):
    try:
        if not file.endswith("scm"):
            print("Can only interpret scheme file")
            sys.exit(1)
        interpreter = Interpret(global_env)
        f = open(file)
        contents = f.read()
        for line in contents.split("\n"):
            status, result = interpreter.interpret(line)
            if status == SUCCESS:
                if result:
                    print(result)
            else:
                print("error:", result)
    except OSError as e:
        print(e)
        sys.exit(1)
