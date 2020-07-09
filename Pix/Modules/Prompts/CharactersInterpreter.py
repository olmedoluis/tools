def merge(word, char):
    if ord(char) == 13:
        return word, "FINISH"
    elif ord(char) == 27:
        return word, "BREAK_CHAR"
    elif char == "\x7f":
        return word[:-1], "BACKSPACE"
    elif len(char) == 1:
        return word + char, "VALID_CHAR"
    else:
        return word, "UNKNOWN"


def getMovement(char):
    charLower = char.lower()

    if charLower == "a":
        return "LEFT"
    elif charLower == "d":
        return "RIGHT"
    elif charLower == "w":
        return "UP"
    elif charLower == "s":
        return "DOWN"
    elif ord(char) == 13:
        return "FINISH"
    elif ord(char) == 27:
        return "BREAK_CHAR"
    else:
        return "UNKNOWN"


def getResponse(char):
    charLower = char.lower()

    if charLower == "y":
        return "YES"
    elif charLower == "n":
        return "NO"
    elif ord(char) == 13:
        return "FINISH"
    elif ord(char) == 27:
        return "BREAK_CHAR"
    else:
        return "UNKNOWN"
