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

    run(errorRunValidator, ["git", "stash", "push", "-m", title])


def setUp(outsideMessages):
    global messages
    messages = outsideMessages


def Router(router, subroute):
    setUp(router.messages)

    if subroute == "DEFAULT":
        addToStash()
