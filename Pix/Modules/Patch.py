def addToFile(text, filePath):
    f = open(filePath, "w+")
    f.write(text)
    f.close()


def patchAll():
    from .Helpers import run
    from pathlib import Path
    from .Prompts import bookSelection

    cwd = Path.cwd()
    filePath = f"{cwd}/changes.patch"

    differences = run(["git", "diff"])
    wea = bookSelection(lines=differences, seleccionableLinesIncludes=["+", "-"])
    
    return print(differences)
    addToFile(differences, filePath)
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
