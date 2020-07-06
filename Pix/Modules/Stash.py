from .Helpers import run
from .Status import getStatus
from .Inputs import prompts


def addToStash():
    if not "added" in getStatus():
        return print(messages["error-stash-addedfiles"])

    print()
    title = prompts().text(
        title=messages["stash-in-title"], errorMessage=messages["scape-error"]
    )

    if title == "":
        return print(messages["error-empty"])

    run(["git", "stash", "push", "-m", title])
    print(messages["stash-in-success"])


def stashSelection():
    if len(getStatus()) > 1:
        return print(messages["error-haschanges"])

    stashesOutput = run(["git", "stash", "list"])
    stashesSpaced = stashesOutput.rstrip().split("\n")

    if stashesSpaced[0] == "":
        return print(messages["error-nostashes"])

    stashList = []
    for stashWithSpaces in stashesSpaced:
        stash = stashWithSpaces.lstrip()

        idStartIndex = stash.find("{") + 1
        stashId = stash[idStartIndex : idStartIndex + 1]

        branchStartIndex = stash.find("On") + 3
        branchEndIndex = stash.find(" ", branchStartIndex) - 1
        branch = stash[branchStartIndex:branchEndIndex]

        content = stash[branchEndIndex + 2 :]

        stashList.append(messages["stash-listitem"].format(stashId, content, branch))

    print()
    stashSelected = prompts().select(
        title=messages["branch-selection-title"],
        options=stashList,
        selectedColor="\x1b[36m",
        errorMessage=messages["scape-error"],
    )

    if stashSelected == "":
        return print(messages["error-empty"])

    stashId = stashSelected[0]
    run(["git", "stash", "pop", stashId])
    print(messages["stash-back-success"].format(stashSelected))


def setUp(outsideMessages):
    global messages
    messages = outsideMessages


def Router(router, subroute):
    setUp(router.messages)

    if subroute == "ADD_STASH":
        addToStash()
    if subroute == "DEFAULT":
        stashSelection()
