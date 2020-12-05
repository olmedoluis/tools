def multi_select(
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
    multi_select_control = _MultiSelectControl(colors, icons, options, title)

    while True:
        input_console.setConsoleLine(0, 1, multi_select_control.get_display_title())

        option_above = multi_select_control.get_display_option(-1)
        option_selected = multi_select_control.get_display_option(0)
        option_down = multi_select_control.get_display_option(1)

        input_console.setConsoleLine(2, 4, option_above)
        input_console.setConsoleLine(3, 4, option_selected)
        input_console.setConsoleLine(4, 4, option_down)
        input_console.refresh()

        char = getch()
        state = get_parsed_char(char)
        is_filter_enabled = multi_select_control.get_is_filter_enabled()

        if is_filter_enabled and state == "FINISH":
            multi_select_control.toggle_filtering_mode()
        elif is_filter_enabled and len(state) == 1:
            multi_select_control.set_filtering(
                multi_select_control.get_filtering() + char
            )
        elif is_filter_enabled and state == "BACKSTAB":
            multi_select_control.set_filtering(
                multi_select_control.get_filtering()[:-1]
            )
        elif state == "F":
            multi_select_control.toggle_filtering_mode()
        elif state == "S":
            multi_select_control.append_to_index(1)
        elif state == "W":
            multi_select_control.append_to_index(-1)
        elif state == "D":
            multi_select_control.add_index_to_selected_options()
        elif state == "A":
            multi_select_control.remove_index_to_selected_options()
        elif state == "FINISH":
            break
        elif state == "BREAK_CHAR":
            input_console.deleteLastLines(4)
            input_console.finish()

            print(error_message)
            exit()

    selected_options = multi_select_control.get_options_selected()
    selected_options_string = ", ".join(selected_options)
    final_title = final_title if final_title != "" else title

    input_console.setConsoleLine(0, 1, f"{final_title} {selected_options_string}")
    input_console.refresh()

    input_console.deleteLastLines(4)
    input_console.finish()

    return selected_options


class _MultiSelectControl:
    def __init__(self, colors, icons, options, title):
        from .Theme import INPUT_THEME, INPUT_ICONS
        from .CharactersInterpreter import FiltersControl

        self._ICONS = {**INPUT_ICONS, **icons}
        self._COLORS = {**INPUT_THEME, **colors}
        self._RESET = self._COLORS["reset"]

        self._options_size = len(options)
        self._options_raw = options
        self._option_index = 0
        self._options_selected = []

        self.title = title
        self.filtersControl = FiltersControl(self._COLORS)

    def get_options_selected(self):
        output = []
        for index in self._options_selected:
            output.append(self._options_raw[index])

        return output

    def get_display_option(self, offset=0):
        option = self.get_option(offset)
        index_in_range = self.get_index_in_range(self._option_index + offset)
        is_selected = self.get_is_option_selected(index_in_range)

        font_mod = self._COLORS["slight"] if offset else self._COLORS["bold"]
        font_color = self._COLORS["selection"] if is_selected else self._COLORS["file"]
        icon = self._ICONS["selection"] if is_selected else self._ICONS["normal"]

        return f"{font_mod}{font_color}{option}{self._RESET}"

    def append_to_index(self, number):
        self._option_index = self._option_index + number

    def get_index_in_range(self, index):
        return index % self._options_size

    def get_option(self, offset=0):
        return self._options_raw[self.get_index_in_range(self._option_index + offset)]

    def add_index_to_selected_options(self):
        if not self.get_is_option_selected():
            self._options_selected.append(self.get_index_in_range(self._option_index))

    def remove_index_to_selected_options(self):
        if self.get_is_option_selected():
            self._options_selected.remove(self.get_index_in_range(self._option_index))

    def get_is_option_selected(self, index=None):
        if index == None:
            index = self.get_index_in_range(self._option_index)

        return index in self._options_selected

    def toggle_filtering_mode(self):
        self.filtersControl.toggle_filtering_mode()

    def get_display_title(self):
        filter_value = self.filtersControl.get_filter_value()

        return f"{self.title} {filter_value}"

    def set_filtering(self, new_value):
        new_filter_options = []

        self.filtersControl.set_filter(new_value)

    def get_is_filter_enabled(self):
        return self.filtersControl.is_filter_enabled

    def get_filtering(self):
        return self.filtersControl.filtering