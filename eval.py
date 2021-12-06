from lark import Transformer
from lark.lexer import Token
from lark.tree import Tree
from typing import List, Dict, Any


class LikeSyntaxError(Exception):
    pass


class LikeEvaluator(Transformer):

    def __init__(self):
        self.scope: List[Dict[str, Any]] = [{}]
        self.func_counter: int = 0

    def expression(self, items):
        if self.func_counter:
            return items

        print(items)

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

    def number(self, num_str: Token):
        return float(num_str[0])

    def assignment(self, items: List):
        if self.func_counter:
            return items
        identifier, res = items
        self.scope[-1][identifier] = {'type': 'var', 'value': res}
        return self.scope[-1][identifier]

    def identifier(self, ident: List[Token]):
        return ident[0].value

    def start_fn(self, tokens):
        self.func_counter += 1

    def end_fn(self, tokens):
        self.func_counter -= 1

    def function(self, items: List):
        _, name, args, body, _ = items
        self.scope[-1][name] = {'type': 'fn', 'args': args, 'body': body}
        return self.scope[-1][name]

    def func_call(self, items: List):
        name, args = items
        print(self.scope)
        ident_scope = self._get_ident(name)
        if not ident_scope:
            raise LikeSyntaxError("function not found")
        elif ident_scope['type'] != 'fn':
            raise LikeSyntaxError("tried to call variable")
        return items

    def args(self, items: List):
        return items

    def _get_ident(self, ident: str):
        for scope in self.scope:
            if ident in scope.keys():
                return scope[ident]
