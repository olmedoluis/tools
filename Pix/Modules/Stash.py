from .Helpers import run, MessageControl
from .Status import getStatus


def addToStash():
    from .Prompts import text
    from Configuration.Theme import INPUT_THEME, INPUT_ICONS

    m = MessageControl()

    if not "added" in getStatus():
        return m.log("error-stash-addedfiles")

    print()
    title = text(
        title=m.getMessage("stash-in-title"),
        errorMessage=m.getMessage("scape-error"),
        colors=INPUT_THEME["STASH_CREATION_NAME"],
    )

    if title == "":
        return m.log("error-empty")

    run(["git", "stash", "push", "-m", title])
    m.log("stash-in-success")


def stashSelection():
    from .Prompts import select
    from Configuration.Theme import INPUT_THEME, INPUT_ICONS

    m = MessageControl()

    if len(getStatus()) > 1:
        return m.log("error-haschanges")

    stashesOutput = run(["git", "stash", "list"])
    stashesSpaced = stashesOutput.rstrip().split("\n")

    if stashesSpaced[0] == "":
        return m.log("error-nostashes")

    stashList = []
    for stashWithSpaces in stashesSpaced:
        stash = stashWithSpaces.lstrip()

        idStartIndex = stash.find("{") + 1
        stashId = stash[idStartIndex : idStartIndex + 1]

        branchStartIndex = stash.find("On") + 3
        branchEndIndex = stash.find(" ", branchStartIndex) - 1
        branch = stash[branchStartIndex:branchEndIndex]

        name = stash[branchEndIndex + 2 :]

        stashList.append(
            m.getMessage(
                "stash-listitem",
                {"pm_stashid": stashId, "pm_stashname": name, "pm_stashbranch": branch},
            )
        )

    print()
    stashSelected = select(
        title=m.getMessage("branch-selection-title"),
        options=stashList,
        errorMessage=m.getMessage("scape-error"),
        colors=INPUT_THEME["STASH_SELECTION"],
        icons=INPUT_ICONS,
    )

    if stashSelected == "":
        return m.log("error-empty")

    stashId = stashSelected[0]
    run(["git", "stash", "pop", stashId])
    m.log("stash-back-success", {"pm_stash": stashSelected})


def Router(router, subroute):
    if subroute == "ADD_STASH":
        addToStash()
    if subroute == "DEFAULT":
        stashSelection()
