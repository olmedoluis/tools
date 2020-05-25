import Status
from PixRoutes import SUBROUTES


def checkRoute(keyword, routes):
    for entityId in routes:
        entity = routes[entityId]
        posibleRoutes = entity["keys"] + entity["alias"]

        if keyword in posibleRoutes:
            return entityId

    return "DEFAULT"


def Router(route_name, pixTools):
    PIX_STORE = {
        "Status": Status
    }

    next_route = pixTools.getNextRoute()
    subroute = checkRoute(next_route, SUBROUTES[route_name])

    PIX_STORE[route_name].Router(pixTools, subroute)
