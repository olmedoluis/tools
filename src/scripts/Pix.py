#!/usr/bin/python3

import sys
from PixRouter import Router
from PixRoutes import ROUTES
from Messages import getMessages

messages = getMessages()


def checkPixShortcut(keyword):
    for entityId in ROUTES:
        entity = ROUTES[entityId]
        posibleRoutes = entity["keys"] + entity["alias"]

        if keyword in posibleRoutes:
            return entityId

    return False


def run(router):
    route_name = checkPixShortcut(router.actual_route)

    if route_name != False:
        Router(route_name, router)
    else:
        good_routes = f"pix {' '.join(router.getGoodRoutes())}"
        wrong_routes = f"{router.actual_route} {' '.join(router.leftKeys)}"
        print(messages["unknownRoute"].format(good_routes, wrong_routes))


class mainRouter():
    def __init__(self, argv):
        self.user_routes = argv
        self.actual_route = argv[0]
        self.leftKeys = argv[1:]

    def runAgain(self, router):
        run(router)

    def getGoodRoutes(self):
        good_routes = []

        for route in self.user_routes:
            if route != self.actual_route:
                good_routes.append(route)
            else:
                break

        return good_routes


if __name__ == "__main__":
    arg = sys.argv[1:]
    if(len(arg) != 0):
        router = mainRouter(arg)
        run(router)
