KEYS = {
    "Status": {
        "keys": ["status", "work"]
    },
    "Add": {
        "keys":["add"], 
        "child_keys": {
            "ADD_ALL": ["all"]
        }
    },
    "Remove": {
        "keys": ["remove"], 
        "child_keys": {
            "REMOVE_ALL": ["all"]
        }
    },
    "Commit": {
        "keys": ["commit"],
    },
    "Branch": {
        "keys": ["branch"],
        "child_keys": {
            "BRANCH_CREATION": ["create", "new"]
        }
    },
    "Stash": {
        "keys": ["stash"],
        "child_keys": {
            "ADD_STASH": ["add", "in"]
        }
    },
}
