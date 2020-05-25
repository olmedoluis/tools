from subprocess import Popen, PIPE


def run(command=[]):
    process = Popen(command, stdout=PIPE, stderr=PIPE, universal_newlines=True)

    output, error = process.communicate()

    if process.returncode != 0:
        exit()

    return output


def add():
    from Status import getStatus, setUp
    from Tools.Inputs import prompts

    setUp(messages)
    status = getStatus()

    options = []
    for statusId in status:
        statusContent = status[statusId]
        if statusId == "branch" or statusId == "added":
            continue

        options = options + statusContent

    if len(options) == 0:
        return

    answer = prompts().multiSelect(title="Choose files to add:",
                                   finalTitle="files selected",
                                   options=options)

    if len(answer) == 0:
        return

    run(["git", "add"] + answer)


def Router(router, subroute):
    global messages
    messages = router.messages

    if subroute == "DEFAULT":
        add()
