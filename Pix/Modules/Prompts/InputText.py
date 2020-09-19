def text(
    title="", content="", place_holder="", final_title="", error_message="", colors={}
):
    from .Console import ConsoleControl, getGetch
    from .CharactersInterpreter import merge

    getch = getGetch()
    input_console = ConsoleControl(1)
    text_control = _TextControl(
        initial_text=content, place_holder=place_holder, colors=colors
    )

    while True:
        display_text = text_control.get_display_text()

        input_console.setConsoleLine(0, 1, f"{title} {display_text}")
        input_console.refresh()

        char = getch()
        new_text, state = merge(text_control.get_text(), char)
        text_control.set_text(new_text)

        if state == "FINISH":
            break
        if state == "BREAK_CHAR":
            input_console.finish()
            print(error_message)
            exit()

    final_title = final_title if final_title != "" else title
    display_text = text_control.get_text_absolute()

    input_console.setConsoleLine(0, 1, f"{final_title} {display_text}")
    input_console.refresh()

    input_console.finish()

    return text_control.get_text_absolute()


class _TextControl:
    def __init__(self, initial_text, place_holder, colors):
        from .Theme import INPUT_THEME

        self._text = initial_text
        self._place_holder = place_holder

        self._COLORS = {**INPUT_THEME, **colors}
        self._RESET = self._COLORS["reset"]

    def set_text(self, text):
        self._text = text

    def get_text(self):
        return self._text

    def get_text_absolute(self):
        return self._text if self._text != "" else self._place_holder

    def get_display_text(self):
        display_text = self.get_text_absolute()
        font_color = (
            self._COLORS["font"] if self._text != "" else self._COLORS["slight"]
        )

        return f"{font_color}{display_text}{self._RESET}"
