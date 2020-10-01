ANSI = "\u001b["
CODE = f"{ANSI}38;5;"

THEME = {
    "th_added": f"{CODE}48;1m",
    "th_conflicted": f"{CODE}209;1m",
    "th_deleted": f"{CODE}203;1m",
    "th_dim": f"{ANSI}2m",
    "th_error": f"{CODE}9;1m",
    "th_keyword": f"{CODE}171;1m",
    "th_modified": f"{CODE}221;1m",
    "th_normal": f"{CODE}15;1m",
    "th_renamed": f"{CODE}203;1m",
    "th_reset": f"{ANSI}0m",
    "th_success": f"{CODE}47;1m",
    "th_untracked": f"{CODE}69;1m",
}

ICONS = {
    "ic_modified": "☢",
    "ic_untracked": "✱",
    "ic_renamed": "✦",
    "ic_deleted": "✝",
    "ic_conflicted": "■",
    "ic_added": "✚",
    "ic_error": "✖",
    "ic_selection": "❤",
    "ic_normal": "•",
    "ic_success": "⚑",
    "ic_branch": "⚲",
}

EMPTY = {}
INPUT_THEME = {
    "ADD_SELECTION": {"selection": f"{CODE}48;1m"},
    "BRANCH_CREATION_ABOUT": EMPTY,
    "BRANCH_CREATION_CONFIRM": EMPTY,
    "BRANCH_CREATION_ID": EMPTY,
    "BRANCH_CREATION_SWITCH": EMPTY,
    "BRANCH_CREATION_TYPE": {"selection": f"{CODE}221;1m"},
    "BRANCH_SELECTION": {"selection": f"{CODE}171;1m"},
    "COMMIT_CREATION_ABOUT": EMPTY,
    "COMMIT_CREATION_CONFIRM": EMPTY,
    "COMMIT_CREATION_SCOPE": EMPTY,
    "COMMIT_CREATION_TYPE": {"selection": f"{CODE}221;1m"},
    "PATCH_SELECTION": EMPTY,
    "REMOVE_SELECTION": {"selection": f"{CODE}9;1m"},
    "RESET_SELECTION": {"selection": f"{CODE}48;1m"},
    "STASH_CREATION_NAME": EMPTY,
    "STASH_SELECTION": EMPTY,
}

INPUT_ICONS = {
    "+": ICONS["ic_modified"],
    "-": ICONS["ic_error"],
    "selection": ICONS["ic_selection"],
    "normal": ICONS["ic_normal"],
}
