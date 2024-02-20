import random

import pygments
from pygments.lexers import PythonLexer
from pygments.token import *
from random import *

randbytes = lambda x: bytes(randint(0, 255) for i in range(x))


class StringOBF:
    """
    String obfuscation: merge all strings into one large bytes and replace with slices
    :param string_obf: Pass this argument to enable
    :param random_strings: Add random strings in the strings
    :param encrypt: Encryption method: 'base64' for base64, 'base64-lzma' for base64+lzma
    """

    priority = 5

    def __init__(self, **options):
        self.options = options

    def __call__(self, code):
        if "string_obf" not in self.options:
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
        code += "\n"
        affix = ""
        string = ""
        strings = []
        pos = 0
        startpos = -1
        fstring_bracket = False
        for toktype, tokval in pygments.lex(code, PythonLexer()):
            if toktype == String.Interpol:
                fstring_bracket = not fstring_bracket
                string += tokval
            elif fstring_bracket:
                string += tokval
            elif toktype == String.Affix:
                affix = tokval
                if startpos == -1:
                    startpos = pos
            elif is_token_subtype(toktype, String):
                if startpos == -1:
                    startpos = pos
                string += tokval
            else:
                if startpos != -1:
                    strings.append((affix, string, startpos, pos))
                    affix, string, startpos = "", "", -1
            pos += len(tokval)
        replacements = []
        stringtable = b""
        for af, s, st, ed in strings:
            result = "$"
            raw_af = af
            notbytes = False
            if "b" not in af:
                result += ".decode()"
                notbytes = True
            if "f" in af:
                result = "eval(chr(102)+repr(" + result + "))"
                raw_af = raw_af.replace("f", "")
            if notbytes:
                s2 = eval(raw_af + s).encode()
            else:
                s2 = eval(raw_af + s)
            replacements.append((s2, result, st, ed))
        slices = []
        for s, fmt, st, ed in replacements:
            if "random_strings" in self.options:
                stringtable += randbytes(randint(1, 20))
            slices.append((len(stringtable), len(stringtable) + len(s)))
            stringtable += s
        if "encrypt" not in self.options:
            res = "_s={}\n".format(repr(stringtable))
        elif self.options["encrypt"] == "base64":
            import base64

            res = "import base64\n_s=base64.b64decode({})\n".format(
                repr(base64.b64encode(stringtable))
            )
        elif self.options["encrypt"] == "base64-lzma":
            import base64, lzma

            res = (
                "import base64,lzma\n_s=lzma.decompress(base64.b64decode({}))\n".format(
                    repr(base64.b64encode(lzma.compress(stringtable)))
                )
            )
        p, P = 0, 0
        while p < len(code):
            if P < len(replacements) and p == replacements[P][2]:
                res += replacements[P][1].replace(
                    "$", "_s[{}:{}]".format(slices[P][0], slices[P][1])
                )
                p = replacements[P][3]
                P += 1
            else:
                res += code[p]
                p += 1
        return res


__all__ = ["StringOBF"]
