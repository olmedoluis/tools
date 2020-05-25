def add():
    print("gg")


def Router(router, subroute):
    global messages
    messages = router.messages

    if subroute == "DEFAULT":
        add()
