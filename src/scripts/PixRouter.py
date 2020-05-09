import Status

PIX_STORE = {
    "Status": Status
}


def Router(route_name, router):
    PIX_STORE[route_name].Router(router)
