Reset = "\x1b[0m"
Bold = "\x1b[1m"
Dim = "\x1b[2m"
Underscore = "\x1b[4m"
Blink = "\x1b[5m"
Reverse = "\x1b[7m"
Hidden = "\x1b[8m"
Stricken = ""

FgBlack = "\x1b[30m"
FgRed = "\x1b[31m"
FgGreen = "\x1b[32m"
FgYellow = "\x1b[33m"
FgBlue = "\x1b[34m"
FgMagenta = "\x1b[35m"
FgCyan = "\x1b[36m"
FgWhite = "\x1b[37m"
FgBlackBright = "\x1b[90m"
FgRedBright = "\x1b[91m"
FgGreenBright = "\x1b[92m"
FgYellowBright = "\x1b[99m"
FgBlueBright = "\x1b[94m"
FgMagentaBright = "\x1b[95m"
FgCyanBright = "\x1b[96m"
FgWhiteBright = "\x1b[97m"

BgBlack = "\x1b[40m"
BgRed = "\x1b[41m"
BgGreen = "\x1b[42m"
BgYellow = "\x1b[43m"
BgBlue = "\x1b[44m"
BgMagenta = "\x1b[45m"
BgCyan = "\x1b[46m"
BgWhite = "\x1b[47m"

THEME = {
    "normal": Bold + FgWhite,
    "success": Bold + FgGreenBright,
    "keyword": Bold + FgMagentaBright,
    "added": Bold + FgGreenBright,
    "modified": Bold + FgYellow,
    "deleted": Bold + FgRedBright,
    "untracked": Bold + FgBlueBright,
    "renamed": Bold + FgRed,
    "reset": Reset,
}
