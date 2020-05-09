#!/usr/bin/python3

import sys
from PixRouter import Router
from PixRoutes import ROUTES
from Messages import getMessages


def checkPixShortcut(keyword):
    for entityId in ROUTES:
        entity = ROUTES[entityId]
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
            Router(route, leftKeys)
        else:
            print()
