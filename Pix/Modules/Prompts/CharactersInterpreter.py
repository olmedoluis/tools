def get_parsed_char(char):
    char_upper = char.upper()
    char_code = ord(char)

    if char_code == 13:
        return "FINISH"

    elif char_code == 27:
        return "BREAK_CHAR"

    elif char == "\x7f":
        return "BACKSTAB"

    elif len(char) == 1:
        return char_upper

    else:
        return "UNKNOWN"
