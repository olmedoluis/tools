def parseStatus(status):
    resetCommands = []

    for statusId in status:
        for change in status[statusId]:
            if statusId == "untracked":
                resetCommands.append(["rm", change])
            else:
                resetCommands.append(["git", "checkout", change])

    return resetCommands


def reset(filePaths=[], shouldVerify=True, messages=""):
    from .Prompts import multiSelect
    from .Helpers import runAll, removeColors, MessageControl
    from .Status import getStatus, searchInStatus
    from Configuration.Theme import INPUT_THEME, INPUT_ICONS

    m = MessageControl() if messages == "" else messages
    status = getStatus()

    filesForParsing = []
    specificFiles = filePaths if filePaths else []

    if len(specificFiles) == 0:
        for statusId in status:
            statusContent = status[statusId]
            if statusId == "branch" or statusId == "added":
                continue

            specificFiles = specificFiles + statusContent

    if len(filePaths) != 0 and shouldVerify:
        filesForParsing = searchInStatus(
            filePaths,
            status,
            excludedFiles=["branch", "added"],
            getOriginalStructure=True,
        )
        specificFiles = searchInStatus(
            filePaths, status, excludedFiles=["branch", "added"]
        )

    if not shouldVerify:
        commands = parseStatus(filesForParsing)

        runAll(commands)
        return m.log("reset-all-success")

    if len(specificFiles) == 0:
        return m.log("error-add-files_not_found")

    print()
    answers = multiSelect(
        title=m.getMessage("reset-title"),
        finalTitle=m.getMessage("file-selection-finaltitle"),
        errorMessage=m.getMessage("error-files_selected_not_found"),
        options=specificFiles,
        colors=INPUT_THEME["ADD_SELECTION"],
        icons=INPUT_ICONS,
    )

    if len(answers) == 0:
        return m.log("error-files_selected_not_found")

    choices = []
    for answer in answers:
        choices.append(removeColors(answer))

    filesForParsing = searchInStatus(
        choices,
        status,
        excludedFiles=["branch", "added"],
        getOriginalStructure=True,
    )

    runAll(parseStatus(filesForParsing))
    m.log("reset-success")


def Router(router, subroute):
    if subroute == "DEFAULT":
        reset(router.leftKeys)
