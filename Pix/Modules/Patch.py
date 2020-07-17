from pprint import pprint


def addToFile(text, filePath):
    f = open(filePath, "w+")
    f.write(text)
    f.close()


def parseDifferences(differencesRaw, files):
    class patch:
        def __init__(self, fileName, metaData):
            self.fileName = fileName
            self.metaData = metaData
            self.patches = []

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
                newPatch.patches.append(lines[lastIndex : index + 1] + [""])
                lastIndex = index + 1

            index = index + 1

        newPatch.patches.append(lines[lastIndex:])
        outputPatches.append(newPatch)
        indexFile = indexFile + 1

    return outputPatches


def patchAll():
    from .Helpers import run
    from pathlib import Path
    from .Prompts import patchSelect

    cwd = Path.cwd()
    filePath = f"{cwd}/changes.patch"

    differencesRaw = run(["git", "diff-files", "-p", "Pix/Modules/Helpers.py"])
    metaData, patches = parseDifferences(differencesRaw)

    selectedPatches = patchSelect(
        patches=patches,
        seleccionableLinesIncludes=["+", "-"],
        fileName="Pix/Modules/Helpers.py",
    )

    patchGenerated = metaData
    for patch in selectedPatches:
        patchGenerated = patchGenerated + patch

    addToFile("\n".join(patchGenerated), filePath)
    run(
        [
            "git",
            "apply",
            "--ignore-space-change",
            "--ignore-whitespace",
            "--cached",
            filePath,
        ]
    )

    run(["rm", filePath])


def setUp(outsideMessages):
    global messages
    messages = outsideMessages


def Router(router, subroute):
    setUp(router.messages)

    if subroute == "DEFAULT":
        patchAll()

