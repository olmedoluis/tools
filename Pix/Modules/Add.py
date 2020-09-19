def add(filePaths=[], shouldVerify=True, messages=""):
    from .Prompts import multiSelect
    from .Helpers import run, removeColors, MessageControl
    from .Status import getStatus, searchInStatus
    from Configuration.Theme import INPUT_THEME, INPUT_ICONS

    m = MessageControl() if messages == "" else messages
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
        return m.log("error-add-files_not_found")

    print()
    answers = multiSelect(
        title=m.getMessage("add-title"),
        finalTitle=m.getMessage("file-selection-finaltitle"),
        errorMessage=m.getMessage("error-files_selected_not_found"),
        options=options,
        colors=INPUT_THEME["ADD_SELECTION"],
        icons=INPUT_ICONS,
    )

    if len(answers) == 0:
        return m.log("error-files_selected_not_found")

    choices = []
    for answer in answers:
        choices.append(removeColors(answer))

    run(["git", "add"] + choices)
    m.log("add-success")


def addAll(fileSearch):
    from .Helpers import run, MessageControl
    from .Status import getStatus, searchInStatus

    m = MessageControl()
    status = getStatus()

    if len(fileSearch) > 0:
        matches = searchInStatus(fileSearch, status, excludedFiles=["branch", "added"])

        return (
            m.log("error-file_match_not_found")
            if len(matches) == 0
            else add(matches, shouldVerify=False, messages=m)
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
        m.log("error-add-files_not_found")


def Router(router, subroute):
    if subroute == "ADD_ALL":
        addAll(router.left_keys[1:])
    if subroute == "DEFAULT":
        add(router.left_keys)
