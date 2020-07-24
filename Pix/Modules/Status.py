from .Helpers import run, MessageControl
from Pix.Data.Theme import THEME, RESET


def searchInStatus(fileSearch, status, excludedFiles=[], includedFiles=[]):
    matches = []

    for statusId in status:
        isExcludedFile = statusId in excludedFiles
        isIncludedFile = not statusId in includedFiles

        if isExcludedFile if len(excludedFiles) != 0 else isIncludedFile:
            continue

        changes = status[statusId]

        for change in changes:
            for file in fileSearch:
                if file.lower() in change.lower():
                    matches.append(change)

    return matches


def parseChange(status, changeId, changeName, path):
    draggedChange = status[changeName] if changeName in status else []

    if changeId == "R":
        oldFilePaths, newFilePaths = path.split(" -> ")
        oldFilePaths = oldFilePaths.split("/")
        newFilePaths = newFilePaths.split("/")

        for index in range(len(oldFilePaths)):
            if not oldFilePaths[index] == newFilePaths[index]:
                path = (
                    oldFilePaths[:index]
                    + [THEME["th_modified"] + newFilePaths[index]]
                    + newFilePaths[index + 1 :]
                    + RESET
                )
                path = "/".join(path)
                break

    status[changeName] = [*draggedChange, path]

    return status


def getStatus():
    STATUS_MATCHES = {
        "##": "branch",
        "??": "untracked",
        "UU": "conflicted",
        "U": "conflicted",
        "M": "modified",
        "R": "renamed",
        "A": "added",
        "D": "deleted",
    }

    statusData = run(["git", "status", "-sb"])
    statusData = statusData.rstrip().split("\n")

    status = {}
    for changeRaw in statusData:
        change = changeRaw[3:]
        changeId = changeRaw[:2]
        firstLetter, secondLetter = changeId

        if changeId in STATUS_MATCHES:
            parseChange(status, changeId, STATUS_MATCHES[changeId], change)
            continue

        if firstLetter != " ":
            parseChange(status, firstLetter, STATUS_MATCHES["A"], change)

        if secondLetter != " ":
            parseChange(status, secondLetter, STATUS_MATCHES[secondLetter], change)

    return status


def showStatus():
    m = MessageControl()
    status = getStatus()

    print()
    if "branch" in status:
        branch_name = status.pop("branch")[0]
        m.log("branch", {"pm_branch": branch_name})

    if len(status) == 0:
        m.log("clean")

    for change_name in status:
        changes = status[change_name]

        m.log(f"{change_name}-title")
        for change in changes:
            m.log(change_name, {"pm_change": change})

    print()


def Router(router, subroute):
    if subroute == "DEFAULT":
        showStatus()
