RESET = "\x1b[0m"
BOLD = "\x1b[1m"
DIM = "\x1b[2m"

RED_LOW = "\x1b[31m"
YELLOW_LOW = "\x1b[33m"

RED_HIGH = "\x1b[91m"
GREEN_HIGH = "\x1b[92m"
BLUE_HIGH = "\x1b[94m"
MAGENTA_HIGH = "\x1b[95m"
WHITE_HIGH = "\x1b[97m"


THEME = {
    "th_normal": f"{BOLD}{WHITE_HIGH}",
    "th_success": f"{BOLD}{GREEN_HIGH}",
    "th_keyword": f"{BOLD}{MAGENTA_HIGH}",
    "th_added": f"{BOLD}{GREEN_HIGH}",
    "th_modified": f"{BOLD}{YELLOW_LOW}",
    "th_deleted": f"{BOLD}{RED_HIGH}",
    "th_untracked": f"{BOLD}{BLUE_HIGH}",
    "th_renamed": f"{BOLD}{RED_LOW}",
    "th_conflicted": f"{BOLD}{WHITE_HIGH}",
    "th_error": f"{BOLD}{RED_HIGH}",
    "th_change": YELLOW_LOW,
    "th_dim": DIM,
}
