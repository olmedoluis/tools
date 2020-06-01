#!/usr/bin/python3

from Helpers import run


def errorRunValidator(error):
    if error.find("not a git repository") != -1:
        print(messages["notGitRepository"])
    else:
        print(messages["unknown-error"])


def addToStash():
    from Status import getStatus

    if not "added" in getStatus():
        return print("only added files can be stashed")

    from Tools.Inputs import prompts

    prompts = prompts()

    print()
    title = prompts.text(title="ponele titulo:")

    if title == "":
        return print(messages["error-empty"])

    run(errorRunValidator, ["git", "stash", "push", "-m", title])


def stashSelection():
    from Status import getStatus

    if len(getStatus()) > 1:
        return print(messages["error-haschanges"])

    stashesOutput = run(errorRunValidator, ["git", "stash", "list"])
    stashesSpaced = stashesOutput.rstrip().split("\n")

    if stashesSpaced[0] == "":
        return print(messages["error-nobranches"])

    stashList = []
    for stashWithSpaces in stashesSpaced:
        stash = stashWithSpaces.lstrip()

        idStartIndex = stash.find("{") + 1
        stashId = stash[idStartIndex: idStartIndex + 1]

        branchStartIndex = stash.find("On") + 3
        branchEndIndex = stash.find(" ", branchStartIndex) - 1
        branch = stash[branchStartIndex:branchEndIndex]

        content = stash[branchEndIndex + 2:]

        stashList.append(
            messages["stash-listitem"].format(stashId, content, branch))

    from Tools.Inputs import prompts
    prompts = prompts()

    print()
    stashSelected = prompts.select(title=messages["branch-selection-title"],
                                   options=stashList, selectedColor="\x1b[36m", errorMessage=messages["scape-error"])

    if stashSelected == "":
        return print(messages["error-empty"])

    stashId = stashSelected[0]
    run(errorRunValidator, ["git", "stash", "pop", stashId])
    print("You bringed back", stashSelected)


def setUp(outsideMessages):
    global messages
    messages = outsideMessages


def Router(router, subroute):
    setUp(router.messages)

    if subroute == "ADD_STASH":
        addToStash()
    if subroute == "DEFAULT":
        stashSelection()
