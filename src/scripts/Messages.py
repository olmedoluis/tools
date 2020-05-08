from Theme import THEME


def themeUp(string):
    return string.format(**THEME).replace("$", "{}") + THEME["reset"]


MESSAGES = {
    "added-title": "\n {}\n".format(themeUp("{normal}Added files:")),
    "branch": " {} {}".format(themeUp("{normal}⚲ Branch:"), themeUp("{keyword}$")),
    "change": "\t{}".format(themeUp("{success}$")),
    "clean": "\n {}\n {}".format(themeUp("{normal}⚑ Congratulations!"), themeUp("{success}⚑ You are clean!")),
    "deleted-title": "\n {}\n".format(themeUp("{normal}Deleted files:")),
    "modified-title": "\n {}\n".format(themeUp("{normal}Modified files:")),
    "renamed-title": "\n {}\n".format(themeUp("{normal}Renamed files:")),
    "untracked-title": "\n {}\n".format(themeUp("{normal}Untracked files:")),
    "deleted": "\t{}".format(themeUp("{deleted}✝ $")),
    "modified": "\t{}".format(themeUp("{modified}☢ $")),
    "renamed": "\t{}".format(themeUp("{renamed}✦ $")),
    "untracked": "\t{}".format(themeUp("{untracked}✱ $")),
    "added": "\t{}".format(themeUp("{added}✚ $")),
}
