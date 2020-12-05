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


class FiltersControl:
    def __init__(
        self,
        colors,
        place_holder='Press "F" to filter',
        active_place_holder="Write something here",
    ):
        self._COLORS = colors
        self._RESET = colors["reset"]
        self.filtering = ""
        self.is_filter_enabled = False
        self.place_holder = place_holder
        self.active_place_holder = active_place_holder

    def get_filter_value(self):
        slight = self._COLORS["slight"]
        color = self._COLORS["modification"] if self.is_filter_enabled else slight
        place_holder = (
            f"{slight}{self.active_place_holder}"
            if self.is_filter_enabled
            else self.place_holder
        )

        return (
            f"{color}{self.filtering}{self._RESET}"
            if self.filtering != ""
            else f"{color}{place_holder}{self._RESET}"
        )

    def toggle_filtering_mode(self):
        self.is_filter_enabled = not self.is_filter_enabled

    def set_filter(self, value):
        self.filtering = value
