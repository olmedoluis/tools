def logger(error_message="", logs=[], colors={}, icons={}, branch="master"):
    from .Console import ConsoleControl, getGetch
    from .CharactersInterpreter import get_movement

    getch = getGetch()
    input_console = ConsoleControl(lines="default")
    log_control = LogControl(
        offset=0,
        term_size_x=input_console.terminalWidth,
        term_size_y=input_console.terminalHeight - 2,
        logs=logs,
        colors=colors,
        icons=icons,
    )

    input_console.setConsoleLine(1, 2, branch)

    while True:
        for line_number in range(3, input_console.terminalHeight):
            text_to_show = log_control.get_styled_line(line_number - 3)
            input_console.setConsoleLine(line_number, 1, text_to_show)

        input_console.refresh()

        char = getch()
        state = get_movement(char, True)

        if state == "FINISH":
            break
        if state == "UP":
            log_control.add_to_index(-1)
        if state == "DOWN":
            log_control.add_to_index(1)
        elif state == "BREAK_CHAR":
            input_console.deleteLastLines(input_console.terminalHeight)
            input_console.finish()
            print(error_message)
            exit()

    input_console.deleteLastLines(input_console.terminalHeight)
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
        self.logs_size = len(logs)
        self.offset = 0
        self.log_number_hovered = 0

    def get_styled_line(self, line_number):

        color = (
            self._COLORS["selection"]
            if (line_number + self.offset) == self.log_number_hovered
            else self._COLORS["slight"]
        )

        if (line_number + self.offset) in range(self.logs_size):
            log = self.logs[line_number + self.offset]

            return f"{color}* {log.commit}{self._RESET}"

        return ""

    def get_index(self, index):
        # return index % self.logs_size
        if index > self.logs_size - 1:
            return self.logs_size - 1
        elif index < 0:
            return 0
        else:
            return index

    def add_to_index(self, number):
        self.log_number_hovered = self.get_index(self.log_number_hovered + number)

        is_up_half_window = self.log_number_hovered >= (self._term_size_y / 2)
        is_down_half_window = self.log_number_hovered <= (
            self.logs_size - (self._term_size_y / 2)
        )

        is_half_window = is_up_half_window
        has_scrollable_logs = (self.logs_size - self.offset) >= self._term_size_y

        if number < 0:
            is_half_window = is_down_half_window
            has_scrollable_logs = (
                self.offset > 0 and self.logs_size >= self._term_size_y
            )

        if is_half_window and has_scrollable_logs:
            self.increase_offset(number)

    def increase_offset(self, number):
        self.offset = self.offset + number
