
def run(command=[]):
    from subprocess import Popen, PIPE

    process = Popen(command, stdout=PIPE, stderr=PIPE, universal_newlines=True)

    output, error = process.communicate()

    if process.returncode != 0:
        if error.find("not a git repository") != -1:
            print(messages["notGitRepository"])
        elif error.find("did not match any files") != 1:
            print(messages["notafile-error"])
        else:
            print(messages["unknown-error"])
        exit()

    return output


def remove(filePaths=[]):
    from pathlib import Path as isFile

    specificFiles = []
    for filePath in filePaths:
        if not isFile(filePath):
            break

        specificFiles.append(filePath)

    if len(specificFiles) > 0:
        run(["git", "reset", "HEAD"] + specificFiles)
        return print(messages["remove-success"])

    from Status import getStatus, setUp as setUpStatus
    from Tools.Inputs import prompts

    setUpStatus(messages)
    status = getStatus()

    options = status["added"] if "added" in status else []

    if len(options) == 0:
        return print(messages["remove-nofiles-error"])

    print()
    answers = prompts().multiSelect(title=messages["remove-removing-title"],
                                    finalTitle=messages["file-selection-finaltitle"],
                                    options=options, selectedColor="\x1b[31m")

    if answers == "UNKNOWN_ERROR":
        return print(messages["unknown-error"])
    if len(answers) == 0:
        return print(messages["remove-nofileschoosen-error"])

    from Helpers import removeColors

    choices = []
    for answer in answers:
        choices.append(removeColors(answer))

    run(["git", "reset", "HEAD"] + choices)
    print(messages["remove-success"])


def removeAll():
    from Status import getStatus, setUp as setUpStatus
    from Tools.Inputs import prompts

    setUpStatus(messages)
    status = getStatus()

    hasFilesToAdd = False
    for statusId in status:
        if statusId != "added":
            continue

        hasFilesToAdd = True
        break

    if hasFilesToAdd:
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
        removeAll()
    if subroute == "DEFAULT":
        remove(router.leftKeys)
