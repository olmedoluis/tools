def bookSelection(lines=[]):
    from .Console import ConsoleControl, getGetch
    from .CharactersInterpreter import getMovement
    import os

    _, terminalWidth = os.popen("stty size", "r").read().split()

    getch = getGetch()
    inputConsole = ConsoleControl(10)
    maxLines = len(lines)

    offset = 0

    def updateConsole():
        for lineNumber in range(0, 10):
            index = lineNumber + offset
            lineText = lines[index].strip() if index < maxLines and index > 0 else ""

            inputConsole.setConsoleLine(
                lineNumber, 1, lineText[0 : int(terminalWidth) - 1]
            )

        inputConsole.refresh()

    while True:
        updateConsole()

        char = getch()
        state = getMovement(char)

        if state == "DOWN":
            offset = offset + 1
        elif state == "UP":
            offset = offset - 1
        elif state == "FINISH" or state == "RIGHT":
            break
        elif state == "BREAK_CHAR":
            # print(errorMessage)
            inputConsole.deleteLastLines(3)
            exit()

    inputConsole.finish()

    return ""

