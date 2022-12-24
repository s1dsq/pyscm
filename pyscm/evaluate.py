from copy import deepcopy
from dataclasses import dataclass
from enum import Enum, unique
from typing import Any, Optional

from .parse import Parse, Token, TokenType


@unique
class EvalStatus(Enum):
    SUCCESS = 0
    FAILURE = 1


@dataclass
class EvalResult:
    status: EvalStatus
    result: Optional[Any]


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
        op_token = None
        if operator.result != None:
            try:
                iter(operator.result)
            except TypeError:
                op_token = operator.result.token_type
            else:
                pass

        args = []
        for i, arg in enumerate(exp[1:]):
            # set! and define don't take expression. They just bind names. Hence,
            # we assume that the first argument is a Token of type IDENT
            if i == 0 and (op_token == TokenType.SET or op_token == TokenType.DEFINE):
                if isinstance(arg, Token):
                    if arg.token_type != TokenType.IDENT:
                        return EvalResult(EvalStatus.FAILURE, "argument of wrong type")
                    else:
                        args.append(arg.literal)
                        continue
                else:
                    assert len(exp) > 2

                    # check if we have a valid function call expression
                    fn_name = arg[0]
                    if (
                        not isinstance(fn_name, Token)
                        or fn_name.token_type != TokenType.IDENT
                    ):
                        return EvalResult(EvalStatus.FAILURE, "ill-formed definition")
                    fn_args = arg[1:]
                    for fn_arg in fn_args:
                        if (
                            not isinstance(fn_arg, Token)
                            or fn_arg.token_type != TokenType.IDENT
                        ):
                            return EvalResult(
                                EvalStatus.FAILURE, "ill-formed definition"
                            )

                    args = [
                        fn_name.literal,
                        [self.parser.get_token("lambda"), fn_args, exp[2]],
                    ]
                    break

            if op_token == TokenType.LAMBDA:
                return EvalResult(EvalStatus.SUCCESS, exp)

            argi = self.evaluate(arg)
            if argi.status == EvalStatus.FAILURE:
                return argi
            if argi.result == None:
                continue

            # evaluate different branches for if statement. The dead branch is
            # never evaluated
            if op_token == TokenType.IF:
                if argi.result.literal == "#t":
                    return self.evaluate(exp[2])
                else:
                    return self.evaluate(exp[3])
            if isinstance(argi.result, Token):
                args.append(argi.result.literal)
            else:
                args.append(argi.result)

        if operator.result != None:
            try:
                iter(operator.result)
            except TypeError:
                pass
            else:
                op_token = operator.result[0].token_type

        # set! checks if binding already exists before overwriting it
        if op_token == TokenType.SET:
            if self.env.get(args[0], None) == None:
                return EvalResult(EvalStatus.FAILURE, None)

            self.env[args[0]] = args[1]
            return EvalResult(EvalStatus.SUCCESS, None)

        elif op_token == TokenType.DEFINE:
            self.env[args[0]] = args[1]
            return EvalResult(EvalStatus.SUCCESS, None)

        elif op_token == TokenType.LAMBDA:
            assert operator.result != None

            named_args = operator.result[1]
            # the function should be called with expected number of arguments
            if len(named_args) != len(args):
                return EvalResult(
                    EvalStatus.FAILURE,
                    f"function expects {len(operator.result[1])} arguments, got {len(args)} instead",
                )

            # replace named parameters in the function body with the arguments
            # provided and evaluate the new expression. Make sure to copy the
            # body to not override the arguments in the function definition
            # permanently
            fn_body = deepcopy(operator.result[2])

            for i, name in enumerate(named_args):
                self.replace_token(fn_body, name, self.parser.get_token(args[i]))

            return self.evaluate(fn_body)

        elif op_token == TokenType.IDENT:
            assert operator.result != None

            fn = operator.result.literal
            call = [fn]
            for arg in args:
                call.append(self.parser.get_token(arg))

            return self.evaluate(call)

        # check if token exists in env. Call the procedure with the args if it
        # exists in env
        elif self.env.get(op_token, None) != None:
            try:
                key = op_token
                if operator.result != None and (
                    operator.result.literal == "#t" or operator.result.literal == "#f"
                ):
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

    def replace_token(self, exp, to_replace: Token, replace_with: Token):
        if isinstance(exp, Token):
            if exp == to_replace:
                return replace_with
            return exp

        for i, e in enumerate(exp):
            exp[i] = self.replace_token(e, to_replace, replace_with)
        return exp
