from .Helpers import run, removeColors
from .Status import getStatus
from pathlib import Path as isFile
from .Inputs import prompts


def errorRunValidator(error):
    if error.find("not a git repository") != -1:
        print(messages["notGitRepository"])
    elif error.find("did not match any files") != 1:
        print(messages["notafile-error"])
    else:
        print(messages["unknown-error"])


def remove(filePaths=[]):
    specificFiles = []
    for filePath in filePaths:
        if not isFile(filePath):
            break

        specificFiles.append(filePath)

    if len(specificFiles) > 0:
        run(errorRunValidator, ["git", "reset", "HEAD"] + specificFiles)
        return print(messages["remove-success"])

    status = getStatus()

    options = status["added"] if "added" in status else []

    if len(options) == 0:
        return print(messages["remove-nofiles-error"])

    print()
    answers = prompts().multiSelect(
        title=messages["remove-removing-title"],
        finalTitle=messages["file-selection-finaltitle"],
        options=options,
        selectedColor="\x1b[31m",
    )

    if answers == "UNKNOWN_ERROR":
        return print(messages["unknown-error"])
    if len(answers) == 0:
        return print(messages["remove-nofileschoosen-error"])

    choices = []
    for answer in answers:
        choices.append(removeColors(answer))

    run(errorRunValidator, ["git", "reset", "HEAD"] + choices)
    print(messages["remove-success"])


def removeAll():
    status = getStatus()

    hasFilesToAdd = False
    for statusId in status:
        if statusId != "added":
            continue

        hasFilesToAdd = True
        break

    if hasFilesToAdd:
        run(errorRunValidator, ["git", "reset", "HEAD", "."])
        print(messages["remove-all-success"])
    else:
        print(messages["remove-all-nofiles"])


def setUp(outsideMessages):
    global messages
    messages = outsideMessages


def Router(router, subroute):
    setUp(router.messages)

    if subroute == "REMOVE_ALL":
        removeAll()
    if subroute == "DEFAULT":
        remove(router.leftKeys)
