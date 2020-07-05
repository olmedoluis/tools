from Pix.Data.Messages import _font_high, _font_low, _mod

_theme = {
    "normal": _mod("bold") + _font_high("white"),
    "success": _mod("bold") + _font_high("green"),
    "keyword": _mod("bold") + _font_high("magenta"),
    "added": _mod("bold") + _font_high("green"),
    "modified": _mod("bold") + _font_low("yellow"),
    "deleted": _mod("bold") + _font_high("red"),
    "untracked": _mod("bold") + _font_high("blue"),
    "renamed": _mod("bold") + _font_low("red"),
    "error": _mod("bold") + _font_high("red"),
    "reset": _mod("reset"),
    "change": _font_low("yellow"),
    "dim": _mod("dim")
}

def _themeUp(string):
    return string.format(**_theme).replace("$", "{}") + _theme["reset"]

messages = {
    "add-adition-title": "{}".format(_themeUp("{normal}Select files to add:")),
    "add-all-nofiles": "\n {}\n".format(_themeUp("{error}✖ There is no file to add")),
    "add-all-success": "\n {}\n".format(_themeUp("{success}⚑ All files has been added")),
    "add-nofiles-error": "\n {}\n".format(_themeUp("{error}✖ There is no files to add")),
    "add-nofileschoosen-error": "\n {}\n".format(_themeUp("{error}✖ No files has been choosen")),
    "add-success": "\n {}\n".format(_themeUp("{success}⚑ Selected files has been added")),
    "added-title": "\n {}\n".format(_themeUp("{normal}Added files:")),
    "added": "\t{}".format(_themeUp("{added}✚ $")),
    "branch-about-title": "{}".format(_themeUp("{normal}What is this branch about?")),
    "branch-id-title": "{}".format(_themeUp("{normal}What is the ticket id?")),
    "branch-selection-title": "{}".format(_themeUp("{normal}Select a branch to switch:")),
    "branch-shouldswitch": "{}".format(_themeUp("{normal}Do you want to switch?")),
    "branch-success": "\n {}\n".format(_themeUp("{success}⚑ You have switched to {keyword}$")),
    "branch-switchsuccess": "\n {}\n".format(_themeUp("{success}⚑ You are on {keyword}${success} now")),
    "branch-type-title": "{}".format(_themeUp("{normal}What type of branch is this?")),
    "branch": " {} {}".format(_themeUp("{normal}⚲ Branch:"), _themeUp("{keyword}$")),
    "change": "\t{}".format(_themeUp("{success}$")),
    "clean": "\n {}\n {}".format(_themeUp("{normal}⚑ Congratulations!"), _themeUp("{success}⚑ You are clean!")),
    "commit-about-title": "{}".format(_themeUp("{normal}What is this commit about?")),
    "commit-cancel": "\n {}\n".format(_themeUp("{error}✖ You have cancelled commiting")),
    "commit-nofiles": "\n {}\n".format(_themeUp("{error}✖ There is no files to commit")),
    "commit-scope-title": "{}".format(_themeUp("{normal}What is the scope?")),
    "commit-success": "\n {}\n".format(_themeUp("{success}⚑ You have commited added files")),
    "commit-type-title": "{}".format(_themeUp("{normal}What type of commit is this?")),
    "confirmation": "{}".format(_themeUp("{normal}Are you sure? y/n")),
    "deleted-title": "\n {}\n".format(_themeUp("{normal}Deleted files:")),
    "deleted": "\t{}".format(_themeUp("{deleted}✝ $")),
    "error-empty": "\n {}\n".format(_themeUp("{error}✖ You left a field empty")),
    "error-haschanges": "\n {}\n".format(_themeUp("{error}✖ You still have uncommited changes")),
    "error-inputcancel": "\n {}\n".format(_themeUp("{error}✖ You have cancelled the form")),
    "error-nobranches": "\n {}\n".format(_themeUp("{error}✖ You do not have any branches yet")),
    "error-nomatchbranch": "\n {}\n".format(_themeUp("{error}✖ There is no branch with {keyword}$")),
    "error-nostashes": "\n {}\n".format(_themeUp("{error}✖ You do not have any stashed files yet")),
    "error-samebranch": "\n {}\n".format(_themeUp("{error}✖ You already are on {keyword}$")),
    "error-stash-addedfiles": "\n {}\n".format(_themeUp("{error}✖ You only can stash added files")),
    "file-selection-finaltitle": "{}".format(_themeUp("{normal}Files selected:")),
    "modified-title": "\n {}\n".format(_themeUp("{normal}Modified files:")),
    "modified": "\t{}".format(_themeUp("{modified}☢ $")),
    "notafile-error": "\n {}\n".format(_themeUp("{error}✖ One of the files you input is not a file")),
    "notGitRepository": "\n {}\n".format(_themeUp("{error}✖ This is not a supported repository")),
    "preview": "\n\t{}\n".format(_themeUp("{normal}Preview: {keyword}$")),
    "remove-all-nofiles": "\n {}\n".format(_themeUp("{error}✖ There is no file to remove")),
    "remove-all-success": "\n {}\n".format(_themeUp("{success}⚑ All files has been removed")),
    "remove-nofiles-error": "\n {}\n".format(_themeUp("{error}✖ There is no files to remove")),
    "remove-nofileschoosen-error": "\n {}\n".format(_themeUp("{error}✖ No files has been choosen")),
    "remove-removing-title": "{}".format(_themeUp("{normal}Select files to remove:")),
    "remove-success": "\n {}\n".format(_themeUp("{success}⚑ Selected files has been removed")),
    "renamed-modify": "{}".format(_themeUp("${change}$")),
    "renamed-title": "\n {}\n".format(_themeUp("{normal}Renamed files:")),
    "renamed": "\t{}".format(_themeUp("{renamed}✦ $")),
    "scape-error": "\n {}\n".format(_themeUp("{error}✖ You have exit pix")),
    "stash-back-success": "\n {}\n".format(_themeUp("{success}⚑ You bringed {keyword}$ {success}back")),
    "stash-in-success": "\n {}\n".format(_themeUp("{success}⚑ You have stashed added files")),
    "stash-in-title": "{}".format(_themeUp("{normal}A name for what you are trying to stash?")),
    "stash-listitem": "{}".format(_themeUp("$ - $ {dim}$")),
    "unknown-error": "\n {}\n".format(_themeUp("{error}✖ Unknown error, something went wrong")),
    "unknownRoute": "\n {}\n".format(_themeUp("{error}✖ Command not found: {success}${error}$")),
    "untracked-title": "\n {}\n".format(_themeUp("{normal}Untracked files:")),
    "untracked": "\t{}".format(_themeUp("{untracked}✱ $")),
}
