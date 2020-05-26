
def run(command=[]):
    from subprocess import Popen, PIPE

    process = Popen(command, stdout=PIPE, stderr=PIPE, universal_newlines=True)

    output, error = process.communicate()

    if process.returncode != 0:
        if error.find("not a git repository") != -1:
            print(messages["notGitRepository"])
        elif error.find("did not match any files") != 1:
            print(messages["add-adition-notafile"])
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
        run(["git", "add"] + specificFiles)
        return print(messages["add-success"])

    if len(filePaths) > 0:
        return print("file not found")

    from Status import getStatus, setUp as setUpStatus
    from Tools.Inputs import prompts

    setUpStatus(messages)
    status = getStatus()

    options = []
    for statusId in status:
        statusContent = status[statusId]
        if statusId == "branch" or statusId == "added":
            continue

        options = options + statusContent

    if len(options) == 0:
        return print(messages["add-nofiles-error"])

    print()
    answer = prompts().multiSelect(title=messages["add-adition-title"],
                                   finalTitle=messages["add-adition-finaltitle"],
                                   options=options)

    if answer == "UNKNOWN_ERROR":
        return print(messages["unknown-error"])
    if len(answer) == 0:
        return print(messages["add-nofileschoosen-error"])

    run(["git", "add"] + answer)
    print(messages["add-success"])


def removeAll():
    from Status import getStatus, setUp as setUpStatus
    from Tools.Inputs import prompts

    setUpStatus(messages)
    status = getStatus()

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

    if subroute == "REMOVE_ALL":
        removeAll()
    if subroute == "DEFAULT":
        remove(router.leftKeys)
