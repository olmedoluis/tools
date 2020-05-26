#!/usr/bin/python3

path = "/home/luis/Documents/Projects/pix-bash"

ROUTES = {
    "Status": {
        "keys": ["status", "work"],
        "alias": ["w", "st"]
    },
    "Add": {
        "keys": ["add"],
        "alias": ["a"]
    },
    "Remove": {
        "keys": ["remove"],
        "alias": ["una", "rm"]
    }
}

SUBROUTES = {
    "Status": {},
    "Add": {
        "ADD_ALL": {
            "keys": ["all"],
            "alias": ["."]
        }
    },
    "Remove": {
        "REMOVE_ALL": {
            "keys": ["all"],
            "alias": ["."]
        }
    }
}
