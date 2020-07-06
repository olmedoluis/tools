from .Helpers import run, removeColors
from .Status import getStatus
from pathlib import Path as isFile
from .Inputs import prompts


def remove(filePaths=[]):
    specificFiles = []
    for filePath in filePaths:
        if not isFile(filePath):
            break

        specificFiles.append(filePath)

    if len(specificFiles) > 0:
        run(["git", "reset", "HEAD"] + specificFiles)
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

    run(["git", "reset", "HEAD"] + choices)
    print(messages["remove-success"])


def removeAll(fileSearch):
    status = getStatus()

    if len(fileSearch) > 0:
        matches = []

        for statusId in status:
            if statusId != "added":
                continue

            changes = status[statusId]

            for change in changes:
                for file in fileSearch:
                    if file.lower() in change.lower():
                        matches.append(change)

        return print(messages["error-nomatchfile"]) if len(matches) == 0 else remove(matches)

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
