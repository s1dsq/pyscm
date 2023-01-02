import sys
from typing import Any, List, Tuple, Union

from .env import global_env
from .evaluate import EvalStatus, Evaluate
from .parse import Parse

SUCCESS = True
FAILURE = False


class Interpret:
    def __init__(self, env: dict):
        self.env = env
        self.parser = Parse()
        self.evaluator = Evaluate(self.parser, self.env)

    def split_expression(self, exp: str):
        lines = exp.replace("(", " ( ").replace(")", " ) ").split("\n")

        def filter_comment(line):
            line = line.lstrip()
            return line and line[0] != ";"

        expr_without_comments = list(filter(filter_comment, lines))

        return "".join(expr_without_comments).split()

    def interpret(self, exp: str) -> Tuple[bool, Union[List[Any], None, str]]:
        if not exp:
            return SUCCESS, None

        to_parse = self.split_expression(exp)
        status = SUCCESS
        results = []
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
                else:
                    if result:
                        results.append(result)
        return SUCCESS, results


def run_repl():
    try:
        interpreter = Interpret(global_env)
        while True:
            exp = input("pyscm> ")
            status, results = interpreter.interpret(exp)
            if status == SUCCESS:
                if isinstance(results, List):
                    for result in results:
                        if result:
                            print(result)
                elif results:
                    print(results)
            else:
                print("error:", results)
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
        status, results = interpreter.interpret(contents)
        if status == SUCCESS:
            if isinstance(results, List):
                for result in results:
                    if result:
                        print(result)
            elif results:
                print(results)
        else:
            print("error:", results)
    except OSError as e:
        print(e)
        sys.exit(1)
