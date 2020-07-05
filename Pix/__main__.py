import sys
from .Data.PixRoutes import ROUTES, SUBROUTES
from .Data.Messages import getMessages
from .Modules import (
    AddRouter,
    StatusRouter,
    BranchRouter,
    CommitRouter,
    RemoveRouter,
    StashRouter,
)
from .Modules.Helpers import checkPixShortcut, checkRoute

messages = getMessages()


class PixTools:
    def __init__(self, argv):
        self.user_routes = argv
        self.actual_route = argv[0]
        self.leftKeys = argv[1:]
        self.messages = messages

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


def main():
    arg = sys.argv[1:]

    if len(arg) == 0:
        return

    pixTools = PixTools(arg)

    route_name = checkPixShortcut(pixTools.actual_route, ROUTES)

    if route_name == False:
        good_routes = f"pix {' '.join(pixTools.getGoodRoutes())}"
        wrong_routes = f"{pixTools.actual_route} {' '.join(pixTools.leftKeys)}"
        return print(messages["unknownRoute"].format(good_routes, wrong_routes))

    PIX_STORE = {
        "Status": StatusRouter,
        "Add": AddRouter,
        "Remove": RemoveRouter,
        "Commit": CommitRouter,
        "Branch": BranchRouter,
        "Stash": StashRouter,
    }

    next_route = pixTools.getNextRoute()
    subroute = checkRoute(next_route, SUBROUTES[route_name])
    requiredRouter = PIX_STORE[route_name]

    requiredRouter(pixTools, subroute)


if __name__ == "__main__":
    main()
