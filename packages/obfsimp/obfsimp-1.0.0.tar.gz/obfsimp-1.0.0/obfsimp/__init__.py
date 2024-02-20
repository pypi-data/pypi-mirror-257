"""
Obfsimp is a simple Python 3 obfuscator that is mainly used for entertainment.

Needs to be used in Python 3, and better use the Python version the same as the version you want to execute the
obfuscated program with to obfuscate.
"""
from .methods import obfuscation_methods


class Obfuscator:
    """
    Class for obfuscating Python code
    """

    def __init__(self, **options):
        """
        Initialize object
        :param options: Options for obfuscation, it is used as flags by methods
        """
        self.options = options
        self.methods = []
        for i in obfuscation_methods:
            self.methods.append(i(**self.options))
        self.methods.sort(key=lambda x: x.priority, reverse=True)

    def __call__(self, code, checksyntax=True):
        """
        Obfuscate
        :param code: Python code
        :param checksyntax: Check if the syntax is valid before obfuscation
        :return: obfuscated code
        """
        if checksyntax:
            try:
                compile(code, "", "exec")
            except SyntaxError:
                raise SyntaxError(
                    "Your code does not have a valid syntax, to silence this error, use checksyntax=False"
                )
        for i in self.methods:
            code = i(code)
        return code
