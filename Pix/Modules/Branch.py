from .Helpers import run, MessageControl


def getHasChanges(change=""):
    from .Status import getStatus

    status = getStatus()

    return len(status.keys()) > 1 if change == "" else change in status


def branchSelection(branchSearch):
    from .Prompts import select

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
        from Pix.Data.Theme import INPUT_THEME, ICONS

        print()
        branchSelected = select(
            title=m.getMessage("branch-selection-title"),
            options=branches,
            selectedColor="\x1b[33m",
            errorMessage=m.getMessage("scape-error"),
            colors=INPUT_THEME["BRANCH_SELECTION"],
            icons={"selection": ICONS["ic_selection"]},
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
    from Pix.Data.Theme import INPUT_THEME, ICONS

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
                "selectedColor": "\x1b[33m",
                "errorMessage": scapeError,
                "colors": INPUT_THEME["BRANCH_CREATION_TYPE"],
                "icons": {"selection": ICONS["ic_selection"]},
            },
            {
                "type": "Text",
                "title": m.getMessage("branch-id-title"),
                "placeHolder": "",
                "errorMessage": scapeError,
            },
            {
                "type": "Text",
                "title": m.getMessage("branch-about-title"),
                "errorMessage": scapeError,
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

    isSure = confirm(title=m.getMessage("confirmation"))

    if isSure:
        run(["git", "branch", branch])
        m.log("branch-success", {"pm_branch": branch})
    else:
        return m.log("commit-cancel")

    shouldSwitch = confirm(title=m.getMessage("branch-shouldswitch"))

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
