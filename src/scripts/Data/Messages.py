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


def getMessages():
    theme = getTheme()

    def themeUp(string):
        return string.format(**theme).replace("$", "{}") + theme["reset"]

    return {
        "added-title": "\n {}\n".format(themeUp("{normal}Added files:")),
        "added": "\t{}".format(themeUp("{added}✚ $")),
        "branch": " {} {}".format(themeUp("{normal}⚲ Branch:"), themeUp("{keyword}$")),
        "change": "\t{}".format(themeUp("{success}$")),
        "clean": "\n {}\n {}".format(themeUp("{normal}⚑ Congratulations!"), themeUp("{success}⚑ You are clean!")),
        "deleted-title": "\n {}\n".format(themeUp("{normal}Deleted files:")),
        "deleted": "\t{}".format(themeUp("{deleted}✝ $")),
        "modified-title": "\n {}\n".format(themeUp("{normal}Modified files:")),
        "modified": "\t{}".format(themeUp("{modified}☢ $")),
        "notGitRepository": "\n {}\n".format(themeUp("{error}✖ This is not a supported repository")),
        "renamed-modify": "{}".format(themeUp("$/{modified}$")),
        "renamed-title": "\n {}\n".format(themeUp("{normal}Renamed files:")),
        "renamed": "\t{}".format(themeUp("{renamed}✦ $")),
        "unknownError": "\n {}\n".format(themeUp("{error}✖ Unknown error, something went wrong")),
        "unknownRoute": "\n {}\n".format(themeUp("{error}✖ Command not found: {success}${error}$")),
        "untracked-title": "\n {}\n".format(themeUp("{normal}Untracked files:")),
        "untracked": "\t{}".format(themeUp("{untracked}✱ $")),
        "add-nofiles-error": "\n {}\n".format(themeUp("{error}✖ There is no files to add")),
        "add-nofileschoosen-error": "\n {}\n".format(themeUp("{error}✖ No files has been choosen")),
        "add-success": "\n {}\n".format(themeUp("{success}⚑ Selected files has been added")),
        "add-adition-title": "{}".format(themeUp("{normal}Select files to add:")),
        "add-adition-finaltitle": "{}".format(themeUp("{normal}Files selected:")),
    }
