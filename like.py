from lark import Lark

with open("like.lark") as f:
    lark_parser = Lark(f.read(), start="start")

with open("like.ll") as f:
    lark_lang = f.read()

print(lark_parser.parse(lark_lang).pretty())