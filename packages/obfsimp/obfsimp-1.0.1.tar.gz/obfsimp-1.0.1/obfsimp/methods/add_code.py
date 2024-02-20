from random import *
import pygments
from pygments.lexers import PythonLexer
from pygments.token import *

hex_cache = set()


def hex_renamer():
    r = "_" + "0x%x" % (randint(0x100000, 0xFFFFFF))
    while r in hex_cache:
        r = "_" + "0x%x" % (randint(0x100000, 0xFFFFFF))
    return r


underscore_cache = (
    1  # Avoid using one underline as variable names because it is usable in Python
)


def underscore_renamer():
    global underscore_cache
    underscore_cache += 1
    return "_" * underscore_cache


char_cache = set()


def character_renamer():
    r = "".join(
        choice("qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM")
        for i in range(20)
    )
    while r in char_cache:
        r = "".join(
            choice("qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM")
            for i in range(20)
        )
    return r


ozero_cache = set()


def ozero_renamer():
    r = "O" + "".join(choice("0O") for i in range(19))
    while r in ozero_cache:
        r = "O" + "".join(choice("0O") for i in range(19))
    return r


lone_cache = set()


def lone_renamer():
    r = "l" + "".join(choice("1l") for i in range(19))
    while r in lone_cache:
        r = "l" + "".join(choice("1l") for i in range(19))
    return r


def getzero():
    op = randint(0, 4)
    if op == 0:
        t = randint(0, 0xFFFFFFFFFFFFFFFF)
        return "{}+(-{})".format(t, t)
    if op == 1:
        t = randint(0, 0xFFFFFFFFFFFFFFFF)
        return "{}-{}".format(t, t)
    if op == 2:
        return "0*{}".format(randint(0, 0xFFFFFFFFFFFFFFFF))
    return "0//{}".format(randint(1, 0xFFFFFFFFFFFFFFFF))


def rndcode(depth, renamer):
    z = []
    if depth == 9:
        codetype = 0
    else:
        codetype = randint(int(depth < 3), 3)
    for i in range(randint(1, 10)):
        if randint(0, 1):
            z.append(("pass", depth))
        else:
            z.append(("var", renamer(), randint(0, 0xFFFFFFFFFFFFFFFF), depth))
    if depth >= 10:
        return z + []
    if codetype == 0:
        return z + []
    if codetype == 1:
        y = [("if", getzero(), depth)]
        y += rndcode(depth + 1, renamer)
        return z + y
    y = [("while", getzero(), depth)]
    y += rndcode(depth + 1, renamer)
    return z + y


def compose_code(c):
    res = ""
    for i in c:
        res += "    " * i[-1]
        if i[0] == "var":
            res += "{}={}".format(i[1], i[2])
        elif i[0] == "pass":
            res += "pass"
        elif i[0] == "if":
            res += "if {}:".format(i[1])
        else:
            res += "while {}:".format(i[1])
        res += "\n"
    return res.strip()


class AddCode:
    """
    Insert random code that does nothing
    :param add_code: Pass this argument to enable
    :param renamer: The renamer to use, 'hex' for hex renamer, 'char' for random letter renamer, 'o0' for O and 0
    renamer, 'underscore' for underscore renamer and 'l1' for l and 1 renamer, hex renamer is used if not passed.
    :param code_amount: Amount of code to insert, default is 10
    """

    priority = 2

    def __init__(self, **options):
        self.options = options

    def __call__(self, code):
        global underscore_cache, hex_cache, char_cache, ozero_cache, lone_cache
        underscore_cache, ozero_cache, lone_cache, char_cache, hex_cache = (
            1,
            set(),
            set(),
            set(),
            set(),
        )
        if "add_code" not in self.options:
            return code
        result = ""
        open_bracket = 0
        for toktype, tokval in pygments.lex(code, PythonLexer()):
            if is_token_subtype(toktype, Token.String) and tokval == "\n":
                result += "\\n"
                continue
            else:
                open_bracket += (
                    tokval.count("(")
                    + tokval.count("[")
                    + tokval.count("{")
                    - tokval.count("}")
                    - tokval.count("]")
                    - tokval.count(")")
                )
                if tokval == "\n" and open_bracket:
                    continue
            result += tokval
        code = result
        if "renamer" not in self.options:
            renamer = hex_renamer
        else:
            renamer = {
                "hex": hex_renamer,
                "char": character_renamer,
                "o0": ozero_renamer,
                "underscore": underscore_renamer,
                "l1": lone_renamer,
            }[self.options["renamer"]]
        breakdown = code.split("\n")
        if "code_amount" in self.options:
            num = self.options["code_amount"]
        else:
            num = 10
        breakdown = [""] + breakdown
        for i in range(num):
            pos = randint(0, len(breakdown) - 1)
            indent = ""
            if pos == len(breakdown) - 1:
                indent = ""
            else:
                c = breakdown[pos + 1]
                for j in c:
                    if j.isspace():
                        indent += j
                    else:
                        break
            random_code = compose_code(rndcode(0, renamer))
            for j in reversed(random_code.split("\n")):
                breakdown.insert(pos + 1, indent + j)
        return "\n".join(breakdown).strip()


__all__ = ["AddCode"]
