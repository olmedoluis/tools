#!/usr/bin/python3

import sys
import PixRoutes
import PixRouter


def checkPixShortcut(keyword):
    routes = PixRoutes.ROUTES

    for entityId in routes:
        entity = routes[entityId]
        posibleRoutes = entity["keys"] + entity["alias"]

        if keyword in posibleRoutes:
            return entityId

    return False


if __name__ == "__main__":
    arg = sys.argv[1:]
    if(len(arg) != 0):
        mainKey = arg[0]
        leftKeys = arg[1:]
        route = checkPixShortcut(mainKey)

        if route != False:
            PixRouter.Router(route, leftKeys)
