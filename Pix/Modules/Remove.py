from .Helpers import run, removeColors, MessageControl
from .Status import getStatus, searchInStatus


def remove(filePaths=[], shouldVerify=True):
    from .Prompts import multiSelect
    from Configuration.Theme import INPUT_THEME, INPUT_ICONS

    m = MessageControl()
    status = getStatus()

    specificFiles = filePaths if filePaths else []
    if len(filePaths) != 0 and shouldVerify:
        specificFiles = searchInStatus(filePaths, status, includedFiles=["added"])

    if len(specificFiles) == 1 or not shouldVerify:
        run(["git", "reset"] + specificFiles)
        return m.log("remove-success")

    options = status["added"] if "added" in status else []
    options = specificFiles if len(specificFiles) != 0 else options

    if len(options) == 0:
        return m.log("remove-nofiles-error")

    print()
    answers = multiSelect(
        title=m.getMessage("remove-removing-title"),
        finalTitle=m.getMessage("file-selection-finaltitle"),
        options=options,
        colors=INPUT_THEME["REMOVE_SELECTION"],
        icons=INPUT_ICONS,
    )

    if answers == "UNKNOWN_ERROR":
        return m.log("unknown-error")
    if len(answers) == 0:
        return m.log("remove-nofileschoosen-error")

    choices = []
    for answer in answers:
        choices.append(removeColors(answer))

    run(["git", "reset"] + choices)
    m.log("remove-success")


def removeAll(fileSearch):
    m = MessageControl()
    status = getStatus()

    if len(fileSearch) > 0:
        matches = searchInStatus(fileSearch, status, includedFiles=["added"])

        return (
            m.log("error-nomatchfile") if len(matches) == 0 else remove(matches, False)
        )

    hasFilesToRemove = False
    for statusId in status:
        if statusId != "added":
            continue

        hasFilesToRemove = True
        break

    if hasFilesToRemove:
        run(["git", "reset", "."])
        m.log("remove-all-success")
    else:
        m.log("remove-all-nofiles")


def Router(router, subroute):
    if subroute == "REMOVE_ALL":
        removeAll(router.leftKeys[1:])
    if subroute == "DEFAULT":
        remove(router.leftKeys)
