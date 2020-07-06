from .Helpers import run
from .Inputs import prompts


def getHasChanges(change=""):
    from .Status import getStatus

    status = getStatus()

    return len(status.keys()) > 1 if change == "" else change in status


def branchSelection(branchSearch):
    hasChanges = getHasChanges()

    if hasChanges:
        return print(messages["error-haschanges"])

    branchesOutput = run(["git", "branch"])
    branchesSpaced = branchesOutput.rstrip().split("\n")

    if branchesSpaced[0] == "":
        return print(messages["error-nobranches"])

    if branchSearch != "":
        branchMatch = []
        for branch in branchesSpaced:
            if branch.find(branchSearch) != -1:
                branchMatch.append(branch)

        if len(branchMatch) == 0:
            return print(messages["error-nomatchbranch"].format(branchSearch))

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
        inputs = prompts()

        print()
        branchSelected = inputs.select(
            title=messages["branch-selection-title"],
            options=branches,
            selectedColor="\x1b[33m",
            errorMessage=messages["scape-error"],
        )

        if branchSelected == "":
            return print(messages["error-empty"])

    if branchSelected != actualBranch:
        run(["git", "checkout", branchSelected])
        print(messages["branch-success"].format(branchSelected))
    else:
        print(messages["error-samebranch"].format(branchSelected))


def branchCreation():
    hasChanges = getHasChanges()

    if hasChanges:
        return print(messages["error-haschanges"])

    inputs = prompts()

    options = ["feature", "refactor", "bugfix", "style"]
    scapeError = messages["scape-error"]

    print()
    answers = inputs.many(
        [
            {
                "type": "Select",
                "title": messages["branch-type-title"],
                "options": options,
                "selectedColor": "\x1b[33m",
                "errorMessage": scapeError,
            },
            {
                "type": "Text",
                "title": messages["branch-id-title"],
                "placeHolder": "",
                "errorMessage": scapeError,
            },
            {
                "type": "Text",
                "title": messages["branch-about-title"],
                "errorMessage": scapeError,
            },
        ]
    )

    if len(answers) != 3:
        return print(messages["error-empty"])

    kind, ticketId, about = answers
    ticketId = ticketId.upper().replace(" ", "-")
    about = about.lower().replace(" ", "-")

    branch = f"{kind}/{ticketId}-{about}"

    print(messages["preview"].format(branch))

    isSure = inputs.confirm(title=messages["confirmation"])

    if isSure:
        run(["git", "branch", branch])
        print(messages["branch-success"].format(branch))
    else:
        return print(messages["commit-cancel"])

    shouldSwitch = inputs.confirm(title=messages["branch-shouldswitch"])

    if shouldSwitch:
        run(["git", "checkout", branch])
        print(messages["branch-switchsuccess"].format(branch))
    else:
        print(messages["error-inputcancel"])


def setUp(outsideMessages):
    global messages
    messages = outsideMessages


def Router(router, subroute):
    setUp(router.messages)

    if subroute == "BRANCH_CREATION":
        branchCreation()
    elif subroute == "DEFAULT":
        branchSelection(router.getNextRoute())
