def removeColors(string):
    if "\x1b" in string:
        posibleColors = ["\x1b[33m", "\x1b[1m", "\x1b[0m"]
        for color in posibleColors:
            string = string.replace(color, "")

    return string


def _errorRunValidator(error):
    m = MessageControl()

    if error.find("not a git repository") != -1:
        m.log("notGitRepository")
    elif error.find("did not match any files") != 1:
        m.log("notafile-error")
    else:
        m.log("unknown-error")


def run(command=[]):
    from subprocess import Popen, PIPE

    process = Popen(command, stdout=PIPE, stderr=PIPE, universal_newlines=True)

    output, error = process.communicate()

    if process.returncode != 0:
        _errorRunValidator(error)
        exit()

    return output


def checkRoute(keyword, outsideKeys, outsideAliases):
    childKeys = outsideKeys["child_keys"] if "child_keys" in outsideKeys else []
    childAliases = (
        outsideAliases["child_aliases"] if "child_aliases" in outsideAliases else []
    )

    for entityId in childKeys:
        posibleRoutes = childKeys[entityId] + childAliases[entityId]

        if keyword in posibleRoutes:
            return entityId

    return "DEFAULT"


def checkPixShortcut(keyword, outsideKeys, outsideAliases):
    for entityId in outsideKeys:
        keys = outsideKeys[entityId]["keys"]
        aliases = outsideAliases[entityId]["aliases"]
        posibleRoutes = keys + aliases

        if keyword in posibleRoutes:
            return entityId

    return False


class MessageControl:
    def __init__(self):
        from pathlib import Path
        from json import loads
        from Pix.Data.Theme import THEME, RESET

        self.THEME = THEME
        self.RESET = RESET

        filePath = Path(__file__).parent.absolute()
        filePath = str(filePath)[:-11] + "/Configuration/Messages.json"

        with open(filePath, "r") as file:
            self.messages = loads(file.read())["messages"]

    def getMessage(self, messageId, params={}):
        return str(self.messages[messageId]).format(**self.THEME, **params) + self.RESET

    def log(self, messageId, params={}):
        return print(self.getMessage(messageId, params))
