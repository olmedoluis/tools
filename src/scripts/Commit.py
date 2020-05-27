
def run(command=[]):
    from subprocess import Popen, PIPE

    process = Popen(command, stdout=PIPE, stderr=PIPE, universal_newlines=True)

    output, error = process.communicate()

    if process.returncode != 0:
        if error.find("not a git repository") != -1:
            print(messages["notGitRepository"])
        else:
            print(messages["unknown-error"])
        exit()

    return output


def save():
    from Status import getStatus, setUp as setUpStatus

    setUpStatus(messages)
    status = getStatus()

    if not "added" in status:
        return print(messages["commit-nofiles"])

    addedFiles = status["added"]

    print(messages["added-title"])
    for addedFile in addedFiles:
        print(messages["added"].format(addedFile))
    print()

    from Tools.Inputs import prompts

    options = ["feat", "refactor", "fix", "style"]
    scapeError = messages["scape-error"]

    prompts = prompts()
    kind = prompts.select(
        title=messages["commit-type-title"], options=options, selectedColor="\x1b[33m", errorMessage=scapeError)

    if kind == "":
        return print(messages["commit-empty"])

    scope = prompts.text(
        title=messages["commit-scope-title"], placeHolder="file.js", errorMessage=scapeError)

    if scope == "":
        return print(messages["commit-empty"])

    about = prompts.text(
        title=messages["commit-about-title"], errorMessage=scapeError)

    if about == "":
        return print(messages["commit-empty"])

    commit = "{}({}):{}".format(kind, scope, about)
    print(messages["commit-preview"].format(commit))

    isSure = prompts.confirm(
        title=messages["commit-confirm"], errorMessage=scapeError)

    if isSure:
        run(["git", "commit", "-m", f"\"{commit}\""])
        print(messages["commit-success"])
    else:
        print(messages["commit-cancel"])


def setUp(outsideMessages):
    global messages
    messages = outsideMessages


def Router(router, subroute):
    setUp(router.messages)

    if subroute == "DEFAULT":
        save()
