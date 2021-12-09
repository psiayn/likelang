from lark import Lark

from like.eval import LikeEvaluator, LikeSyntaxError

import sys

filename = sys.argv[1]

with open("like.lark") as f:
    lark_parser = Lark(f.read(), start="start", parser="lalr")

with open(filename) as f:
    lark_lang = f.read()
try:
    ast = lark_parser.parse(lark_lang)
    # print(ast.pretty())
    res = LikeEvaluator().transform(ast)
except LikeSyntaxError as le:
    print(le)
except Exception as e:
    print(e)
