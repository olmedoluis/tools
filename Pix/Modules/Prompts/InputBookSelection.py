def bookSelection(lines=[], seleccionableLinesIncludes=[]):
    from .Console import ConsoleControl, getGetch
    from .CharactersInterpreter import getMovement
    import os

    _, terminalWidth = os.popen("stty size", "r").read().split()

    getch = getGetch()
    inputConsole = ConsoleControl(9)
    textZoneArea = range(0, len(lines))
    selectionableArea = range(-3, len(lines) - 3)

    offset = 0

    def updateConsole():
        for lineNumber in range(0, 9):
            index = lineNumber + offset
            lineText = lines[index].strip() if index in textZoneArea else ""
            lineTextLimited = lineText[0 : int(terminalWidth) - 1]

            inputConsole.setConsoleLine(lineNumber, 1, lineTextLimited)

        inputConsole.refresh()

    while True:
        updateConsole()

        char = getch()
        state = getMovement(char)

        if state == "DOWN":
            newOffset = offset + 1
            offset = newOffset if newOffset in selectionableArea else offset
        elif state == "UP":
            newOffset = offset - 1
            offset = newOffset if newOffset in selectionableArea else offset
        elif state == "FINISH" or state == "RIGHT":
            break
        elif state == "BREAK_CHAR":
            # print(errorMessage)
            # inputConsole.deleteLastLines(3)
            exit()

    inputConsole.finish()

    return ""

