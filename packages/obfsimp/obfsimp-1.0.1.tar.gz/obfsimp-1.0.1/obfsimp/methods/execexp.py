class ExecExp:
    """
    Exec expression wrapper
    :param exec: Pass this argument to enable
    :param exec_crypt: 'escape' for escape, 'base64' for base64, 'base64-lzma' for base64+lzma
    """

    priority = -2

    def __init__(self, **options):
        self.options = options

    def __call__(self, code):
        if "exec" not in self.options:
            return code
        if "exec_crypt" not in self.options:
            return "exec(" + repr(code) + ")"
        elif self.options["exec_crypt"] == "base64":
            import base64

            return (
                'exec(__import__("base64").b64decode('
                + repr(base64.b64encode(code.encode()))
                + ").decode())"
            )
        elif self.options["exec_crypt"] == "base64-lzma":
            import lzma, base64

            return (
                'exec(__import__("lzma").decompress(__import__("base64").b64decode('
                + repr(base64.b64encode(lzma.compress(code.encode())))
                + ")).decode())"
            )
        elif self.options["exec_crypt"] == "escape":
            return 'exec("' + "".join("\\u{:04x}".format(ord(i)) for i in code) + '")'


__all__ = ["ExecExp"]
