def patchSelect(lines=[], seleccionableLinesIncludes=[], fileName="", errorMessage=""):
    from .Console import ConsoleControl, getGetch
    from .CharactersInterpreter import getMovement
    from os import popen

    print("\n On " + fileName + "\n")

    _, terminalWidth = popen("stty size", "r").read().split()
    terminalWidth = int(terminalWidth) - 1

    reset = "\x1b[0m"
    bold = "\x1b[1m"
    dim = "\x1b[2m"
    colors = {"+": "\x1b[32m", "-": "\x1b[31m"}

    getch = getGetch()
    inputConsole = ConsoleControl(15)
    textZoneArea = range(0, len(lines))

    offset = 0
    patchesSelected = []

    def updateConsole():
        for lineNumber in range(0, 15):
            index = lineNumber + offset
            lineText = lines[index].strip() if index in textZoneArea else ""
            lineTextLimited = lineText[0:terminalWidth]
            if len(lineText) and lineText[0] in colors:
                lineTextLimited = colors[lineText[0]] + lineTextLimited + reset

            inputConsole.setConsoleLine(lineNumber, 1, lineTextLimited)

        inputConsole.refresh()

    def saveLineText(shouldSave, text):
        return
        patchesSelected.append(lineNumber)

    while True:
        updateConsole()

        char = getch()
        state = getMovement(char)

        if state == "DOWN":
            offset = offset + 1
        elif state == "UP":
            offset = offset - 1
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

    return patchesSelected

