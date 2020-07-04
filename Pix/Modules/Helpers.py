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

def checkRoute(keyword, routes):
    for entityId in routes:
        entity = routes[entityId]
        posibleRoutes = entity["keys"] + entity["alias"]

        if keyword in posibleRoutes:
            return entityId

    return "DEFAULT"


def checkPixShortcut(keyword, routes):
    for entityId in routes:
        entity = routes[entityId]
        posibleRoutes = entity["keys"] + entity["alias"]

        if keyword in posibleRoutes:
            return entityId

    return False