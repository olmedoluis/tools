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
        "change": font_low("yellow")
    }


def getMessages():
    theme = getTheme()

    def themeUp(string):
        return string.format(**theme).replace("$", "{}") + theme["reset"]

    return {
        "add-adition-title": "{}".format(themeUp("{normal}Select files to add:")),
        "add-all-nofiles": "\n {}\n".format(themeUp("{error}✖ There is no file to add")),
        "add-all-success": "\n {}\n".format(themeUp("{success}⚑ All files has been added")),
        "add-nofiles-error": "\n {}\n".format(themeUp("{error}✖ There is no files to add")),
        "add-nofileschoosen-error": "\n {}\n".format(themeUp("{error}✖ No files has been choosen")),
        "add-success": "\n {}\n".format(themeUp("{success}⚑ Selected files has been added")),
        "branch-switchsuccess": "\n {}\n".format(themeUp("{success}⚑ You are on {keyword}${success} now")),
        "added-title": "\n {}\n".format(themeUp("{normal}Added files:")),
        "added": "\t{}".format(themeUp("{added}✚ $")),
        "branch-about-title": "{}".format(themeUp("{normal}What is this branch about?")),
        "branch-id-title": "{}".format(themeUp("{normal}What is the ticket id?")),
        "branch-selection-title": "{}".format(themeUp("{normal}Select a branch to switch:")),
        "branch-success": "\n {}\n".format(themeUp("{success}⚑ You have switched to {keyword}$")),
        "branch-type-title": "{}".format(themeUp("{normal}What type of branch is this?")),
        "branch-shouldswitch": "{}".format(themeUp("{normal}Do you want to switch?")),
        "error-inputcancel": "\n {}\n".format(themeUp("{error}✖ You have cancelled the form")),
        "branch": " {} {}".format(themeUp("{normal}⚲ Branch:"), themeUp("{keyword}$")),
        "change": "\t{}".format(themeUp("{success}$")),
        "clean": "\n {}\n {}".format(themeUp("{normal}⚑ Congratulations!"), themeUp("{success}⚑ You are clean!")),
        "commit-about-title": "{}".format(themeUp("{normal}What is this commit about?")),
        "commit-cancel": "\n {}\n".format(themeUp("{error}✖ You have cancelled commiting")),
        "confirmation": "{}".format(themeUp("{normal}Are you sure? y/n")),
        "commit-nofiles": "\n {}\n".format(themeUp("{error}✖ There is no files to commit")),
        "preview": "\n\t{}\n".format(themeUp("{normal}Preview: {keyword}$")),
        "commit-scope-title": "{}".format(themeUp("{normal}What is the scope?")),
        "commit-success": "\n {}\n".format(themeUp("{success}⚑ You have commited added files")),
        "commit-type-title": "{}".format(themeUp("{normal}What type of commit is this?")),
        "deleted-title": "\n {}\n".format(themeUp("{normal}Deleted files:")),
        "deleted": "\t{}".format(themeUp("{deleted}✝ $")),
        "error-empty": "\n {}\n".format(themeUp("{error}✖ You left a field empty")),
        "error-haschanges": "\n {}\n".format(themeUp("{error}✖ You still have uncommited changes")),
        "error-samebranch": "\n {}\n".format(themeUp("{error}✖ You already are on {keyword}$")),
        "file-selection-finaltitle": "{}".format(themeUp("{normal}Files selected:")),
        "modified-title": "\n {}\n".format(themeUp("{normal}Modified files:")),
        "modified": "\t{}".format(themeUp("{modified}☢ $")),
        "notafile-error": "\n {}\n".format(themeUp("{error}✖ One of the files you input is not a file")),
        "notGitRepository": "\n {}\n".format(themeUp("{error}✖ This is not a supported repository")),
        "remove-all-nofiles": "\n {}\n".format(themeUp("{error}✖ There is no file to remove")),
        "remove-all-success": "\n {}\n".format(themeUp("{success}⚑ All files has been removed")),
        "remove-nofiles-error": "\n {}\n".format(themeUp("{error}✖ There is no files to remove")),
        "remove-nofileschoosen-error": "\n {}\n".format(themeUp("{error}✖ No files has been choosen")),
        "remove-removing-title": "{}".format(themeUp("{normal}Select files to remove:")),
        "remove-success": "\n {}\n".format(themeUp("{success}⚑ Selected files has been removed")),
        "renamed-modify": "{}".format(themeUp("${change}$")),
        "renamed-title": "\n {}\n".format(themeUp("{normal}Renamed files:")),
        "renamed": "\t{}".format(themeUp("{renamed}✦ $")),
        "scape-error": "\n {}\n".format(themeUp("{error}✖ You have exit pix")),
        "unknown-error": "\n {}\n".format(themeUp("{error}✖ Unknown error, something went wrong")),
        "unknownRoute": "\n {}\n".format(themeUp("{error}✖ Command not found: {success}${error}$")),
        "untracked-title": "\n {}\n".format(themeUp("{normal}Untracked files:")),
        "untracked": "\t{}".format(themeUp("{untracked}✱ $")),
    }
