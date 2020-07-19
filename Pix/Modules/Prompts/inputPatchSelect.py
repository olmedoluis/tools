def patchSelect(errorMessage="", files=[]):
    from .Console import ConsoleControl, getGetch
    from .CharactersInterpreter import getMovement
    from os import popen

    terminalHeight, terminalWidth = popen("stty size", "r").read().split()
    terminalWidth = int(terminalWidth) - 1
    selectionAreaHeight = int(terminalHeight) - 1

    reset = "\x1b[0m"
    bold = "\x1b[1m"
    dim = "\x1b[2m"
    colors = {"+": f"{bold}\x1b[33m", "-": f"{bold}\x1b[31m"}
    borders = {
        "+": f"\x1b[32m{bold}❚{reset}",
        "-": f"\x1b[37m{bold}❚{reset}",
    }
    icons = {"+": "☢", "-": "✖"}

    getch = getGetch()
    inputConsole = ConsoleControl(selectionAreaHeight)
    patchControl = PatchControl(
        offset=0, termSizeX=terminalWidth, termSizeY=selectionAreaHeight, files=files,
    )

    patchControl.setPatchesOfFile(1)
    patchControl.setPatchShowing(0)

    def updateConsole():
        border = borders["+"] if patchControl.getIsPatchSelected() else borders["-"]
        inputConsole.setConsoleLine(1, 2, patchControl.getFileIndexShown())
        inputConsole.setConsoleLine(3, 1, patchControl.getCurrentFileName())

        for lineNumber in range(5, selectionAreaHeight):
            lineTextLimited = patchControl.getStyledPatchLine(lineNumber)
            textToShow = ""

            if lineTextLimited:
                firstChar = lineTextLimited[0]

                lineTextLimited = (
                    icons[firstChar] + lineTextLimited[1:]
                    if firstChar in icons
                    else lineTextLimited
                )

                lineTextLimited = (
                    colors[firstChar] + lineTextLimited
                    if firstChar in colors
                    else dim + lineTextLimited
                ) + reset

                textToShow = f"   {lineTextLimited}"

            inputConsole.setConsoleLine(lineNumber, 1, f"{border}{textToShow}")

        inputConsole.refresh()

    while True:
        updateConsole()

        char = getch()
        state = getMovement(char, True)

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
        elif state == "YES":
            patchControl.addIndexSelectedToPatch()
            patchControl.changePage(1)
        elif state == "NO":
            patchControl.removeIndexSelectedToPatch()
            patchControl.changePage(-1)
        elif state == "FINISH":
            break
        elif state == "BREAK_CHAR":
            inputConsole.deleteLastLines(selectionAreaHeight + 4)
            inputConsole.finish()
            print(errorMessage)
            exit()

    inputConsole.deleteLastLines(selectionAreaHeight + 4)
    inputConsole.finish()

    return patchControl.files


class PatchControl:
    def __init__(self, offset, termSizeX, termSizeY, files):
        self.patches = []
        self.offset = offset
        self.termSizeX = termSizeX
        self.termSizeY = termSizeY
        self.patchIndexSelected = 0
        self.patchIndexesSelected = []
        self.patchShowing = []
        self.textZoneArea = range(0)
        self.fileNameIndex = 0
        self.files = files

    def setPatchesOfFile(self, times):
        self.patches = self.files[self.fileNameIndex].patches
        # self.patchIndexSelected = self.patchIndexSelected % len(self.patches)
        self.patchIndexSelected = 0 if times > 0 else len(self.patches) - 1

    def setPatchShowing(self, index):
        self.patchShowing = self.patches[index][1:]
        self.textZoneArea = range(0, len(self.patchShowing))

    def decreaseOffset(self):
        newOffset = self.offset - 1
        self.offset = newOffset if newOffset in self.textZoneArea else self.offset

    def increaseOffset(self):
        newOffset = self.offset + 1
        self.offset = (
            newOffset
            if newOffset in self.textZoneArea
            and (len(self.patchShowing) > self.termSizeY)
            and (newOffset < (len(self.patchShowing) * 0.5))
            else self.offset
        )

    def changePage(self, times):
        newIndex = self.patchIndexSelected + times
        self.patchIndexSelected = newIndex % len(self.patches)

        if not (newIndex in range(len(self.patches))) and len(self.files) > 1:
            self.fileNameIndex = (self.fileNameIndex + times) % len(self.files)
            self.setPatchesOfFile(times)

        self.setPatchShowing(self.patchIndexSelected)
        self.offset = 0

    def addIndexSelectedToPatch(self):
        if not self.getIsPatchSelected():
            self.files[self.fileNameIndex].patchesSelected.append(
                self.patchIndexSelected
            )

    def removeIndexSelectedToPatch(self):
        if self.getIsPatchSelected():
            self.files[self.fileNameIndex].patchesSelected.remove(
                self.patchIndexSelected
            )

    def getStyledPatchLine(self, lineNumber):
        index = lineNumber + self.offset - 4
        if not (index in self.textZoneArea):
            return False

        lineText = self.patchShowing[index]
        return lineText[0 : self.termSizeX]

    def getIsPatchSelected(self):
        return self.patchIndexSelected in self.files[self.fileNameIndex].patchesSelected

    def getCurrentFileName(self):
        return self.files[self.fileNameIndex].fileName

    def getPatchIndexShown(self):
        output = ""

        for index in range(0, len(self.patches)):
            colorCode = "\x1b[36m" if index == self.patchIndexSelected else ""

            output = (
                output
                + (
                    f"\x1b[1m\x1b[32m{colorCode} ❤"
                    if index in self.files[self.fileNameIndex].patchesSelected
                    else f"\x1b[1m\x1b[37m{colorCode} •"
                )
                + "\x1b[0m"
            )

        return output + " "

    def getFileIndexShown(self):
        output = ""

        for index in range(0, len(self.files)):
            output = output + (
                "\x1b[1m\x1b[35m|\x1b[0m" + self.getPatchIndexShown()
                if index == self.fileNameIndex
                else "\x1b[1m\x1b[37m|\x1b[0m"
            )

        return output
