import pygments
from pygments.lexers import PythonLexer
from pygments.token import *


class RemoveComments:
    """
    Comment remover, removes comments and docstrings
    :param remove_comments: Pass this argument to enable
    """

    priority = 0xFFFFFFFFFFFFFFFF  # Priority must be the highest

    def __init__(self, **options):
        self.options = options

    def __call__(self, code):
        if "remove_comments" not in self.options:
            return code
        result = ""
        for toktype, tokval in pygments.lex(code, PythonLexer()):
            if not is_token_subtype(toktype, Token.Comment) and not is_token_subtype(
                toktype, String.Doc
            ):
                if is_token_subtype(toktype, Token.String) and tokval == "\n":
                    result += "\\n"
                    continue
                result += tokval
        return result


__all__ = ["RemoveComments"]
