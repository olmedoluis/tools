def bookSelection(lines=[], seleccionableLinesIncludes=[], colors={"": "\x1b[32m"}, errorMessage=""):
    from .Console import ConsoleControl, getGetch
    from .CharactersInterpreter import getMovement
    from os import popen

    _, terminalWidth = popen("stty size", "r").read().split()

    reset = "\x1b[0m"
    bold = "\x1b[1m"
    dim = "\x1b[2m"
    addedColor = "\x1b[32m"
    deletedColor = "\x1b[31m"

    getch = getGetch()
    inputConsole = ConsoleControl(9)
    textZoneArea = range(0, len(lines))
    selectionableArea = range(-4, len(lines) - 4)

    linesToSelect = []
    for index in textZoneArea:
        for selectionableInclusion in seleccionableLinesIncludes:
            if selectionableInclusion in lines[index]:
                linesToSelect.append(index - 4)

    offset = linesToSelect[0]
    indexLimits = range(0, len(linesToSelect))
    index = 0
    linesSelected = []

    def updateConsole():
        for lineNumber in range(0, 9):
            index = lineNumber + offset
            lineText = lines[index].strip() if index in textZoneArea else ""
            lineTextLimited = lineText[0 : int(terminalWidth) - 1]
            selectionColor = ""
            if index in linesSelected:
                option1, option2 = seleccionableLinesIncludes
                selectionColor = addedColor if lineText[0] == option1 else deletedColor

            lineTextColored = (
                f"{reset}{bold}{selectionColor}{lineTextLimited}"
                if lineNumber == 4
                else f"{reset}{dim}{selectionColor}{lineTextLimited}"
            )

            inputConsole.setConsoleLine(lineNumber, 1, lineTextColored)

        inputConsole.refresh()

    def saveLineText(shouldSave, text):
        symbol = text[0]
        lineNumber = offset + 4
        if lineNumber in linesSelected and not shouldSave:
            index = linesSelected.index(lineNumber)
            return linesSelected.pop(index)
        elif not lineNumber in linesSelected and shouldSave:
            linesSelected.append(lineNumber)

    while True:
        updateConsole()

        char = getch()
        state = getMovement(char)

        if state == "DOWN":
            newIndex = index + 1
            if newIndex in indexLimits:
                offset = linesToSelect[newIndex]
                index = newIndex
        elif state == "UP":
            newIndex = index - 1
            if newIndex in indexLimits:
                offset = linesToSelect[newIndex]
                index = newIndex
        elif state == "RIGHT":
            lineText = lines[offset + 4]
            saveLineText(True, lineText)
        elif state == "LEFT":
            lineText = lines[offset + 4]
            saveLineText(False, lineText)
        elif state == "FINISH":
            break
        elif state == "BREAK_CHAR":
            inputConsole.deleteLastLines(9)
            inputConsole.finish()
            print(errorMessage)
            exit()
    
    inputConsole.deleteLastLines(9)
    inputConsole.finish()

    return linesSelected

