def multi_select(
    title="",
    final_title="",
    options=[""],
    error_message="",
    colors={},
    icons={},
):
    from .Console import ConsoleControl, getGetch
    from .Tools import get_parsed_char

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

    options_values, options_display = multi_select_control.get_options_selected()
    selected_options_string = ", ".join(options_display)

    final_title = final_title if final_title != "" else title

    input_console.setConsoleLine(0, 1, f"{final_title} {selected_options_string}")
    input_console.refresh()

    input_console.deleteLastLines(4)
    input_console.finish()

    return options_values


class _MultiSelectControl:
    def __init__(self, colors, icons, options, title):
        from .Theme import INPUT_THEME, INPUT_ICONS
        from .Tools import FiltersControl

        self._ICONS = {**INPUT_ICONS, **icons}
        self._COLORS = {**INPUT_THEME, **colors}
        self._RESET = self._COLORS["reset"]

        self._options_size = len(options)
        self._options_raw = options
        self._options_filtered = options
        self._option_index = 0
        self._options_selected = []

        self.title = title
        self.filtersControl = FiltersControl(self._COLORS)

    def get_options_selected(self):
        options_selected_values = []
        options_selected_display = []

        for selected_option_id in self._options_selected:
            for option in self._options_raw:
                if option["id"] == selected_option_id:
                    options_selected_values.append(option["value"])
                    options_selected_display.append(option["display_name"])
                    break

        return options_selected_values, options_selected_display

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
        return index % self._options_size if self._options_size else 0

    def get_option(self, offset=0):
        return (
            self._options_filtered[
                self.get_index_in_range(self._option_index + offset)
            ]["display_name"]
            if self._options_size
            else "None"
        )

    def _get_option_id_from_index(self, index):
        return self._options_filtered[index]["id"]

    def add_index_to_selected_options(self):
        if not self.get_is_option_selected():
            index = self.get_index_in_range(self._option_index)

            self._options_selected.append(self._get_option_id_from_index(index))

    def remove_index_to_selected_options(self):
        if self.get_is_option_selected():
            index = self.get_index_in_range(self._option_index)

            self._options_selected.remove(self._get_option_id_from_index(index))

    def get_is_option_selected(self, index=None):
        if index == None:
            index = self.get_index_in_range(self._option_index)

        option_id = self._get_option_id_from_index(index)

        return option_id in self._options_selected

    def toggle_filtering_mode(self):
        self.filtersControl.toggle_filtering_mode()

    def get_display_title(self):
        filter_value = self.filtersControl.get_filter_value()

        return f"{self.title} {filter_value}"

    def set_filtering(self, new_value):
        new_filter_options = []

        for option in self._options_raw:
            if new_value in option["display_name"]:
                new_filter_options.append(option)

        self._options_size = len(new_filter_options)
        self._options_filtered = new_filter_options
        self.filtersControl.set_filter(new_value)

    def get_is_filter_enabled(self):
        return self.filtersControl.is_filter_enabled

    def get_filtering(self):
        return self.filtersControl.filtering