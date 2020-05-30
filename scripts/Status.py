#!/usr/bin/python3

from Helpers import run


def errorRunValidator(error):
    if error.find("not a git repository") != -1:
        print(messages["notGitRepository"])
    else:
        print(messages["unknown-error"])


def getStatus():
    STATUS_MATCHES = {"#": "branch", "M": "modified",
                      "?": "untracked",
                      "R": "renamed", "A": "added",
                      "D": "deleted"}

    status_data = run(errorRunValidator, ["git", "status", "-sb"])
    status_data = status_data.rstrip().split("\n")

    status = {}
    for change in status_data:
        prefix = change[:2]
        firstCode = change[0]
        secondCode = change[1]
        content = change[3:]
        change_name = ''
        second_change_name = ''

        if "R" in prefix:
            files = content.split(" -> ")
            oldFilePaths = files[0].split("/")
            newFilePaths = files[1].split("/")

            for index in range(0, len(oldFilePaths)):
                if not oldFilePaths[index] == newFilePaths[index]:
                    content = messages["renamed-modify"].format(
                        '/'.join(oldFilePaths[0:index]), '/'.join(newFilePaths[index:]))
                    break

        if firstCode.isalpha():
            change_name = STATUS_MATCHES["A"]
            if secondCode != " ":
                second_name = STATUS_MATCHES[secondCode]
                second_change_name = second_name if second_name != '' else ''
        else:
            change_name = STATUS_MATCHES[secondCode] if firstCode == ' ' else STATUS_MATCHES[firstCode]

        if not change_name in status:
            status[change_name] = []

        if not second_change_name in status and second_change_name != "":
            status[second_change_name] = []

        status[change_name].append(content)
        if second_change_name != "":
            status[second_change_name].append(content)

    return status


def showStatus():
    status = getStatus()

    print()
    if "branch" in status:
        branch_name = status.pop("branch")[0]
        print(messages["branch"].format(branch_name))

    if len(status) == 0:
        print(messages["clean"])

    for change_name in status:
        changes = status[change_name]

        print(messages[f"{change_name}-title"])
        for change in changes:
            print(messages[change_name].format(change))

    print()


def setUp(outsideMessages):
    global messages
    messages = outsideMessages


def Router(router, subroute):
    setUp(router.messages)

    if subroute == "DEFAULT":
        showStatus()
