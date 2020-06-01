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
    },
    "Commit": {
        "keys": ["commit", "save"],
        "alias": ["s", "c"]
    },
    "Branch": {
        "keys": ["branch", "line"],
        "alias": ["br"]
    },
    "Stash": {
        "keys": ["stash", "box"],
        "alias": ["b"]
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
    },
    "Commit": {},
    "Branch": {
        "BRANCH_CREATION": {
            "keys": ["create", "new"],
            "alias": ["cr"]
        }
    },
    "Stash": {
        "ADD_STASH": {
            "keys": ["add", "in"],
            "alias": ["a", "i"]
        }
    },
}
