
from Helpers import run


def errorRunValidator(error):
    if error.find("not a git repository") != -1:
        print(messages["notGitRepository"])
    else:
        print(messages["unknown-error"])


def getCommonDirectory(directories):
    directoriesSplited = []
    for directory in directories:
        directoriesSplited.append(directory.split("/"))

    if len(directoriesSplited) == 1:
        return directoriesSplited[0][-1]

    from os.path import basename
    from os import getcwd
    from Helpers import removeColors

    index = 0
    for example in directoriesSplited[0]:
        for directory in directoriesSplited:
            if example == directory[index]:
                continue
            return removeColors(directory[index - 1] if index > 0 else basename(getcwd()))

        index = index + 1

    return removeColors(basename(getcwd()))


def save():
    from Status import getStatus, setUp as setUpStatus

    setUpStatus(messages)
    status = getStatus()

    if not "added" in status:
        return print(messages["commit-nofiles"])

    addedFiles = status["added"]

    print(messages["added-title"])
    for addedFile in addedFiles:
        print(messages["added"].format(addedFile))
    print()

    from Tools.Inputs import prompts

    options = ["feat", "refactor", "fix", "style"]
    scapeError = messages["scape-error"]
    commonDir = getCommonDirectory(status["added"])

    prompts = prompts()

    answers = prompts.many([{"type": "Select", "title": messages["commit-type-title"],
                             "options":options, "selectedColor":"\x1b[33m", "errorMessage":scapeError},
                            {"type": "Text", "title": messages["commit-scope-title"],
                             "placeHolder": commonDir, "errorMessage": scapeError},
                            {"type": "Text", "title": messages["commit-about-title"]}])

    if len(answers) != 3:
        return print(messages["error-empty"])

    commit = "{}({}):{}".format(*answers)
    print(messages["preview"].format(commit))

    isSure = prompts.confirm(title=messages["confirmation"])

    if isSure:
        run(errorRunValidator, ["git", "commit", "-m", commit])
        print(messages["commit-success"])
    else:
        print(messages["commit-cancel"])


def setUp(outsideMessages):
    global messages
    messages = outsideMessages


def Router(router, subroute):
    setUp(router.messages)

    if subroute == "DEFAULT":
        save()