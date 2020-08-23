def reset(files):
    print("reseting...", files)

def Router(router, subroute):
    if subroute == "DEFAULT":
        reset(router.leftKeys)
