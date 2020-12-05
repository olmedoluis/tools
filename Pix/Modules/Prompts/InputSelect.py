def select(
    title="",
    final_title="",
    options=[""],
    error_message="",
    colors={},
    icons={},
):
    from .Console import ConsoleControl, getGetch
    from .CharactersInterpreter import get_parsed_char

    getch = getGetch()
    input_console = ConsoleControl(5)
    select_control = _SelectControl(colors, icons, options, title)

    while True:
        display_text = select_control.get_display_title()
        input_console.setConsoleLine(0, 1, display_text)

        display_text = select_control.get_display_option(-1)
        input_console.setConsoleLine(2, 6, display_text)

        display_text = select_control.get_display_option(0)
        input_console.setConsoleLine(3, 4, display_text)

        display_text = select_control.get_display_option(1)
        input_console.setConsoleLine(4, 6, display_text)
        input_console.refresh()

        char = getch()
        state = get_parsed_char(char)
        is_filter_enabled = select_control.get_is_filter_enabled()

        if is_filter_enabled and state == "FINISH":
            select_control.toggle_filtering_mode()
        elif is_filter_enabled and len(state) == 1:
            select_control.set_filtering(select_control.get_filtering() + char)
        elif is_filter_enabled and state == "BACKSTAB":
            select_control.set_filtering(select_control.get_filtering()[:-1])
        elif state == "F":
            select_control.toggle_filtering_mode()
        elif state == "S":
            select_control.append_to_index(1)
        elif state == "W":
            select_control.append_to_index(-1)
        elif state == "FINISH" or state == "D":
            break
        elif state == "BREAK_CHAR":
            input_console.deleteLastLines(4)
            input_console.finish()
            print(error_message)
            exit()

    selected_option = select_control.get_option()
    final_title = final_title if final_title != "" else title

    input_console.setConsoleLine(0, 1, f"{final_title} {selected_option}")
    input_console.refresh()
    input_console.deleteLastLines(4)
    input_console.finish()

    return selected_option


class _SelectControl:
    def __init__(self, colors, icons, options, title):
        from .Theme import INPUT_THEME, INPUT_ICONS
        from .CharactersInterpreter import FiltersControl

        self._SELECTION_ICON = ({**INPUT_ICONS, **icons})["selection"]
        self._COLORS = {**INPUT_THEME, **colors}
        self._RESET = self._COLORS["reset"]

        self._options = options
        self._options_size = len(options)
        self._option_index = 0

        self._options_filtered = options
        self.title = title

        self.filtersControl = FiltersControl(self._COLORS)

    def get_display_option(self, offset=0):
        font_color = self._COLORS["slight"] if offset else self._COLORS["selection"]
        option = self.get_option(offset)
        icon = "" if offset else f"{self._SELECTION_ICON} "

        return f"{font_color}{icon}{option}{self._RESET}"

    def get_option(self, offset=0):
        return (
            self._options_filtered[(self._option_index + offset) % self._options_size]
            if self._options_size
            else "None"
        )

    def append_to_index(self, number):
        self._option_index = self._option_index + number

    def toggle_filtering_mode(self):
        self.filtersControl.toggle_filtering_mode()

    def get_display_title(self):
        filter_value = self.filtersControl.get_filter_value()

        return f"{self.title} {filter_value}"

    def set_filtering(self, new_value):
        new_filter_options = []

        for option in self._options:
            if new_value in option:
                new_filter_options.append(option)

        self._options_size = len(new_filter_options)
        self._options_filtered = new_filter_options

        self.filtersControl.set_filter(new_value)

    def get_is_filter_enabled(self):
        return self.filtersControl.is_filter_enabled

    def get_filtering(self):
        return self.filtersControl.filtering
