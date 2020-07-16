def patchSelect(lines=[], seleccionableLinesIncludes=[], fileName="", errorMessage=""):
    from .Console import ConsoleControl, getGetch
    from .CharactersInterpreter import getMovement
    from os import popen

    print("\n On " + fileName + "\n")

    terminalHeight, terminalWidth = popen("stty size", "r").read().split()
    terminalWidth = int(terminalWidth) - 1
    selectionAreaHeight = int(terminalHeight) - 4

    reset = "\x1b[0m"
    bold = "\x1b[1m"
    dim = "\x1b[2m"
    colors = {"+": f"{bold}\x1b[32m", "-": f"{bold}\x1b[31m"}
    border = f"\x1b[36m|{reset}"

    getch = getGetch()
    inputConsole = ConsoleControl(selectionAreaHeight)
    textZoneArea = range(0, len(lines))

    offset = 0
    patchesSelected = []

    def updateConsole():
        for lineNumber in range(0, selectionAreaHeight):
            index = lineNumber + offset
            lineText = lines[index].strip() if index in textZoneArea else ""
            lineTextLimited = lineText[0:terminalWidth]
            if len(lineText) and lineText[0] in colors:
                lineTextLimited = colors[lineText[0]] + lineTextLimited + reset
            else:
                lineTextLimited = dim + lineTextLimited + reset

            inputConsole.setConsoleLine(lineNumber, 1, f"{border}   {lineTextLimited}")

        inputConsole.refresh()

    def saveLineText(shouldSave, text):
        return
        patchesSelected.append(lineNumber)

    while True:
        updateConsole()

        char = getch()
        state = getMovement(char)

        if state == "DOWN":
            newOffset = offset + 1
            offset = newOffset if newOffset in textZoneArea and len(lines) > selectionAreaHeight else offset
        elif state == "UP":
            newOffset = offset - 1
            offset = newOffset if newOffset in textZoneArea else offset
        elif state == "RIGHT":
            lineText = lines[offset + 4]
            saveLineText(True, lineText)
        elif state == "LEFT":
            lineText = lines[offset + 4]
            saveLineText(False, lineText)
        elif state == "FINISH":
            break
        elif state == "BREAK_CHAR":
            inputConsole.deleteLastLines(selectionAreaHeight + 4)
            inputConsole.finish()
            print(errorMessage)
            exit()

    inputConsole.deleteLastLines(selectionAreaHeight)
    inputConsole.finish()

    return patchesSelected

