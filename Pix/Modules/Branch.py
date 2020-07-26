def getHasChanges(change=""):
    from .Status import getStatus

    status = getStatus()

    return len(status.keys()) > 1 if change == "" else change in status


def branchSelection(branchSearch):
    from .Prompts import select
    from .Helpers import run, MessageControl

    m = MessageControl()
    hasChanges = getHasChanges()

    if hasChanges:
        return m.log("error-haschanges")

    branchesOutput = run(["git", "branch"])
    branchesSpaced = branchesOutput.rstrip().split("\n")

    if branchesSpaced[0] == "":
        return m.log("error-nobranches")

    if branchSearch != "":
        branchMatch = []
        for branch in branchesSpaced:
            if branch.find(branchSearch) != -1:
                branchMatch.append(branch)

        if len(branchMatch) == 0:
            return m.log("error-nomatchbranch", {"pm_branch": branchSearch})

        branchesSpaced = branchMatch

    branches = []
    actualBranch = ""
    for branch in branchesSpaced:
        if branch[0] == "*":
            branch = branch[1:]
            actualBranch = branch.lstrip()
        branches.append(branch.lstrip())

    branchSelected = branches[0]

    if len(branches) > 1:
        from Configuration.Theme import INPUT_THEME, INPUT_ICONS

        print()
        branchSelected = select(
            title=m.getMessage("branch-selection-title"),
            options=branches,
            errorMessage=m.getMessage("scape-error"),
            colors=INPUT_THEME["BRANCH_SELECTION"],
            icons=INPUT_ICONS,
        )

        if branchSelected == "":
            return m.log("error-empty")

    if branchSelected != actualBranch:
        run(["git", "checkout", branchSelected])
        m.log("branch-success", {"pm_branch": branchSelected})
    else:
        m.log("error-samebranch", {"pm_branch": branchSelected})


def branchCreation():
    from .Prompts import many, confirm
    from .Helpers import run, MessageControl
    from Configuration.Theme import INPUT_THEME, INPUT_ICONS

    m = MessageControl()
    hasChanges = getHasChanges()

    if hasChanges:
        return m.log("error-haschanges")

    options = ["feature", "refactor", "bugfix", "style"]
    scapeError = m.getMessage("scape-error")

    print()
    answers = many(
        [
            {
                "type": "Select",
                "title": m.getMessage("branch-type-title"),
                "options": options,
                "errorMessage": scapeError,
                "colors": INPUT_THEME["BRANCH_CREATION_TYPE"],
                "icons": INPUT_ICONS,
            },
            {
                "type": "Text",
                "title": m.getMessage("branch-id-title"),
                "placeHolder": "",
                "errorMessage": scapeError,
                "colors": INPUT_THEME["BRANCH_CREATION_ID"],
            },
            {
                "type": "Text",
                "title": m.getMessage("branch-about-title"),
                "errorMessage": scapeError,
                "colors": INPUT_THEME["BRANCH_CREATION_ABOUT"],
            },
        ]
    )

    if len(answers) != 3:
        return m.log("error-empty")

    kind, ticketId, about = answers
    ticketId = ticketId.upper().replace(" ", "-")
    about = about.lower().replace(" ", "-")

    branch = f"{kind}/{ticketId}-{about}"

    m.log("preview", {"pm_preview": branch})

    isSure = confirm(
        title=m.getMessage("confirmation"),
        colors=INPUT_THEME["BRANCH_CREATION_CONFIRM"],
    )

    if isSure:
        run(["git", "branch", branch])
        m.log("branch-success", {"pm_branch": branch})
    else:
        return m.log("commit-cancel")

    shouldSwitch = confirm(
        title=m.getMessage("branch-shouldswitch"),
        colors=INPUT_THEME["BRANCH_CREATION_SWITCH"],
    )

    if shouldSwitch:
        run(["git", "checkout", branch])
        m.log("branch-switchsuccess", {"pm_branch": branch})
    else:
        m.log("error-inputcancel")


def Router(router, subroute):
    if subroute == "BRANCH_CREATION":
        branchCreation()
    elif subroute == "DEFAULT":
        branchSelection(router.getNextRoute())
