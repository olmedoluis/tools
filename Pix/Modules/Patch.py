def addToFile(text, filePath):
    f = open(filePath, "w+")
    f.write(text)
    f.close()


def parsePatches(patches):
    parsedPatches = []

    for patch in patches:
        if len(patch.patchesSelected):
            parsedPatches = parsedPatches + patch.metaData

            for indexSelected in patch.patchesSelected:
                parsedPatches = parsedPatches + patch.patches[indexSelected]

    if not len(parsedPatches):
        parsedPatches = [""]

    return parsedPatches if parsedPatches[-1] == "" else parsedPatches + [""]


def parseDifferences(differencesRaw, files):
    class patch:
        def __init__(self, fileName, metaData):
            self.fileName = messages["file-title"].format(fileName)
            self.metaData = metaData
            self.patches = []
            self.patchesSelected = []

    lines = differencesRaw.split("\n")
    differences = []

    index = 0
    lastIndex = 0
    for line in lines[1:]:
        if "diff --git a" == line[:12]:
            differences.append(lines[lastIndex : index + 1])
            lastIndex = index + 1

        index = index + 1

    differences.append(lines[lastIndex:])

    outputPatches = []
    indexFile = 0
    for lines in differences:
        metaData = lines[:4]
        newPatch = patch(fileName=files[indexFile], metaData=metaData)

        index = 4
        lastIndex = 4
        for line in lines[5:]:
            if "@@ " == line[:3] and " @@" in line[3:]:
                newPatch.patches.append(lines[lastIndex : index + 1])
                lastIndex = index + 1

            index = index + 1

        newPatch.patches.append(lines[lastIndex:] + [""])
        outputPatches.append(newPatch)
        indexFile = indexFile + 1

    return outputPatches


def patch(files):
    from .Helpers import run
    from .Prompts import patchSelect
    from pathlib import Path

    cwd = Path.cwd()
    filePath = f"{cwd}/changes.patch"

    differencesRaw = run(["git", "diff-files", "-p"] + files)
    patches = parseDifferences(differencesRaw, files)

    selectedPatches = patchSelect(
        files=patches, errorMessage=messages["error-nofileschoosen"]
    )

    patchGenerated = parsePatches(selectedPatches)

    if not len(patchGenerated):
        return print(messages["error-empty"])

    addToFile("\n".join(patchGenerated), filePath)

    run(["git", "apply", "--cached", filePath])

    run(["rm", filePath])


def patchAll(fileSearch):
    from .Status import getStatus, searchInStatus

    status = getStatus()
    if len(fileSearch) > 0:
        matches = searchInStatus(fileSearch, status, includedFiles=["modified"])

        return (
            print(messages["error-nomatchfile"])
            if len(matches) == 0
            else patch(matches)
        )

    files = []
    for statusId in status:
        if statusId != "added" and statusId != "branch" and statusId != "untracked":
            files = files + status[statusId]

    if not len(files):
        return print(messages["error-patch-nofiles"])

    patch(files)


def setUp(outsideMessages):
    global messages
    messages = outsideMessages


def Router(router, subroute):
    setUp(router.messages)

    if subroute == "DEFAULT":
        patchAll(router.leftKeys)

