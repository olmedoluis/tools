
def run(command=[]):
    from subprocess import Popen, PIPE

    process = Popen(command, stdout=PIPE, stderr=PIPE, universal_newlines=True)

    output, error = process.communicate()

    if process.returncode != 0:
        if error.find("not a git repository") != -1:
            print(messages["notGitRepository"])
        elif error.find("did not match any files") != 1:
            print(messages["add-adition-notafile"])
        else:
            print(messages["unknown-error"])
        exit()

    return output


def save():
    print("hola")


def setUp(outsideMessages):
    global messages
    messages = outsideMessages


def Router(router, subroute):
    setUp(router.messages)

    if subroute == "DEFAULT":
        save()
