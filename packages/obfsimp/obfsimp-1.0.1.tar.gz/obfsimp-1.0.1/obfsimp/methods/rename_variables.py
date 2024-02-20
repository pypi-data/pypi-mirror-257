import pygments
from pygments.lexers import PythonLexer
from random import randint, choice
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


is_magic = lambda x: len(x) > 4 and all((x[i] == "_") for i in [0, 1, -1, -2])


class RenameVariables:
    """
    Variable renamer, renames variables, functions, classes and decorators
    Currently doesn't support these:
    1. Names imported from modules
    2. Keyword arguments
    3. Renaming variables differently in different scopes
    4. eval() and exec() may not work correctly
    :param rename_variables: Pass this argument to enable
    :param renamer: The renamer to use, 'hex' for hex renamer, 'char' for random letter renamer, 'o0' for O and 0
    renamer, 'underscore' for underscore renamer and 'l1' for l and 1 renamer, hex renamer is used if not passed.
    :param obfuscation_list: Optional, a dictionary for names that must be renamed to exactly the corresponding value in dictionary. Usually used for names that are not
    supposed to be renamed, or names from other obfuscated files.
    :param exports: Names that are renamed but needed to be exported, it is recommended to use this with string obfuscations
    """

    priority = 4

    def __init__(self, **options):
        self.options = options

    def __call__(self, code):
        global underscore_cache, hex_cache, char_cache, ozero_cache, lone_cache
        builtins_val = [  # A list of builtin functions
            "ArithmeticError",
            "AssertionError",
            "AttributeError",
            "BaseException",
            "BlockingIOError",
            "BrokenPipeError",
            "BufferError",
            "BytesWarning",
            "ChildProcessError",
            "ConnectionAbortedError",
            "ConnectionError",
            "ConnectionRefusedError",
            "ConnectionResetError",
            "DeprecationWarning",
            "EOFError",
            "Ellipsis",
            "EnvironmentError",
            "Exception",
            "False",
            "FileExistsError",
            "FileNotFoundError",
            "FloatingPointError",
            "FutureWarning",
            "GeneratorExit",
            "IOError",
            "ImportError",
            "ImportWarning",
            "IndentationError",
            "IndexError",
            "InterruptedError",
            "IsADirectoryError",
            "KeyError",
            "KeyboardInterrupt",
            "LookupError",
            "MemoryError",
            "ModuleNotFoundError",
            "NameError",
            "None",
            "NotADirectoryError",
            "NotImplemented",
            "NotImplementedError",
            "OSError",
            "OverflowError",
            "PendingDeprecationWarning",
            "PermissionError",
            "ProcessLookupError",
            "RecursionError",
            "ReferenceError",
            "ResourceWarning",
            "RuntimeError",
            "RuntimeWarning",
            "StopAsyncIteration",
            "StopIteration",
            "SyntaxError",
            "SyntaxWarning",
            "SystemError",
            "SystemExit",
            "TabError",
            "TimeoutError",
            "True",
            "TypeError",
            "UnboundLocalError",
            "UnicodeDecodeError",
            "UnicodeEncodeError",
            "UnicodeError",
            "UnicodeTranslateError",
            "UnicodeWarning",
            "UserWarning",
            "ValueError",
            "Warning",
            "WindowsError",
            "ZeroDivisionError",
            "_",
            "__build_class__",
            "__debug__",
            "__doc__",
            "__import__",
            "__loader__",
            "__name__",
            "__package__",
            "__spec__",
            "abs",
            "all",
            "any",
            "ascii",
            "bin",
            "bool",
            "breakpoint",
            "bytearray",
            "bytes",
            "callable",
            "chr",
            "classmethod",
            "compile",
            "complex",
            "copyright",
            "credits",
            "delattr",
            "dict",
            "dir",
            "divmod",
            "enumerate",
            "eval",
            "exec",
            "exit",
            "filter",
            "float",
            "format",
            "frozenset",
            "getattr",
            "globals",
            "hasattr",
            "hash",
            "help",
            "hex",
            "id",
            "input",
            "int",
            "isinstance",
            "issubclass",
            "iter",
            "len",
            "license",
            "list",
            "locals",
            "map",
            "max",
            "memoryview",
            "min",
            "next",
            "object",
            "oct",
            "open",
            "ord",
            "pow",
            "print",
            "property",
            "quit",
            "range",
            "repr",
            "reversed",
            "round",
            "set",
            "setattr",
            "slice",
            "sorted",
            "staticmethod",
            "str",
            "sum",
            "super",
            "tuple",
            "type",
            "vars",
            "zip",
            "__builtins__",
        ]
        underscore_cache, ozero_cache, lone_cache, char_cache, hex_cache = (
            1,
            set(),
            set(),
            set(),
            set(),
        )
        if "rename_variables" not in self.options:
            return code
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
        scanned_names = {}
        obfulist = {}
        if "obfuscation_list" in self.options:
            scanned_names = self.options["obfuscation_list"]
            obfulist = self.options["obfuscation_list"]
        exports = set()
        if "exports" in self.options:
            exports = set(self.options["exports"])
        result = ""
        prev_toktype, prev_tokval = "", ""
        string_removed = ""
        for toktype, tokval in pygments.lex(code, PythonLexer()):
            if not is_token_subtype(toktype, String):
                string_removed += tokval
        modules = set()
        for i in string_removed.split("\n"):
            j = i.split()
            if len(j) >= 2:
                if j[0] in ["from", "import"]:
                    modules |= set(map(lambda x: x.strip(), j[1].split(",")))
        for toktype, tokval in pygments.lex(code, PythonLexer()):
            if (
                (
                    toktype == Token.Name
                    or toktype == Token.Name.Function
                    or toktype == Token.Name.Class
                    or toktype == Token.Name.Decorator
                    or toktype == Token.Name.Builtin.Pseudo
                )
                and (tokval not in scanned_names and (tokval not in builtins_val))
                and (
                    not (
                        prev_tokval == "."
                        and prev_toktype == Token.Operator
                        and (tokval not in scanned_names)
                    )
                )
                and (tokval not in modules)
            ):
                scanned_names[tokval] = renamer()
                if tokval[0] == "@":  # For decorators
                    scanned_names[tokval] = "@" + scanned_names[tokval]
            prev_toktype = toktype
            prev_tokval = tokval
        for toktype, tokval in pygments.lex(code, PythonLexer()):
            if (
                (
                    toktype == Token.Name
                    or toktype == Token.Name.Function
                    or toktype == Token.Name.Class
                    or toktype == Token.Name.Decorator
                    or toktype == Token.Name.Builtin.Pseudo
                )
                and (tokval in scanned_names and (tokval not in builtins_val))
                and (not is_magic(tokval))
            ):
                result += scanned_names[tokval]
            else:
                result += tokval
        for i in exports:
            if (i in scanned_names) and (i not in obfulist):
                result += (
                    "\n"
                    + '(setattr(__builtins__,"{}",{}) if not isinstance(__builtins__,dict) else __builtins__.__setitem__("{}",{}))'.format(
                        i, scanned_names[i], i, scanned_names[i]
                    )
                )
        return result


__all__ = ["RenameVariables"]
