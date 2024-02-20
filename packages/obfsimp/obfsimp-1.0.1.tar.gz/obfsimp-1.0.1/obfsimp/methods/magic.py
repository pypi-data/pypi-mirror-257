import warnings


def getint1(x):
    one = "__name__.__len__().__bool__().__int__()"
    one += (".__add__(" + one + ")") * (x - 1)
    return one


def getint2(x):
    one = "__name__.__len__().__bool__().__int__()"
    two = one + ".__add__(" + one + ")"
    if x == 1:
        return one
    if x == 2:
        return two
    return (
        getint2(x >> 1) + ".__mul__(" + two + ")" + (".__add__(" + one + ")") * (x & 1)
    )


def getint(x):
    g1, g2 = getint1(x), getint2(x)
    if len(g1) < len(g2):
        return g1
    return g2


def getchar(x):
    two = getint(2)
    c = "__name__.__class__.__call__.__name__.__getitem__(" + two + ")"
    h = "__name__.__hash__.__name__.__getitem__(" + two + ")"
    r = "__name__.__rmul__.__name__.__getitem__(" + two + ")"
    cchr = (
        "__builtins__.__getattribute__(" + c + ".__add__(" + h + ").__add__(" + r + "))"
    )
    return cchr + ".__call__(" + x + ")"


def geteval(x):
    one, three, four = getint(1), getint(3), getint(4)
    e = "__name__.__class__.__class__.__name__.__getitem__(" + three + ")"
    v = (
        "__name__.__class__.__call__().__len__().__invert__.__name__.__getitem__("
        + four
        + ")"
    )
    a = (
        "__name__.__class__.__call__().__len__().__truediv__("
        + one
        + ").__class__.__name__.__getitem__("
        + three
        + ")"
    )
    l = (
        "__name__.__class__.__call__().__len__().__truediv__("
        + one
        + ").__class__.__name__.__getitem__("
        + one
        + ")"
    )
    eeval = (
        "__builtins__.__getattribute__("
        + e
        + ".__add__("
        + v
        + ").__add__("
        + a
        + ").__add__("
        + l
        + "))"
    )
    return eeval + ".__call__(" + x + ")"


def magicify(code):
    if not code:
        return ""
    code = "exec(" + repr(code) + ")"
    res = getchar(getint(ord(code[0])))
    for i, j in enumerate(code):
        if i == 0:
            continue
        res = res + ".__add__(" + getchar(getint(ord(j))) + ")"
    return geteval(res)


class Magic:
    """
    Converts normal Python code into code that only uses magic functions (inspired by this
    article: https://esolangs.org/wiki/Python_is_Magic).
    This is slow when processing large programs, and will largely increase the program size, so it is only supposed to
    be used for small programs.
    If the generated program is larger than 10KiB, you are warned.
    """

    priority = -1

    def __init__(self, **options):
        self.options = options

    def __call__(self, code):
        if "magic" not in self.options:
            return code
        result = magicify(code)
        if len(result) > 10240:
            warnings.warn("The converted program is larger than 10KiB")
        return result


__all__ = ["Magic"]
