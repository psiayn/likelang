import sys

from colorama import Back, Fore, Style, init
from lark import Lark
from lark.exceptions import UnexpectedCharacters, UnexpectedInput, VisitError

from eval import LikeEvaluator, LikeSyntaxError

init()

filename = sys.argv[1]


def error_print(type: str, s: str):
    print(f"{Fore.RED}{type}:{Style.RESET_ALL} {s}")


def syntax_error(s: str):
    error_print("Syntax Error", s)


def runtime_error(s: str):
    error_print("Runtime Error", s)


def get_context(u: UnexpectedInput, text: str):
    pos = u.pos_in_stream

    start = pos

    while start >= 0:
        if text[start] == "\n":
            break
        start -= 1

    if start == -1:
        start += 1

    # if text[start] == "\n":
    #     start -= 1

    end = pos

    while end < len(text):
        if text[end] == "\n":
            break
        end += 1

    if end == len(text):
        end -= 1

    # if text[end] == "\n":
    #     end += 1

    line = text[start:end]

    s = line.expandtabs()

    err = (
        f"{Fore.BLACK}{Back.WHITE}{s}{Style.RESET_ALL}\n"
        + " " * (len(text[start:pos].expandtabs()) - 1)
        + f"{Fore.BLUE}^{Style.RESET_ALL}"
    )

    return err


with open("like.lark") as f:
    lark_parser = Lark(f.read(), start="start", parser="lalr")

with open(filename) as f:
    inp_str = f.read()
try:
    ast = lark_parser.parse(inp_str)
    # print(ast.pretty())
    res = LikeEvaluator().transform(ast)
except VisitError as ve:
    if isinstance(ve.orig_exc, LikeSyntaxError):
        runtime_error(str(ve.orig_exc))
    else:
        raise
except UnexpectedCharacters as u:
    print(get_context(u, inp_str))
    syntax_error(f"Unknown character at line {u.line}, column {u.column}")
    # print(u.get_context(inp_str))
except UnexpectedInput as u:
    print(get_context(u, inp_str))
    syntax_error(f"at line {u.line}, column {u.column}")
    # print(u.get_context(inp_str))
