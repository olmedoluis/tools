import Status


def Router(route_name, pixTools):
    PIX_STORE = {
        "Status": Status
    }

    PIX_STORE[route_name].Router(pixTools)
