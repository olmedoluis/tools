def bookSelection(lines=[], seleccionableLinesIncludes=[]):
    from .Console import ConsoleControl, getGetch
    from .CharactersInterpreter import getMovement
    import os

    _, terminalWidth = os.popen("stty size", "r").read().split()

    reset = "\x1b[0m"
    bold = "\x1b[1m"
    dim = "\x1b[2m"

    getch = getGetch()
    inputConsole = ConsoleControl(9)
    textZoneArea = range(0, len(lines))
    selectionableArea = range(-2, len(lines) - 4)

    offset = 0

    def updateConsole():
        for lineNumber in range(0, 9):
            index = lineNumber + offset
            lineText = lines[index].strip() if index in textZoneArea else ""
            lineTextLimited = lineText[0 : int(terminalWidth) - 1]
            lineTextColored = (
                f"{reset}{bold}{lineTextLimited}"
                if lineNumber == 4
                else f"{reset}{dim}{lineTextLimited}"
            )

            inputConsole.setConsoleLine(lineNumber, 1, lineTextColored)

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

