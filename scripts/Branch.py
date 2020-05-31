from Helpers import run


def errorRunValidator(error):
    if error.find("not a git repository") != -1:
        print(messages["notGitRepository"])
    else:
        print(messages["unknown-error"])


def getHasChanges():
    from Status import getStatus, setUp as setUpStatus

    return len(getStatus().keys()) > 1


def branchSelection(branchSearch):
    hasChanges = getHasChanges()

    if hasChanges:
        return print(messages["error-haschanges"])

    branchesOutput = run(errorRunValidator, ["git", "branch"])
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
        from Tools.Inputs import prompts
        prompts = prompts()

        print()
        branchSelected = prompts.select(title=messages["branch-selection-title"],
                                        options=branches, selectedColor="\x1b[33m", errorMessage=messages["scape-error"])

        if branchSelected == "":
            return print(messages["error-empty"])

    if branchSelected != actualBranch:
        run(errorRunValidator, ["git", "checkout", branchSelected])
        print(messages["branch-success"].format(branchSelected))
    else:
        print(messages["error-samebranch"].format(branchSelected))


def branchCreation():
    hasChanges = getHasChanges()

    if hasChanges:
        return print(messages["error-haschanges"])

    from Tools.Inputs import prompts
    prompts = prompts()

    options = ["feature", "refactor", "bugfix", "style"]
    scapeError = messages["scape-error"]

    print()
    answers = prompts.many([{"type": "Select", "title": messages["branch-type-title"],
                             "options":options, "selectedColor":"\x1b[33m", "errorMessage":scapeError},
                            {"type": "Text", "title": messages["branch-id-title"],
                             "placeHolder": "", "errorMessage": scapeError},
                            {"type": "Text", "title": messages["branch-about-title"], "errorMessage": scapeError}])

    if len(answers) != 3:
        return print(messages["error-empty"])

    kind, ticketId, about = answers
    ticketId = ticketId.upper().replace(" ", "-")
    about = about.lower().replace(" ", "-")

    branch = f"{kind}/{ticketId}-{about}"

    print(messages["preview"].format(branch))

    isSure = prompts.confirm(
        title=messages["confirmation"])

    if isSure:
        run(errorRunValidator, ["git", "branch", branch])
        print(messages["branch-success"].format(branch))
    else:
        return print(messages["commit-cancel"])

    shouldSwitch = prompts.confirm(
        title=messages["branch-shouldswitch"])

    if shouldSwitch:
        run(errorRunValidator, ["git", "checkout", branch])
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
