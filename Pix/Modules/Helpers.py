def removeColors(string):
    if "\x1b" in string:
        posibleColors = ["\x1b[33m", "\x1b[1m", "\x1b[0m"]
        for color in posibleColors:
            string = string.replace(color, "")

    return string


def run(validator, command=[]):
    from subprocess import Popen, PIPE

    process = Popen(command, stdout=PIPE, stderr=PIPE, universal_newlines=True)

    output, error = process.communicate()

    if process.returncode != 0:
        validator(error)
        exit()

    return output


def checkRoute(keyword, outsideKeys, outsideAliases):
    childKeys = outsideKeys["child_keys"] if "child_keys" in outsideKeys else []
    childAliases = outsideAliases["child_aliases"] if "child_aliases" in outsideAliases else []

    
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
