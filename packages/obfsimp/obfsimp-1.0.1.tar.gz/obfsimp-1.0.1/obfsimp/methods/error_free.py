class ErrorFree:
    """
    Disable errors
    :param error_free: Pass this argument to enable
    """

    priority = 0

    def __init__(self, **options):
        self.options = options

    def __call__(self, code):
        if "error_free" not in self.options:
            return code
        s = code.split("\n")
        t = ["try:"]
        for i in s:
            t.append("    " + i)
        t.append("except:\n    pass")
        return "\n".join(t)


__all__ = ["ErrorFree"]
