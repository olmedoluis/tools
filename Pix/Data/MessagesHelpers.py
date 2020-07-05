_modifies = ["reset", "bold", "dim", "underscore", "blink", "reverse", "hidden"]
_fonts = ["black", "red", "green", "yellow", "blue", "magenta", "cyan", "white"]


def _mod(modify):
    code = _modifies.index(modify) + 0
    return f"\x1b[{code}m"


def _font_low(color):
    code = _fonts.index(color) + 30
    return f"\x1b[{code}m"


def _font_high(color):
    code = _fonts.index(color) + 90
    return f"\x1b[{code}m"
