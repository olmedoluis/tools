ALIASES = {
    "Status": {
        "aliases": ["w", "st"]
    },
    "Add": {
        "aliases": ["a"], 
        "child_aliases": {
            "ADD_ALL": ["."]
        }
    },
    "Remove": {
        "aliases": ["una", "rm"], 
        "child_aliases": {
            "REMOVE_ALL": ["."]
        }
    },
    "Commit": {
        "aliases": ["s", "c"],
    },
    "Branch": {
        "aliases": ["br"],
        "child_aliases": {
            "BRANCH_CREATION": ["cr"]
        }
    },
    "Stash": {
        "aliases": ["b"],
        "child_aliases": {
            "ADD_STASH": ["a", "i"]
        }
    },
    "Patch": {
        "aliases": ["e"]
    },
    "Reset": {
        "aliases": ["rs"],
        "child_aliases": {
            "RESET_ALL": ["."]
        }
    },
}
