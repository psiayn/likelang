from typing import Any, Dict, List, cast

from lark import Transformer
from lark.lexer import Token
from lark.tree import Tree
from lark.visitors import v_args


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
    def assignment(self, tree: Tree):
        if self._should_not_eval():
            return tree

        identifier, res = cast(List, tree.children)
        self._scopes[-1][identifier] = {"type": "var", "value": res}
        return self._scopes[-1][identifier]

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
        return ident["value"]

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
        self._scopes[-1][name] = {"type": "fn", "args": args, "body": body}
        return self._scopes[-1][name]

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
        elif ident_scope["type"] != "fn":
            raise LikeSyntaxError("tried to call variable")
        elif len(ident_scope["args"]) != len(args):
            raise LikeSyntaxError(
                "expected: {} args, got {}.".format(len(ident_scope["args"]), len(args))
            )
        self._scopes.append(
            {
                param: {"value": arg, "type": "var"}
                for param, arg in zip(ident_scope["args"], args)
            }
        )
        result = self.transform(ident_scope["body"])
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
