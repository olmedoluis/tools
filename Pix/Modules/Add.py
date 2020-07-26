from .Helpers import run, removeColors, MessageControl
from .Status import getStatus, searchInStatus


def add(filePaths=[], shouldVerify=True):
    from .Prompts import multiSelect
    from Configuration.Theme import INPUT_THEME, INPUT_ICONS

    m = MessageControl()
    status = getStatus()

    specificFiles = filePaths if filePaths else []
    if len(filePaths) != 0 and shouldVerify:
        specificFiles = searchInStatus(
            filePaths, status, excludedFiles=["branch", "added"]
        )

    if len(specificFiles) == 1 or not shouldVerify:
        run(["git", "add"] + specificFiles)
        return m.log("add-success")

    options = specificFiles
    if len(specificFiles) == 0:
        for statusId in status:
            statusContent = status[statusId]
            if statusId == "branch" or statusId == "added":
                continue

            options = options + statusContent

    if len(options) == 0:
        return m.log("add-nofiles-error")

    print()
    answers = multiSelect(
        title=m.getMessage("add-adition-title"),
        finalTitle=m.getMessage("file-selection-finaltitle"),
        options=options,
        colors=INPUT_THEME["ADD_SELECTION"],
        icons=INPUT_ICONS,
    )

    if answers == "UNKNOWN_ERROR":
        return m.log("unknown-error")
    if len(answers) == 0:
        return m.log("error-nofileschoosen")

    choices = []
    for answer in answers:
        choices.append(removeColors(answer))

    run(["git", "add"] + choices)
    m.log("add-success")


def addAll(fileSearch):
    m = MessageControl()
    status = getStatus()

    if len(fileSearch) > 0:
        matches = searchInStatus(fileSearch, status, excludedFiles=["branch", "added"])

        return (
            m.log("error-nomatchfile")
            if len(matches) == 0
            else add(matches, shouldVerify=False)
        )

    hasFilesToAdd = False
    for statusId in status:
        if statusId == "branch" or statusId == "added":
            continue

        hasFilesToAdd = True
        break

    if hasFilesToAdd:
        run(["git", "add", "."])
        m.log("add-all-success")
    else:
        m.log("add-all-nofiles")


def Router(router, subroute):
    if subroute == "ADD_ALL":
        addAll(router.leftKeys[1:])
    if subroute == "DEFAULT":
        add(router.leftKeys)
