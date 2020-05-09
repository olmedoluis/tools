def getTheme():
    modifies = ["reset", "bold", "dim",
                "underscore", "blink", "reverse", "hidden"]
    fonts = ["black", "red", "green", "yellow",
             "blue", "magenta", "cyan", "white"]

    def mod(modify):
        code = modifies.index(modify) + 0
        return f"\x1b[{code}m"

    def font_low(color):
        code = fonts.index(color) + 30
        return f"\x1b[{code}m"

    def font_high(color):
        code = fonts.index(color) + 90
        return f"\x1b[{code}m"

    return {
        "normal": mod("bold") + font_high("white"),
        "success": mod("bold") + font_high("green"),
        "keyword": mod("bold") + font_high("magenta"),
        "added": mod("bold") + font_high("green"),
        "modified": mod("bold") + font_low("yellow"),
        "deleted": mod("bold") + font_high("red"),
        "untracked": mod("bold") + font_high("blue"),
        "renamed": mod("bold") + font_low("red"),
        "error": mod("bold") + font_high("red"),
        "reset": mod("reset"),
    }
