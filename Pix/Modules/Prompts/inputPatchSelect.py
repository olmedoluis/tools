def patchSelect(
    lines=[], seleccionableLinesIncludes=[], fileName="", errorMessage="", patches=[]
):
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
    borders = {
        "selected": f"\x1b[32m{bold}|{reset}",
        "notSelected": f"\x1b[31m{bold}|{reset}",
    }

    getch = getGetch()
    inputConsole = ConsoleControl(selectionAreaHeight)

    offset = 0
    patchIndexesSelected = []
    patchIndexSelected = 0
    patchShowing = patches[0][1:]
    textZoneArea = range(0, len(patchShowing))

    # options[index % optionsLen]

    def updateConsole():
        patchShowing = patches[patchIndexSelected][1:]
        textZoneArea = range(0, len(patchShowing))
        border = (
            borders["selected"]
            if patchIndexSelected in patchIndexesSelected
            else borders["notSelected"]
        )

        for lineNumber in range(0, selectionAreaHeight):
            index = lineNumber + offset
            lineText = patchShowing[index].strip() if index in textZoneArea else ""
            lineTextLimited = lineText[0:terminalWidth]
            if len(lineText) and lineText[0] in colors:
                lineTextLimited = colors[lineText[0]] + lineTextLimited + reset
            else:
                lineTextLimited = dim + lineTextLimited + reset

            inputConsole.setConsoleLine(lineNumber, 1, f"{border}   {lineTextLimited}")

        inputConsole.refresh()

    while True:
        updateConsole()

        char = getch()
        state = getMovement(char)

        if state == "DOWN":
            newOffset = offset + 1
            offset = (
                newOffset
                if newOffset in textZoneArea and len(lines) > selectionAreaHeight
                else offset
            )
        elif state == "UP":
            newOffset = offset - 1
            offset = newOffset if newOffset in textZoneArea else offset
        elif state == "RIGHT":
            patchIndexSelected = (patchIndexSelected + 1) % len(patches)
        elif state == "LEFT":
            patchIndexSelected = (patchIndexSelected - 1) % len(patches)
        elif state == "EXTENDED_RIGHT" and not (
            patchIndexSelected in patchIndexesSelected
        ):
            patchIndexesSelected.append(patchIndexSelected)
        elif state == "EXTENDED_LEFT" and patchIndexSelected in patchIndexesSelected:
            patchIndexesSelected.remove(patchIndexSelected)
        elif state == "FINISH":
            break
        elif state == "BREAK_CHAR":
            inputConsole.deleteLastLines(selectionAreaHeight + 4)
            inputConsole.finish()
            print(errorMessage)
            exit()

    inputConsole.deleteLastLines(selectionAreaHeight + 4)
    inputConsole.finish()

    patchesOutput = []
    for index in patchIndexesSelected:
        patchesOutput.append(patches[index])

    return patchesOutput

