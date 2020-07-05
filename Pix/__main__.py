import sys
from Configuration import ALIASES, MESSAGES
from .Data.PixRoutes import KEYS
from .Modules import (
    AddRouter,
    StatusRouter,
    BranchRouter,
    CommitRouter,
    RemoveRouter,
    StashRouter,
)
from .Modules.Helpers import checkPixShortcut, checkRoute


class PixTools:
    def __init__(self, argv):
        self.user_routes = argv
        self.actual_route = argv[0]
        self.leftKeys = argv[1:]
        self.messages = MESSAGES

    def getGoodRoutes(self):
        good_routes = []

        for route in self.user_routes:
            if route != self.actual_route:
                good_routes.append(route)
            else:
                break

        return good_routes

    def getNextRoute(self):
        return "" if 0 == len(self.leftKeys) else self.leftKeys[0]


def getConcatenatedRoutes(routes):
    indexes = [i for i, e in enumerate(routes) if e == "n"]
    lastRoute = routes[indexes[-1] + 1 :]
    allRoutes = []
    lastIndex = 0

    for index in indexes:
        allRoutes.append(routes[lastIndex:index])
        lastIndex = index + 1

    allRoutes.append(lastRoute)

    return allRoutes


def main():
    arg = sys.argv[1:]

    if len(arg) == 0:
        return

    PIX_STORE = {
        "Status": StatusRouter,
        "Add": AddRouter,
        "Remove": RemoveRouter,
        "Commit": CommitRouter,
        "Branch": BranchRouter,
        "Stash": StashRouter,
    }

    allRoutes = getConcatenatedRoutes(arg) if "n" in arg else [arg]

    for arguments in allRoutes:
        pixTools = PixTools(arguments)

        route_name = checkPixShortcut(pixTools.actual_route, KEYS, ALIASES)

        if route_name == False:
            good_routes = f"pix {' '.join(pixTools.getGoodRoutes())}"
            wrong_routes = f"{pixTools.actual_route} {' '.join(pixTools.leftKeys)}"
            return print(MESSAGES["unknownRoute"].format(good_routes, wrong_routes))

        next_route = pixTools.getNextRoute()
        subroute = checkRoute(next_route, KEYS[route_name], ALIASES[route_name])

        requiredRouter = PIX_STORE[route_name]
        requiredRouter(pixTools, subroute)


if __name__ == "__main__":
    main()
