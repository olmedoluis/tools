import Status

PIX_STORE = {
    "Status": Status
}


def Router(route, leftKeys):
    PIX_STORE[route].Router(leftKeys)
