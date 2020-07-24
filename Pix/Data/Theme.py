RESET = "\x1b[0m" + "\u001b[0m"
BOLD = "\u001b[1m"
DIM = "\x1b[2m"

RED_LOW = "\x1b[31m"
YELLOW_LOW = "\x1b[33m"

RED_HIGH = "\x1b[91m"
GREEN_HIGH = "\x1b[92m"
BLUE_HIGH = "\x1b[94m"
MAGENTA_HIGH = "\x1b[95m"
WHITE_HIGH = "\x1b[97m"
CODE = u"\u001b[38;5;"

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
    "th_dim": u"\u001b[2m"
}


# import sys
#     for i in range(0, 16):
#         for j in range(0, 16):
#             code = str(i * 16 + j)
#             sys.stdout.write(u"\u001b[38;5;" + code + "m " + code.ljust(4))
#         print (u"\u001b[0m")
