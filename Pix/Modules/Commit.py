
from .Helpers import run, removeColors
from .Status import getStatus
from Tools.Inputs import prompts
from os.path import basename
from os import getcwd

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

    index = 0
    for example in directoriesSplited[0]:
        for directory in directoriesSplited:
            if example == directory[index]:
                continue
            return removeColors(directory[index - 1] if index > 0 else basename(getcwd()))

        index = index + 1

    return removeColors(basename(getcwd()))


def save():
    status = getStatus()

    if not "added" in status:
        return print(messages["commit-nofiles"])

    addedFiles = status["added"]

    print(messages["added-title"])
    for addedFile in addedFiles:
        print(messages["added"].format(addedFile))
    print()


    options = ["feat", "refactor", "fix", "style"]
    scapeError = messages["scape-error"]
    commonDir = getCommonDirectory(status["added"])

    inputs = prompts()

    answers = inputs.many([{"type": "Select", "title": messages["commit-type-title"],
                             "options":options, "selectedColor":"\x1b[33m", "errorMessage":scapeError},
                            {"type": "Text", "title": messages["commit-scope-title"],
                             "placeHolder": commonDir, "errorMessage": scapeError},
                            {"type": "Text", "title": messages["commit-about-title"], "errorMessage": scapeError}])

    if len(answers) != 3:
        return print(messages["error-empty"])

    commit = "{}({}):{}".format(*answers)
    print(messages["preview"].format(commit))

    isSure = inputs.confirm(title=messages["confirmation"])

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
