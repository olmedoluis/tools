def logger(error_message="", logs=[], colors={}, icons={}, branch="master"):
    from .Console import ConsoleControl, getGetch
    from .CharactersInterpreter import get_movement

    getch = getGetch()
    input_console = ConsoleControl(lines="default")
    log_control = LogControl(
        offset=0,
        term_size_x=input_console.terminalWidth,
        term_size_y=input_console.terminalHeight,
        logs=logs,
        colors=colors,
        icons=icons,
    )

    input_console.setConsoleLine(1, 2, branch)

    while True:
        for line_number in range(3, len(logs) + 3):
            text_to_show = log_control.get_styled_line(line_number - 3)

            input_console.setConsoleLine(line_number, 1, text_to_show)

        input_console.refresh()

        char = getch()
        state = get_movement(char, True)

        if state == "FINISH":
            break
        elif state == "BREAK_CHAR":
            input_console.deleteLastLines(input_console.terminalHeight + 4)
            input_console.finish()
            print(error_message)
            exit()

    input_console.deleteLastLines(input_console.terminalHeight + 4)
    input_console.finish()

    return log_control.logs


class LogControl:
    def __init__(self, offset, term_size_x, term_size_y, logs, colors, icons):
        from .Theme import INPUT_THEME, INPUT_ICONS

        self._ICONS = {**INPUT_ICONS, **icons}
        self._COLORS = {**INPUT_THEME, **colors}
        self._RESET = self._COLORS["reset"]
        self._term_size_x = term_size_x
        self._term_size_y = term_size_y
        self.logs = logs
        self.offset = 0

    def get_styled_line(self, line_number):
        log = self.logs[line_number]

        return f"* {log.commit}"
