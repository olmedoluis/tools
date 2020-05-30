from Helpers import run


def errorRunValidator(error):
    if error.find("not a git repository") != -1:
        print(messages["notGitRepository"])
    else:
        print(messages["unknown-error"])


def branchSelection():
    branchesOutput = run(errorRunValidator, ["git", "branch"])
    branchesSpaced = branchesOutput.rstrip().split("\n")

    branches = []
    actualBranch = ""
    for branch in branchesSpaced:
        if branch[0] == "*":
            branch = branch[1:]
            actualBranch = branch.lstrip()
        branches.append(branch.lstrip())

    from Tools.Inputs import prompts
    prompts = prompts()

    print()
    branchSelected = prompts.select(title=messages["commit-type-title"],
                                    options=branches, selectedColor="\x1b[33m", errorMessage="errorxd")

    from Status import getStatus, setUp as setUpStatus
    setUpStatus(messages)
    hasChanges = len(getStatus().keys()) > 1

    if hasChanges:
        return print(messages["error-haschanges"])

    if branchSelected != actualBranch:
        run(errorRunValidator, ["git", "checkout", branchSelected])
        print(messages["branch-success"].format(branchSelected))
    else:
        print(messages["error-samebranch"].format(branchSelected))


def branchCreation():
    print("hola")


def setUp(outsideMessages):
    global messages
    messages = outsideMessages


def Router(router, subroute):
    setUp(router.messages)

    if subroute == "BRANCH_CREATION":
        branchCreation()
    elif subroute == "DEFAULT":
        branchSelection()
