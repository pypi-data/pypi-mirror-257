"""
Obfuscation methods
"""
from .execexp import ExecExp
from .remove_comments import RemoveComments
from .rename_variables import RenameVariables
from .add_code import AddCode
from .error_free import ErrorFree
from .stringobf import StringOBF
from .magic import Magic

obfuscation_methods = [
    ExecExp,
    RemoveComments,
    RenameVariables,
    AddCode,
    ErrorFree,
    StringOBF,
    Magic,
]
