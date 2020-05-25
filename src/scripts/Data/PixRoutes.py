#!/usr/bin/python3

path = "/home/luis/Documents/Projects/pix-bash"

ROUTES = {
    "Status": {
        "keys": ["status", "work"],
        "alias": ["w", "st"]
    }
}

SUBROUTES = {
    "Status": {
        "ADD_IGNORE_FILE": {
            "keys": ["ignore"],
            "alias": ["i"]
        }
    }
}
