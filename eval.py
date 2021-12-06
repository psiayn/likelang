from lark import Transformer
from lark.lexer import Token
from lark.tree import Tree


class LikeSyntaxError(Exception):
    pass


class LikeEvaluator(Transformer):
    def expression(self, items):
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
                LikeSyntaxError("aaaa unknown operator")

        elif len(items) == 1:
            return items[0]

        else:
            raise LikeSyntaxError(
                f"Expression did not get 3 things what to dooo: {items}"
            )

    def number(self, num_str: Token):
        return float(num_str[0])
