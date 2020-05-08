from Theme import THEME


def themeUp(string):
    return string.format(**THEME).replace("$", "{}") + THEME["reset"]


MESSAGES = {
    "added-title": "\n {}\n".format(themeUp("{normal}Added files:")),
    "added": "\t{}".format(themeUp("{added}✚ $")),
    "branch": " {} {}".format(themeUp("{normal}⚲ Branch:"), themeUp("{keyword}$")),
    "change": "\t{}".format(themeUp("{success}$")),
    "clean": "\n {}\n {}".format(themeUp("{normal}⚑ Congratulations!"), themeUp("{success}⚑ You are clean!")),
    "deleted-title": "\n {}\n".format(themeUp("{normal}Deleted files:")),
    "deleted": "\t{}".format(themeUp("{deleted}✝ $")),
    "modified-title": "\n {}\n".format(themeUp("{normal}Modified files:")),
    "modified": "\t{}".format(themeUp("{modified}☢ $")),
    "renamed-modify": "{}".format(themeUp("$/{modified}$")),
    "renamed-title": "\n {}\n".format(themeUp("{normal}Renamed files:")),
    "renamed": "\t{}".format(themeUp("{renamed}✦ $")),
    "untracked-title": "\n {}\n".format(themeUp("{normal}Untracked files:")),
    "untracked": "\t{}".format(themeUp("{untracked}✱ $")),
}
