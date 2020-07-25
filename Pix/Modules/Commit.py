from .Helpers import run, removeColors, MessageControl


def getCommonDirectory(directories):
    from os.path import basename
    from os import getcwd

    directoriesSplited = []
    for directory in directories:
        directoriesSplited.append(directory.split("/"))

    if len(directoriesSplited) == 1:
        return directoriesSplited[0][-1]

    index = 0
    for example in directoriesSplited[0]:
        for directory in directoriesSplited:
            if example == directory[index]:
                continue
            return removeColors(
                directory[index - 1] if index > 0 else basename(getcwd())
            )

        index = index + 1

    return removeColors(basename(getcwd()))


def save():
    from .Prompts import many, confirm
    from .Status import getStatus
    from Pix.Data.Theme import INPUT_THEME, INPUT_ICONS

    m = MessageControl()
    status = getStatus()

    if not "added" in status:
        return m.log("commit-nofiles")

    addedFiles = status["added"]

    m.log("added-title")
    for addedFile in addedFiles:
        m.log("added", {"pm_change": addedFile})

    options = ["feat", "refactor", "fix", "style"]
    scapeError = m.getMessage("scape-error")
    commonDir = getCommonDirectory(addedFiles)

    print()
    answers = many(
        [
            {
                "type": "Select",
                "title": m.getMessage("commit-type-title"),
                "options": options,
                "errorMessage": scapeError,
                "colors": INPUT_THEME["COMMIT_TYPE"],
                "icons": INPUT_ICONS,
            },
            {
                "type": "Text",
                "title": m.getMessage("commit-scope-title"),
                "placeHolder": commonDir,
                "errorMessage": scapeError,
            },
            {
                "type": "Text",
                "title": m.getMessage("commit-about-title"),
                "errorMessage": scapeError,
            },
        ]
    )

    if len(answers) != 3:
        return m.log("error-empty")

    commit = "{}({}):{}".format(*answers)
    m.log("preview", {"pm_preview": commit})

    isSure = confirm(title=m.getMessage("confirmation"))

    if isSure:
        run(["git", "commit", "-m", commit])
        m.log("commit-success")
    else:
        m.log("commit-cancel")


def Router(router, subroute):
    if subroute == "DEFAULT":
        save()
