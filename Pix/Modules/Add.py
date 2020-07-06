from .Helpers import run, removeColors
from .Status import getStatus, searchInStatus
from .Inputs import prompts


def add(filePaths=[], shouldVerify=True):
    status = getStatus()
    inputs = prompts()

    specificFiles = []
    if len(filePaths) != 0 and shouldVerify:
        specificFiles = searchInStatus(
            filePaths, status, excludedFiles=["branch", "added"]
        )

    if len(specificFiles) == 1:
        run(["git", "add"] + specificFiles)
        return print(messages["remove-success"])

    options = specificFiles
    if len(specificFiles) == 0:
        for statusId in status:
            statusContent = status[statusId]
            if statusId == "branch" or statusId == "added":
                continue

            options = options + statusContent

    if len(options) == 0:
        return print(messages["add-nofiles-error"])

    print()
    answers = inputs.multiSelect(
        title=messages["add-adition-title"],
        finalTitle=messages["file-selection-finaltitle"],
        options=options,
    )

    if answers == "UNKNOWN_ERROR":
        return print(messages["unknown-error"])
    if len(answers) == 0:
        return print(messages["add-nofileschoosen-error"])

    choices = []
    for answer in answers:
        choices.append(removeColors(answer))

    run(["git", "add"] + choices)
    print(messages["add-success"])


def addAll(fileSearch):
    status = getStatus()

    if len(fileSearch) > 0:
        matches = searchInStatus(fileSearch, status, excludedFiles=["branch", "added"])

        return (
            print(messages["error-nomatchfile"])
            if len(matches) == 0
            else add(matches, false)
        )

    hasFilesToAdd = False
    for statusId in status:
        if statusId == "branch" or statusId == "added":
            continue

        hasFilesToAdd = True
        break

    if hasFilesToAdd:
        run(["git", "add", "."])
        print(messages["add-all-success"])
    else:
        print(messages["add-all-nofiles"])


def setUp(outsideMessages):
    global messages
    messages = outsideMessages


def Router(router, subroute):
    setUp(router.messages)

    if subroute == "ADD_ALL":
        addAll(router.leftKeys[1:])
    if subroute == "DEFAULT":
        add(router.leftKeys)
