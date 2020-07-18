def patchSelect(
    seleccionableLinesIncludes=[], fileName="", errorMessage="", patches=[]
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
        "+": f"\x1b[32m{bold}|{reset}",
        "-": f"\x1b[31m{bold}|{reset}",
    }

    getch = getGetch()
    inputConsole = ConsoleControl(selectionAreaHeight)
    patchControl = PatchControl(
        offset=0,
        termSizeX=terminalWidth,
        termSizeY=selectionAreaHeight,
        patches=patches,
    )

    patchControl.setPatchShowing(0)

    def updateConsole():
        border = borders["+"] if patchControl.getIsPatchSelected() else borders["-"]

        for lineNumber in range(0, selectionAreaHeight):
            lineTextLimited = patchControl.getStyledPatchLine(lineNumber)
            textToShow = ""

            if lineTextLimited:
                firstChar = lineTextLimited[0]
                lineTextLimited = (
                    colors[firstChar] + lineTextLimited + reset
                    if firstChar in colors
                    else dim + lineTextLimited + reset
                )
                textToShow = f"   {lineTextLimited}"

            inputConsole.setConsoleLine(lineNumber, 1, f"{border}{textToShow}")

        inputConsole.refresh()

    while True:
        updateConsole()

        char = getch()
        state = getMovement(char)

        if state == "DOWN":
            patchControl.increaseOffset()
        elif state == "UP":
            patchControl.decreaseOffset()
        elif state == "RIGHT":
            patchControl.changePage(1)
        elif state == "LEFT":
            patchControl.changePage(-1)
        elif state == "EXTENDED_RIGHT":
            patchControl.addIndexSelectedToPatch()
        elif state == "EXTENDED_LEFT":
            patchControl.removeIndexSelectedToPatch()
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


class PatchControl:
    def __init__(self, patches, offset, termSizeX, termSizeY):
        self.patches = patches
        self.offset = offset
        self.termSizeX = termSizeX
        self.termSizeY = termSizeY
        self.patchIndexSelected = 0
        self.patchIndexesSelected = []
        self.patchShowing = []
        self.textZoneArea = range(0)

    def setPatchShowing(self, index):
        self.patchShowing = self.patches[index][1:]
        self.textZoneArea = range(0, len(self.patchShowing))

    def decreaseOffset(self):
        newOffset = self.offset - 1
        self.offset = newOffset if newOffset in self.textZoneArea else self.offset

    def increaseOffset(self):
        newOffset = self.offset + 1
        offset = (
            newOffset
            if newOffset in self.textZoneArea
            and (len(self.patchShowing) > self.termSizeY)
            and (newOffset < (len(self.patchShowing) * 0.5))
            else self.offset
        )

    def changePage(self, times):
        self.patchIndexSelected = (self.patchIndexSelected + times) % len(self.patches)
        self.setPatchShowing(self.patchIndexSelected)
        self.offset = 0

    def addIndexSelectedToPatch(self):
        if not self.getIsPatchSelected():
            self.patchIndexesSelected.append(self.patchIndexSelected)

    def removeIndexSelectedToPatch(self):
        if self.getIsPatchSelected():
            self.patchIndexesSelected.remove(self.patchIndexSelected)

    def getStyledPatchLine(self, lineNumber):
        index = lineNumber + self.offset
        if not (index in self.textZoneArea):
            return False

        lineText = self.patchShowing[index].strip()
        return lineText[0 : self.termSizeX]

    def getIsPatchSelected(self):
        return self.patchIndexSelected in self.patchIndexesSelected
