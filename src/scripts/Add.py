from subprocess import Popen, PIPE


def run(command=[]):
    process = Popen(command, stdout=PIPE, stderr=PIPE, universal_newlines=True)

    output, error = process.communicate()

    if process.returncode != 0:
        if error.find("not a git repository") != -1:
            print(messages["notGitRepository"])
        exit()

    return output


def add():
    from Status import getStatus, setUp as setUpStatus
    from Tools.Inputs import prompts

    setUpStatus(messages)
    status = getStatus()

    options = []
    for statusId in status:
        statusContent = status[statusId]
        if statusId == "branch" or statusId == "added":
            continue

        options = options + statusContent

    if len(options) == 0:
        return print(messages["add-nofiles-error"])

    print()
    answer = prompts().multiSelect(title=messages["add-adition-title"],
                                   finalTitle=messages["add-adition-finaltitle"],
                                   options=options)

    if len(answer) == 0:
        return print(messages["add-nofileschoosen-error"])

    run(["git", "add"] + answer)
    print(messages["add-success"])


def setUp(outsideMessages):
    global messages
    messages = outsideMessages


def Router(router, subroute):
    setUp(router.messages)

    if subroute == "DEFAULT":
        add()
