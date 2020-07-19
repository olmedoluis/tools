from .Helpers import run, MessageControl

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


def parseDifferences(differencesRaw, files, getMessage):
    class Patch:
        def __init__(self, fileName, metaData):
            self.fileName = fileName
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
        newPatch = Patch(
            fileName=getMessage("file-title", {"pm_file": files[indexFile]}),
            metaData=metaData,
        )

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
    from .Prompts import patchSelect
    from pathlib import Path

    m = MessageControl()

    cwd = Path.cwd()
    filePath = f"{cwd}/changes.patch"

    differencesRaw = run(["git", "diff-files", "-p"] + files)
    patches = parseDifferences(differencesRaw, files, m.getMessage)

    selectedPatches = patchSelect(
        files=patches, errorMessage=m.getMessage("error-nofileschoosen")
    )

    patchGenerated = parsePatches(selectedPatches)

    if not len(patchGenerated):
        return m.log("error-empty")

    addToFile("\n".join(patchGenerated), filePath)

    run(["git", "apply", "--cached", filePath])

    run(["rm", filePath])
    m.log("patch-success")


def patchAll(fileSearch):
    from .Status import getStatus, searchInStatus
    m = MessageControl()

    status = getStatus()
    if len(fileSearch) > 0:
        matches = searchInStatus(fileSearch, status, includedFiles=["modified"])

        return m.log("error-nomatchfile") if len(matches) == 0 else patch(matches)

    files = status["modified"] if "modified" in status else []

    if not len(files):
        return m.log("error-patch-nofiles")

    patch(files)


def Router(router, subroute):
    if subroute == "DEFAULT":
        patchAll(router.leftKeys)

