def remove(filePaths=[], shouldVerify=True):
    from .Prompts import multiSelect
    from .Helpers import run, removeColors, MessageControl
    from .Status import getStatus, searchInStatus
    from Configuration.Theme import INPUT_THEME, INPUT_ICONS

    m = MessageControl()
    status = getStatus()

    specificFiles = filePaths if filePaths else []
    if len(filePaths) != 0 and shouldVerify:
        specificFiles = searchInStatus(filePaths, status, included_files=["added"])

    if len(specificFiles) == 1 or not shouldVerify:
        run(["git", "reset"] + specificFiles)
        return m.log("remove-success")

    options = status["added"] if "added" in status else []
    options = specificFiles if len(specificFiles) != 0 else options

    if len(options) == 0:
        return m.log("error-remove-files_not_found")

    print()
    answers = multiSelect(
        title=m.getMessage("remove-title"),
        finalTitle=m.getMessage("file-selection-finaltitle"),
        errorMessage=m.getMessage("error-files_selected_not_found"),
        options=options,
        colors=INPUT_THEME["REMOVE_SELECTION"],
        icons=INPUT_ICONS,
    )

    if len(answers) == 0:
        return m.log("error-files_selected_not_found")

    choices = []
    for answer in answers:
        choices.append(removeColors(answer))

    run(["git", "reset"] + choices)
    m.log("remove-success")


def removeAll(fileSearch):
    from .Helpers import run, removeColors, MessageControl
    from .Status import getStatus, searchInStatus

    m = MessageControl()
    status = getStatus()

    if len(fileSearch) > 0:
        matches = searchInStatus(fileSearch, status, included_files=["added"])

        return (
            m.log("error-file_match_not_found")
            if len(matches) == 0
            else remove(matches, False)
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
        m.log("error-remove-files_not_found")


def Router(router, subroute):
    if subroute == "REMOVE_ALL":
        removeAll(router.left_keys[1:])
    if subroute == "DEFAULT":
        remove(router.left_keys)
