#!/usr/bin/python3

import sys
from Data.PixRoutes import ROUTES, SUBROUTES
from Data.Messages import getMessages
from Modules import AddRouter, StatusRouter, BranchRouter, CommitRouter, RemoveRouter, StashRouter

messages = getMessages()

def checkRoute(keyword, routes):
    for entityId in routes:
        entity = routes[entityId]
        posibleRoutes = entity["keys"] + entity["alias"]

        if keyword in posibleRoutes:
            return entityId

    return "DEFAULT"


def checkPixShortcut(keyword):
    for entityId in ROUTES:
        entity = ROUTES[entityId]
        posibleRoutes = entity["keys"] + entity["alias"]

        if keyword in posibleRoutes:
            return entityId

    return False


def Router(route_name, pixTools):
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

    PIX_STORE[route_name](pixTools, subroute)


def run(pixTools):
    route_name = checkPixShortcut(pixTools.actual_route)

    if route_name != False:
        Router(route_name, pixTools)
    else:
        good_routes = f"pix {' '.join(pixTools.getGoodRoutes())}"
        wrong_routes = f"{pixTools.actual_route} {' '.join(pixTools.leftKeys)}"
        print(messages["unknownRoute"].format(good_routes, wrong_routes))


class PixTools():
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


arg = sys.argv[1:]

if(len(arg) != 0):
    pixTools = PixTools(arg)
    run(pixTools)
