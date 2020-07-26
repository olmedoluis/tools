class PixTools:
    def __init__(self, argv):
        self.user_routes = argv
        self.actual_route = argv[0]
        self.leftKeys = argv[1:]

    def getGoodRoutes(self):
        goodRoutes = []

        for route in self.user_routes:
            if route != self.actual_route:
                goodRoutes.append(route)
            else:
                break

        return goodRoutes

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
    from sys import argv

    arg = argv[1:]

    if len(arg) == 0:
        return

    from Configuration import ALIASES
    from .Data.PixRoutes import KEYS
    from .Modules import PIX_STORE
    from .Modules.Helpers import checkPixShortcut, checkRoute

    allRoutes = getConcatenatedRoutes(arg) if "n" in arg else [arg]

    for arguments in allRoutes:
        pixTools = PixTools(arguments)

        routeName = checkPixShortcut(pixTools.actual_route, KEYS, ALIASES)

        if routeName == False:
            from .Modules.Helpers import MessageControl

            goodRoutes = f"pix {' '.join(pixTools.getGoodRoutes())}"
            wrongRoutes = f"{pixTools.actual_route} {' '.join(pixTools.leftKeys)}"
            m = MessageControl()

            return m.log(
                "unknownRoute",
                {"pm_goodRoutes": goodRoutes, "pm_wrongRoutes": wrongRoutes},
            )

        next_route = pixTools.getNextRoute()
        subroute = checkRoute(next_route, KEYS[routeName], ALIASES[routeName])

        requiredRouter = PIX_STORE[routeName]
        requiredRouter(pixTools, subroute)


if __name__ == "__main__":
    main()
