def getOptionsWithStates(options):
    class opt:
        def __init__(self, content):
            self.state = False
            self.content = content

        def getStateString(self):
            return "❤" if self.state else "•"

        def setState(self, newState):
            self.state = newState

    output = []
    for option in options:
        output.append(opt(option))

    return output


def getOptionsSelected(options):
    output = []
    for option in options:
        if option.state:
            output.append(option)
    return output


def getOptionContents(options):
    output = []
    for option in options:
        if option.state:
            output.append(option.content)
    return output


def multiSelect(
    title="", finalTitle="", options=[""], errorMessage="", colors={}, icons={},
):
    from .Console import ConsoleControl, getGetch
    from .CharactersInterpreter import getMovement
    from .Theme import INPUT_THEME, INPUT_ICONS

    COLORS = {**INPUT_THEME, **colors}
    ICONS = {**INPUT_ICONS, **icons}
    RESET = COLORS["reset"]
    SLIGHT_SELECTION = COLORS["selection"] + COLORS["slight"]

    getch = getGetch()
    inputConsole = ConsoleControl(5)
    multiSelectControl = _MultiSelectControl(colors, icons, options)

    selectedOptions = []
    finalTitle = finalTitle if finalTitle != "" else title
    optionsWithStates = getOptionsWithStates(options)

    inputConsole.setConsoleLine(0, 1, title)

    while True:
        optionAbove = multiSelectControl.getDisplayOption(-1)
        optionSelected = multiSelectControl.getDisplayOption(0)
        optionDown = multiSelectControl.getDisplayOption(1)

        inputConsole.setConsoleLine(2, 4, optionAbove)
        inputConsole.setConsoleLine(3, 4, optionSelected)
        inputConsole.setConsoleLine(4, 4, optionDown)
        inputConsole.refresh()

        char = getch()
        state = getMovement(char)

        if state == "DOWN":
            multiSelectControl.appendToIndex(1)
        elif state == "UP":
            multiSelectControl.appendToIndex(-1)
        elif state == "RIGHT":
            multiSelectControl.setOptionState(True)
        elif state == "LEFT":
            multiSelectControl.setOptionState(False)
        elif state == "FINISH":
            break
        elif state == "BREAK_CHAR":
            print(errorMessage)
            exit()

    selectedOptionsWithStates = getOptionsSelected(optionsWithStates)
    selectedOptions = getOptionContents(selectedOptionsWithStates)
    selectedOptionsString = ", ".join(selectedOptions)

    inputConsole.setConsoleLine(0, 1, f"{finalTitle} {selectedOptionsString}")
    inputConsole.refresh()

    inputConsole.deleteLastLines(4)

    inputConsole.finish()
    return selectedOptions


class Option:
    selectionIcon = ""
    defaultIcon = ""

    def __init__(self, content):
        self.state = False
        self.content = content

    def getIcon(self):
        return self.selectionIcon if self.state else self.defaultIcon

    def setState(self, newState):
        self.state = newState


class _MultiSelectControl:
    def __init__(self, colors, icons, options):
        from .Theme import INPUT_THEME, INPUT_ICONS

        self._ICONS = {**INPUT_ICONS, **icons}
        self._COLORS = {**INPUT_THEME, **colors}
        self._RESET = self._COLORS["reset"]
        self._SLIGHT_SELECTION = self._COLORS["selection"] + self._COLORS["slight"]

        self._optionsSize = len(options)
        self._optionsRaw = options
        self._optionIndex = 0
        self._options = []

        for option in options:
            self._options.append(Option(option))

    def getOptionsSelected(options):
        output = []
        for option in self._options:
            if option.state:
                output.append(option)

        return output

    def getDisplayOption(self, offset=0):
        option = self.getOptionState(offset)
        fontMod = self._COLORS["slight"] if offset else self._COLORS["bold"]
        fontColor = self._COLORS["selection"] if option.state else ""
        icon = option.getIcon()

        return f"{fontMod}{fontColor}{icon}{option.content}{self._RESET}"

    def appendToIndex(self, number):
        self._optionIndex = self._optionIndex + number

    def getOption(self, offset=0):
        return self._optionsRaw[(self._optionIndex + offset) % self._optionsSize]

    def getOptionState(self, offset=0):
        return self._options[(self._optionIndex + offset) % self._optionsSize]

    def setOptionState(self, state, offset=0):
        self.getOptionState(offset).setState(state)
