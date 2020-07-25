RESET = "\u001b[0m"
CODE = "\u001b[38;5;"

THEME = {
    "th_normal": f"{CODE}15;1m",
    "th_success": f"{CODE}47;1m",
    "th_keyword": f"{CODE}171;1m",
    "th_added": f"{CODE}48;1m",
    "th_modified": f"{CODE}221;1m",
    "th_deleted": f"{CODE}203;1m",
    "th_untracked": f"{CODE}69;1m",
    "th_renamed": f"{CODE}203;1m",
    "th_conflicted": f"{CODE}209;1m",
    "th_error": f"{CODE}9;1m",
    "th_dim": "\u001b[2m",
    "th_reset": RESET,
}

ICONS = {"ic_modified": "☢", "ic_error": "✖", "ic_selection": "❤", "ic_normal": "•"}

INPUT_THEME = {
    "COMMIT_CREATION_TYPE": {"selection": f"{CODE}221;1m"},
    "COMMIT_CREATION_SCOPE": {},
    "COMMIT_CREATION_ABOUT": {},
    "COMMIT_CREATION_CONFIRM": {},
    "BRANCH_SELECTION": {"selection": f"{CODE}171;1m"},
    "BRANCH_CREATION_TYPE": {"selection": f"{CODE}221;1m"},
    "BRANCH_CREATION_ID": {},
    "BRANCH_CREATION_ABOUT": {},
    "BRANCH_CREATION_CONFIRM": {},
    "BRANCH_CREATION_SWITCH": {},
    "STASH_SELECTION": {},
    "STASH_CREATION_NAME": {},
    "PATCH_SELECTION": {},
}

INPUT_ICONS = {
    "+": ICONS["ic_modified"],
    "-": ICONS["ic_error"],
    "selection": ICONS["ic_selection"],
    "normal": ICONS["ic_normal"],
}


# import sys
#     for i in range(0, 16):
#         for j in range(0, 16):
#             code = str(i * 16 + j)
#             sys.stdout.write(u"\u001b[38;5;" + code + "m " + code.ljust(4))
#         print (u"\u001b[0m")
