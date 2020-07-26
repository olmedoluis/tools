def removeColors(string):
    while "\u001b" in string:
        start = string.index("\u001b")
        end = string.index("m", start) + 1
        string = string[:start] + string[end:]

    return string


def _errorRunValidator(error):
    m = MessageControl()

    if error.find("not a git repository") != -1:
        m.log("notGitRepository")
    elif error.find("did not match any files") != -1:
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
        from Configuration.Theme import THEME, ICONS
        from Configuration.Messages import MESSAGES

        self.THEME = {**THEME, **ICONS}
        self.RESET = THEME["th_reset"]
        self.messages = MESSAGES

    def getMessage(self, messageId, params={}):
        return str(self.messages[messageId]).format(**self.THEME, **params) + self.RESET

    def log(self, messageId, params={}):
        return print(self.getMessage(messageId, params))
