import re
from typing import Any, Dict, List, Tuple, cast

from lark import Transformer
from lark.lexer import Token
from lark.tree import Tree
from lark.visitors import v_args

import like_types


class LikeSyntaxError(Exception):
    pass


class LikeEvaluator(Transformer):
    def __init__(self):
        self._scopes: List[Dict[str, Any]] = [{}]
        self._func_counter: int = 0

    def _should_not_eval(self) -> bool:
        return self._func_counter > 0

    @v_args(tree=True)
    def expression(self, tree: Tree):
        if self._should_not_eval():
            return tree

        items = cast(List, tree.children)

        if len(items) == 3:
            op1, operator, op2 = items
            operator: Tree
            if isinstance(op1, like_types.Variable):
                op1 = op1.value
            if isinstance(op2, like_types.Variable):
                op2 = op2.value
            if operator.data == "add":
                return op1 + op2
            elif operator.data == "sub":
                return op1 - op2
            elif operator.data == "mul":
                return op1 * op2
            elif operator.data == "div":
                return op1 / op2
            else:
                raise LikeSyntaxError("aaaa unknown operator")

        elif len(items) == 1:
            return items[0]

        else:
            raise LikeSyntaxError(
                f"Expression did not get 3 things what to dooo: {items}"
            )

    @v_args(tree=True)
    def number(self, tree: Tree):
        if self._should_not_eval():
            return tree

        return float(cast(str, tree.children)[0])

    @v_args(tree=True)
    def string(self, tree: Tree):
        if self._should_not_eval():
            return tree
        return cast(str, tree.children)[0].strip('"')

    @v_args(tree=True)
    def assignment(self, tree: Tree):
        if self._should_not_eval():
            return tree

        identifier, res = cast(List, tree.children)
        var = like_types.Variable(identifier, res)
        self._scopes[-1][identifier] = var
        return var

    @v_args(tree=True)
    def identifier(self, tree: Tree):
        if self._should_not_eval():
            return tree

        return cast(Token, tree.children[0]).value

    @v_args(tree=True)
    def existing_ident(self, tree: Tree):
        if self._should_not_eval():
            return tree

        items = cast(List, tree.children)
        ident = self._get_ident(items[0])
        if not ident:
            raise LikeSyntaxError(f"Unknown variable: {items[0]}")
        return ident

    @v_args(tree=True)
    def start_fn(self, tree: Tree):
        self._func_counter += 1

        return tree if self._should_not_eval() else None

    @v_args(tree=True)
    def end_fn(self, tree: Tree):
        self._func_counter -= 1

        return tree if self._should_not_eval() else None

    @v_args(tree=True)
    def function(self, tree: Tree):
        if self._should_not_eval():
            return tree

        name, args, _, body, _ = cast(List, tree.children)
        func = like_types.Function(name, args, body)
        self._scopes[-1][name] = func
        return func

    @v_args(tree=True)
    def func_call(self, tree: Tree):
        if self._should_not_eval():
            return tree

        name, args = cast(List, tree.children)
        if name == "print":
            print(*args)
            return None

        ident_scope = self._get_ident(name)
        if not ident_scope:
            raise LikeSyntaxError("function not found")
        elif isinstance(ident_scope, like_types.Variable):
            raise LikeSyntaxError("tried to call variable")
        elif isinstance(ident_scope, like_types.Collect):
            funs = [fun for name, fun in ident_scope.value if name == ""]

            if not funs:
                raise LikeSyntaxError("Function not found")
            if len(funs) > 1:
                raise LikeSyntaxError("Too many functions found aaa")

            ident_scope = funs[0]
        elif len(ident_scope.args) != len(args):
            raise LikeSyntaxError(
                "expected: {} args, got {}.".format(len(ident_scope.args), len(args))
            )
        self._scopes.append(
            {
                param: like_types.Variable(param, arg)
                for param, arg in zip(ident_scope.args, args)
            }
        )
        result = self.transform(ident_scope.value)
        self._scopes.pop()
        return result

    @v_args(tree=True)
    def params(self, tree: Tree):
        return tree if self._should_not_eval() else tree.children

    @v_args(tree=True)
    def args(self, tree: Tree):
        return tree if self._should_not_eval() else tree.children

    @v_args(tree=True)
    def block(self, tree: Tree):
        if self._should_not_eval():
            return tree

        return tree.children[-1]

    @v_args(tree=True)
    def start(self, tree: Tree):
        if self._should_not_eval():
            return tree

        return tree.children[-1]

    def _get_ident(self, ident: str):
        for scope in reversed(self._scopes):
            if ident in scope.keys():
                return scope[ident]

    @v_args(tree=True)
    def collect(self, tree: Tree):
        if self._should_not_eval():
            return tree

        identifier, pattern = cast(List, tree.children)
        pattern = pattern.strip("/")
        functions = self._get_functions()

        if pattern[-1] == "*":
            pattern_type = "prefix"

            def filter_func(fun):
                return fun[0].startswith(pattern[:-1])

            def extract_func(fun):
                return fun[0][len(pattern[:-1]) :]

        elif pattern[0] == "*":
            pattern_type = "postfix"

            def filter_func(fun):
                return fun[0].endswith(pattern[1:])

            def extract_func(fun):
                return fun[0][: -len(pattern[1:])]

        else:
            raise LikeSyntaxError("Invalid pattern. Use a * at the beginning or end.")

        matching_functions = list(filter(filter_func, functions))
        fun_names = list(map(extract_func, matching_functions))
        _collect = like_types.Collect(
            [
                (fun_name, fun)
                for fun_name, (_, fun) in zip(fun_names, matching_functions)
            ],
            pattern_type,
        )
        self._scopes[-1][identifier] = _collect
        return _collect

    def _get_functions(self) -> List[Tuple[str, Any]]:
        function = []
        for scope in self._scopes:
            for (key, value) in scope.items():
                if isinstance(value, like_types.Function):
                    function.append((key, value))
        return function

    @v_args(tree=True)
    def collect_call(self, tree: Tree):
        # do not evaluate until execution is reached
        if self._should_not_eval():
            return tree

        # destructuring the tree
        prefix, postfix, args = cast(List, tree.children)

        # checking if prefix exists
        pref_scope = self._get_ident(prefix)
        if isinstance(pref_scope, like_types.Collect):
            # getting functions that match the postfix
            matching_function = list(filter(lambda x: x[0] == postfix, cast(List[Tuple], pref_scope.value)))

            # checking if no funtions match
            if len(matching_function) < 1:
                raise LikeSyntaxError("Tried to call invalid function")

            # checking if more than function matches
            if len(matching_function) > 1:
                raise LikeSyntaxError("Ambiguous function call")

            # storing the matching function
            function = matching_function[0][1]
        else:
            # check if postfix exists
            post_scope = self._get_ident(postfix)
            if isinstance(post_scope, like_types.Collect):
                # getting functions that match the prefix
                matching_function = list(filter(lambda x: x[0] == prefix, cast(List[Tuple], post_scope.value)))

                # checking if no functions match
                if len(matching_function) < 1:
                    raise LikeSyntaxError("Tried to call invalid function")

                # checking if multiple functions match
                if len(matching_function) > 1:
                    raise LikeSyntaxError("Ambiguous function call")

                # storing the matching function
                function = matching_function[0][1]
            else:
                raise LikeSyntaxError("Trying to use collect on no collect types")

        # check if args match
        if len(function.args) != len(args):
            raise LikeSyntaxError(
                "expected: {} args, got {}.".format(len(function.args), len(args))
            )

        # create a new scope with args
        self._scopes.append(
            {
                param: like_types.Variable(param, arg)
                for param, arg in zip(function.args, args)
            }
        )

        # get the result of the function and pop the scope
        result = self.transform(function.value)
        self._scopes.pop()

        return result