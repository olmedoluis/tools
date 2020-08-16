def text(
    title="", content="", placeHolder="", finalTitle="", errorMessage="", colors={}
):
    from .Console import ConsoleControl, getGetch
    from .CharactersInterpreter import merge

    getch = getGetch()
    inputConsole = ConsoleControl(1)
    textControl = _TextControl(
        initialText=content, placeHolder=placeHolder, colors=colors
    )

    while True:
        displayText = textControl.getDisplayText()

        inputConsole.setConsoleLine(0, 1, f"{title} {displayText}")
        inputConsole.refresh()

        char = getch()
        newText, state = merge(textControl.getText(), char)
        textControl.setText(newText)

        if state == "FINISH":
            break
        if state == "BREAK_CHAR":
            print(errorMessage)
            inputConsole.finish()
            exit()

    finalTitle = finalTitle if finalTitle != "" else title
    displayText = textControl.getTextAbsolute()

    inputConsole.setConsoleLine(0, 1, f"{finalTitle} {displayText}")
    inputConsole.refresh()

    inputConsole.finish()

    return textControl.getTextAbsolute()


class _TextControl:
    def __init__(self, initialText, placeHolder, colors):
        from .Theme import INPUT_THEME

        self._text = initialText
        self._placeHolder = placeHolder

        self.COLORS = {**INPUT_THEME, **colors}
        self.RESET = self.COLORS["reset"]

    def setText(self, text):
        self._text = text

    def getText(self):
        return self._text

    def getTextAbsolute(self):
        return self._text if self._text != "" else self._placeHolder

    def getDisplayText(self):
        displayText = self.getTextAbsolute()
        fontColor = self.COLORS["font"] if self._text != "" else self.COLORS["slight"]

        return f"{fontColor}{displayText}{self.RESET}"
