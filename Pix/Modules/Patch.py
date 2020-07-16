from pprint import pprint


def addToFile(text, filePath):
    f = open(filePath, "w+")
    f.write(text)
    f.close()


def parseDifferences(differencesRaw):
    lines = differencesRaw.split("\n")

    metaData = lines[:4]
    patches = []

    index = 4
    lastIndex = 4
    for line in lines[5:]:
        if "@@ " == line[:3] and " @@" in line[3:]:
            patches.append(lines[lastIndex : index + 1] + [""])
            lastIndex = index + 1

        index = index + 1

    patches.append(lines[lastIndex:])

    return metaData, patches


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
        lines=patches[0][1:],
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

