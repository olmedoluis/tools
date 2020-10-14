from pprint import pprint


def logger(error_message="", logs=[], colors={}, icons={}, branch="master", fetch=""):
    from .Console import ConsoleControl, getGetch
    from .CharactersInterpreter import get_parsed_char

    getch = getGetch()
    input_console = ConsoleControl(lines="default")
    log_control = LogControl(
        offset=0,
        term_size_x=input_console.terminalWidth,
        term_size_y=input_console.terminalHeight - 7,
        logs=logs,
        colors=colors,
        icons=icons,
        fetch=fetch,
    )

    input_console.setConsoleLine(1, 2, branch)

    while True:
        point = input_console.terminalHeight - 5
        for line_number in range(3, point):
            text_to_show = log_control.get_styled_line(line_number - 3)
            input_console.setConsoleLine(line_number, 1, text_to_show)

        log_info = log_control.get_styled_info()
        for line_number in range(4):
            input_console.setConsoleLine(
                point + line_number + 1, 1, log_info[line_number]
            )

        input_console.refresh()

        char = getch()
        state = get_parsed_char(char)

        if len(state) == 1 and log_control.is_filter_enabled:
            log_control.set_filters(log_control.get_filter() + char)

        elif state == "BACKSTAB":
            log_control.set_filters(log_control.get_filter()[:-1])

        elif state == "FINISH":
            if not log_control.is_filter_enabled:
                break

            log_control.re_fetch()
            log_control.set_is_filter_enabled(False)

        elif state == "F":
            log_control.set_is_filter_enabled(True)

        elif state == "W":
            log_control.add_to_index(-1)

        elif state == "S":
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
    def __init__(self, offset, term_size_x, term_size_y, logs, colors, icons, fetch):
        from .Theme import INPUT_THEME, INPUT_ICONS

        self._ICONS = {**INPUT_ICONS, **icons}
        self._COLORS = {**INPUT_THEME, **colors}
        self._RESET = self._COLORS["reset"]
        self.filters_control = FiltersControl(fetch=fetch)

        self._term_size_x = term_size_x
        self._term_size_y = term_size_y
        self.logs = logs
        self.logs_size = len(logs)
        self.offset = 0
        self.log_number_hovered = 0
        self.is_filter_enabled = False

        empty = "None"
        self.default_log = Log(
            hash=empty, author=empty, time=empty, commit=empty, date=empty
        )

    def set_filters(self, filters):
        self.filters_control.set_filters(filters)

    def get_filter(self):
        return self.filters_control.get_filter()

    def re_fetch(self):
        self.logs = self.filters_control.get_updated_filters(self.logs)
        self.logs_size = len(self.logs)
        self.offset = 0
        self.log_number_hovered = 0

    def set_is_filter_enabled(self, state):
        self.is_filter_enabled = state

    def get_styled_line(self, line_number):
        if self.logs_size and (line_number + self.offset) in range(self.logs_size):
            color = (
                self._COLORS["selection"]
                if (line_number + self.offset) == self.log_number_hovered
                else self._COLORS["slight"]
            )
            icon = (
                self._ICONS["log_selection"] + " "
                if (line_number + self.offset) == self.log_number_hovered
                else self._ICONS["log_normal"]
            )

            log = self.logs[line_number + self.offset]

            return f"{color}{icon} {log.commit}{self._RESET}"

        return ""

    def get_styled_info(self):
        log = self.logs[self.log_number_hovered] if self.logs_size else self.default_log
        border = "−" * (self._term_size_x - 2)
        color = self._COLORS["font"]
        border_color = self._COLORS["border"]
        filters = self.filters_control.get_filter()
        filters_section = f" | Filters: {filters}" if self.is_filter_enabled else ""

        return [
            f"{border_color}{border}{self._RESET}",
            "",
            f"{color}Relative Time: {log.time} | Date: {log.date}{self._RESET}",
            f"{color}Author: {log.author}{filters_section}{self._RESET}",
        ]

    def get_index(self, index):
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


class FiltersControl:
    def __init__(self, fetch):
        from re import search

        self.search = search
        self.filter_commands = {
            "date_to": lambda date: [f"--until={date}"],
            "date_from": lambda date: [f"--since={date}"],
            "contains": lambda text: [f"--grep={text}"],
            "date": self.get_date_command,
            "author": self.get_author_command,
            "show": self.get_show_command,
        }
        self.filter_keys = {
            "date": ["d", "date"],
            "date_to": ["dt", "until", "to"],
            "date_from": ["df", "from"],
            "contains": ["c", "contains"],
            "author": ["a", "author"],
            "show": ["s", "show"],
        }
        self.fetch = fetch
        self.filters_raw = ""

    def get_updated_filters(self, default_value=[]):
        return self.fetch(filters=self.parse_filter_string(self.filters_raw))

    def set_filters(self, filters):
        self.filters_raw = filters

    def get_filter(self):
        return self.filters_raw

    def parse_filter_string(self, string):
        output = []

        for filter_name in self.filter_keys:
            keys = "|".join(self.filter_keys[filter_name])

            match = self.search(f"(({keys})\.(\S+))", string)

            if match:
                value = match.group(3)
                output = output + self.filter_commands[filter_name](value)

        return output

    def get_date_command(self, dates_raw):
        dates = dates_raw.split(".")
        filter_format = [
            self.filter_commands["date_from"],
            self.filter_commands["date_to"],
        ]
        output = []

        if len(dates) == 1:
            dates.append(dates[0] + " 23:59")
            dates[0] = dates[0] + " 00:00"

        for index in range(2):
            if index >= len(dates) or dates[index] == "":
                continue

            output = output + filter_format[index](dates[index])

        return output

    def get_author_command(self, authors_raw):
        authors = authors_raw.split(".")
        authors_formatted = "\|".join(authors)

        return [f"--author={authors_formatted}"]

    def get_show_command(self, shows_raw):
        shows = shows_raw.split(".")
        output = []

        for show in shows:
            if show == "all":
                output.append("--all")
            elif show == "current":
                output.append("--first-parent")

        return output


class Log:
    def __init__(self, hash, author, time, commit, date):
        self.hash = hash
        self.author = author
        self.time = time
        self.date = date
        self.commit = commit
