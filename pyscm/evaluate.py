from dataclasses import dataclass
from enum import Enum, unique
from typing import Any

from .parse import Parse, Token, TokenType


@unique
class EvalStatus(Enum):
    SUCCESS = 0
    FAILURE = 1


@dataclass
class EvalResult:
    status: EvalStatus
    result: Any


@dataclass
class Evaluate:
    parser: Parse
    env: dict

    def evaluate(self, exp) -> EvalResult:
        if isinstance(exp, Token):
            if exp.token_type == TokenType.IDENT:
                if self.env.get(exp.literal, None) == None:
                    return EvalResult(
                        EvalStatus.FAILURE, f"undefined variable {exp.literal}"
                    )
                else:
                    return EvalResult(
                        EvalStatus.SUCCESS,
                        self.parser.get_token(self.env.get(exp.literal)),
                    )
            return EvalResult(EvalStatus.SUCCESS, exp)

        # evaluate the first element of the list this might be a function, macro or
        # special operator (terms taken from
        # https://en.wikipedia.org/wiki/Lisp_(programming_language))
        operator = self.evaluate(exp[0])
        if operator.status == EvalStatus.FAILURE:
            return operator
        op_token = operator.result.token_type

        args = []
        for i, arg in enumerate(exp[1:]):
            # set! and define don't take expression. They just bind names. Hence,
            # we assume they are just Token instances
            if i == 0 and (op_token == TokenType.SET or op_token == TokenType.DEFINE):
                try:
                    args.append(arg.literal)
                    continue
                except AttributeError:
                    return EvalResult(EvalStatus.FAILURE, "ill-formed definition")

            argi = self.evaluate(arg)
            if argi.status == EvalStatus.FAILURE:
                return argi

            # evaluate different branches for if statement. The dead branch is
            # never evaluated
            if op_token == TokenType.IF:
                if argi.result.literal == "#t":
                    return self.evaluate(exp[2])
                else:
                    return self.evaluate(exp[3])
            args.append(argi.result.literal)

        # set! checks if binding already exists before overwriting it
        if op_token == TokenType.SET:
            if self.env.get(args[0], None) == None:
                return EvalResult(EvalStatus.FAILURE, f"undefined variable {args[0]}")

            self.env[args[0]] = args[1]
            return EvalResult(EvalStatus.SUCCESS, ";no values returned")

        elif op_token == TokenType.DEFINE:
            self.env[args[0]] = args[1]
            return EvalResult(EvalStatus.SUCCESS, ";no values returned")

        # check if token exists in env. Call the procedure with the args if it
        # exists in env
        elif self.env.get(op_token, None) != None:
            try:
                key = op_token
                if operator.result.literal == "#t" or operator.result.literal == "#f":
                    key = operator.result.literal
                result = self.env[key](*args)
                # why is 1 == True and 2 != True in python?
                if type(result) == bool:
                    if result == True:
                        result = "#t"
                    elif result == False:
                        result = "#f"
                return EvalResult(
                    EvalStatus.SUCCESS, self.parser.get_token(str(result))
                )
            except Exception as e:
                return EvalResult(EvalStatus.FAILURE, e)
        return EvalResult(EvalStatus.FAILURE, "attempt to call a non procedure")
