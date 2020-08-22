def multiSelect(
    title="", finalTitle="", options=[""], errorMessage="", colors={}, icons={},
):
    from .Console import ConsoleControl, getGetch
    from .CharactersInterpreter import getMovement

    getch = getGetch()
    inputConsole = ConsoleControl(5)
    multiSelectControl = _MultiSelectControl(colors, icons, options)

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
            multiSelectControl.addIndexToSelectedOptions()
        elif state == "LEFT":
            multiSelectControl.removeIndexToSelectedOptions()
        elif state == "FINISH":
            break
        elif state == "BREAK_CHAR":
            inputConsole.deleteLastLines(4)
            inputConsole.finish()

            print(errorMessage)
            exit()

    selectedOptions = multiSelectControl.getOptionsSelected()
    selectedOptionsString = ", ".join(selectedOptions)
    finalTitle = finalTitle if finalTitle != "" else title

    inputConsole.setConsoleLine(0, 1, f"{finalTitle} {selectedOptionsString}")
    inputConsole.refresh()

    inputConsole.deleteLastLines(4)
    inputConsole.finish()

    return selectedOptions


class _MultiSelectControl:
    def __init__(self, colors, icons, options):
        from .Theme import INPUT_THEME, INPUT_ICONS

        self._ICONS = {**INPUT_ICONS, **icons}
        self._COLORS = {**INPUT_THEME, **colors}
        self._RESET = self._COLORS["reset"]

        self._optionsSize = len(options)
        self._optionsRaw = options
        self._optionIndex = 0
        self._optionsSelected = []

    def getOptionsSelected(self):
        output = []
        for index in self._optionsSelected:
            output.append(self._optionsRaw[index])

        return output

    def getDisplayOption(self, offset=0):
        option = self.getOption(offset)
        indexInRange = self.getIndexInRange(self._optionIndex + offset)
        isSelected = self.getIsOptionSelected(indexInRange)

        fontMod = self._COLORS["slight"] if offset else self._COLORS["bold"]
        fontColor = self._COLORS["selection"] if isSelected else ""
        icon = self._ICONS["selection"] if isSelected else self._ICONS["normal"]

        return f"{fontMod}{fontColor}{option}{self._RESET}"

    def appendToIndex(self, number):
        self._optionIndex = self._optionIndex + number

    def getIndexInRange(self, index):
        return index % self._optionsSize

    def getOption(self, offset=0):
        return self._optionsRaw[self.getIndexInRange(self._optionIndex + offset)]

    def addIndexToSelectedOptions(self):
        if not self.getIsOptionSelected():
            self._optionsSelected.append(self.getIndexInRange(self._optionIndex))

    def removeIndexToSelectedOptions(self):
        if self.getIsOptionSelected():
            self._optionsSelected.remove(self.getIndexInRange(self._optionIndex))

    def getIsOptionSelected(self, index=None):
        if index == None:
            index = self.getIndexInRange(self._optionIndex)

        return index in self._optionsSelected
