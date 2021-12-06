from lark import Lark

from eval import LikeEvaluator

with open("like.lark") as f:
    lark_parser = Lark(f.read(), start="start", parser="lalr")

with open("like.ll") as f:
    lark_lang = f.read()

ast = lark_parser.parse(lark_lang)

print(ast.pretty())

LikeEvaluator().transform(ast)
