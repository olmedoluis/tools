def select(
    title="",
    final_title="",
    options=[""],
    error_message="",
    colors={},
    icons={},
):
    from .Console import ConsoleControl, getGetch
    from .CharactersInterpreter import get_movement

    getch = getGetch()
    input_console = ConsoleControl(5)
    select_control = _SelectControl(colors, icons, options)

    input_console.setConsoleLine(0, 1, title)

    while True:
        display_text = select_control.get_display_option(-1)
        input_console.setConsoleLine(2, 6, display_text)

        display_text = select_control.get_display_option(0)
        input_console.setConsoleLine(3, 4, display_text)

        display_text = select_control.get_display_option(1)
        input_console.setConsoleLine(4, 6, display_text)
        input_console.refresh()

        char = getch()
        state = get_movement(char)

        if state == "DOWN":
            select_control.append_to_index(1)
        elif state == "UP":
            select_control.append_to_index(-1)
        elif state == "FINISH" or state == "RIGHT":
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
    def __init__(self, colors, icons, options):
        from .Theme import INPUT_THEME, INPUT_ICONS

        self._SELECTION_ICON = ({**INPUT_ICONS, **icons})["selection"]
        self._COLORS = {**INPUT_THEME, **colors}
        self._RESET = self._COLORS["reset"]

        self._options = options
        self._options_size = len(options)
        self._option_index = 0

    def get_display_option(self, offset=0):
        font_color = self._COLORS["slight"] if offset else self._COLORS["selection"]
        option = self.get_option(offset)
        icon = "" if offset else f"{self._SELECTION_ICON} "

        return f"{font_color}{icon}{option}{self._RESET}"

    def get_option(self, offset=0):
        return self._options[(self._option_index + offset) % self._options_size]

    def append_to_index(self, number):
        self._option_index = self._option_index + number
