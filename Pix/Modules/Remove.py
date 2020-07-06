from .Helpers import run, removeColors
from .Status import getStatus, searchInStatus
from pathlib import Path as isFile
from .Inputs import prompts


def remove(filePaths=[], shouldVerify=True):
    status = getStatus()
    inputs = prompts()

    specificFiles = []
    if len(filePaths) != 0 and shouldVerify:
        specificFiles = searchInStatus(filePaths, status, includedFiles=["added"])

    if len(specificFiles) == 1:
        run(["git", "reset", "HEAD"] + specificFiles)
        return print(messages["remove-success"])

    options = status["added"] if "added" in status else []
    options = specificFiles if len(specificFiles) != 0 else options

    if len(options) == 0:
        return print(messages["remove-nofiles-error"])

    print()
    answers = inputs.multiSelect(
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

    run(["git", "reset", "HEAD"] + choices)
    print(messages["remove-success"])


def removeAll(fileSearch):
    status = getStatus()

    if len(fileSearch) > 0:
        matches = searchInStatus(fileSearch, status, includedFiles=["added"])

        return (
            print(messages["error-nomatchfile"])
            if len(matches) == 0
            else remove(matches, false)
        )

    hasFilesToRemove = False
    for statusId in status:
        if statusId != "added":
            continue

        hasFilesToRemove = True
        break

    if hasFilesToRemove:
        run(["git", "reset", "HEAD", "."])
        print(messages["remove-all-success"])
    else:
        print(messages["remove-all-nofiles"])


def setUp(outsideMessages):
    global messages
    messages = outsideMessages


def Router(router, subroute):
    setUp(router.messages)

    if subroute == "REMOVE_ALL":
        removeAll(router.leftKeys[1:])
    if subroute == "DEFAULT":
        remove(router.leftKeys)
