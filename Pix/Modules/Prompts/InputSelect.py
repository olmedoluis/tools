def select(
    title="", finalTitle="", options=[""], errorMessage="", colors={}, icons={},
):
    from .Console import ConsoleControl, getGetch
    from .CharactersInterpreter import getMovement

    getch = getGetch()
    inputConsole = ConsoleControl(5)
    selectControl = _SelectControl(colors, icons, options)

    inputConsole.setConsoleLine(0, 1, title)

    while True:
        displayText = selectControl.getDisplayOption(-1)
        inputConsole.setConsoleLine(2, 6, displayText)

        displayText = selectControl.getDisplayOption(0)
        inputConsole.setConsoleLine(3, 4, displayText)

        displayText = selectControl.getDisplayOption(1)
        inputConsole.setConsoleLine(4, 6, displayText)
        inputConsole.refresh()

        char = getch()
        state = getMovement(char)

        if state == "DOWN":
            selectControl.appendToIndex(1)
        elif state == "UP":
            selectControl.appendToIndex(-1)
        elif state == "FINISH" or state == "RIGHT":
            break
        elif state == "BREAK_CHAR":
            inputConsole.deleteLastLines(4)
            inputConsole.finish()
            print(errorMessage)
            exit()

    selectedOption = selectControl.getOption()
    finalTitle = finalTitle if finalTitle != "" else title

    inputConsole.setConsoleLine(0, 1, f"{finalTitle} {selectedOption}")
    inputConsole.refresh()
    inputConsole.deleteLastLines(4)
    inputConsole.finish()

    return selectedOption


class _SelectControl:
    def __init__(self, colors, icons, options):
        from .Theme import INPUT_THEME, INPUT_ICONS

        self._SELECTION_ICON = ({**INPUT_ICONS, **icons})["selection"]
        self._COLORS = {**INPUT_THEME, **colors}
        self._RESET = self._COLORS["reset"]

        self._options = options
        self._optionsSize = len(options)
        self._selectedOption = ""
        self._optionIndex = 0

    def getDisplayOption(self, offset=0):
        fontColor = self._COLORS["slight"] if offset else self._COLORS["selection"]
        option = self.getOption(offset)
        icon = "" if offset else f"{self._SELECTION_ICON} "

        return f"{fontColor}{icon}{option}{self._RESET}"

    def getOption(self, offset=0):
        return self._options[(self._optionIndex + offset) % self._optionsSize]

    def appendToIndex(self, number):
        self._optionIndex = self._optionIndex + number

