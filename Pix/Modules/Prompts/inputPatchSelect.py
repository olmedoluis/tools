def patchSelect(errorMessage="", files=[], colors={}, icons={}):
    from .Console import ConsoleControl, getGetch
    from .CharactersInterpreter import getMovement
    from .Theme import INPUT_THEME, INPUT_ICONS
    from os import popen

    terminalHeight, terminalWidth = popen("stty size", "r").read().split()
    terminalWidth = int(terminalWidth) - 1
    selectionAreaHeight = int(terminalHeight) - 1

    KEYWORDS = {"+": "modification", "-": "deletation"}
    COLORS = {**INPUT_THEME, **colors}
    ICONS = {**INPUT_ICONS, **icons}
    RESET = COLORS["reset"]

    getch = getGetch()
    inputConsole = ConsoleControl(selectionAreaHeight)
    patchControl = PatchControl(
        offset=0,
        termSizeX=terminalWidth,
        termSizeY=selectionAreaHeight,
        files=files,
        colors=COLORS,
        icons=ICONS,
    )

    patchControl.setPatchesOfFile(1)
    patchControl.setPatchShowing(0)

    def updateConsole():
        state = (
            COLORS["borderSel"]
            if patchControl.getIsPatchSelected()
            else COLORS["border"]
        )

        inputConsole.setConsoleLine(1, 2, patchControl.getFileIndexShown())
        inputConsole.setConsoleLine(3, 1, patchControl.getCurrentFileName())

        for lineNumber in range(5, selectionAreaHeight):
            textToShow = patchControl.getStyledPatchLine(lineNumber)
            color = COLORS["slight"]

            if textToShow != "":
                firstChar = textToShow[0]
                icon = ICONS[firstChar] if firstChar in ICONS else firstChar
                color = COLORS[KEYWORDS[firstChar]] if firstChar in KEYWORDS else color

                textToShow = color + icon + textToShow[1:] + COLORS["reset"]

            inputConsole.setConsoleLine(
                lineNumber, 1, f"{state}❚{RESET}   {textToShow}"
            )

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
    def __init__(self, offset, termSizeX, termSizeY, files, colors, icons):
        self.COLORS = colors
        self.RESET = colors["reset"]
        self.ICONS = icons
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
        index = lineNumber + self.offset - 5
        if not (index in self.textZoneArea):
            return ""

        lineText = self.patchShowing[index]
        return lineText[0 : self.termSizeX - 5]

    def getIsPatchSelected(self):
        return self.patchIndexSelected in self.files[self.fileNameIndex].patchesSelected

    def getCurrentFileName(self):
        return self.files[self.fileNameIndex].fileName

    def getPatchIndexShown(self):
        output = ""

        for index in range(0, len(self.patches)):
            active = self.COLORS["indexAct"] if index == self.patchIndexSelected else ""
            color = self.COLORS["index"]
            icon = self.ICONS["normal"]

            if index in self.files[self.fileNameIndex].patchesSelected:
                color = self.COLORS["indexSel"]
                icon = self.ICONS["selection"]

            output = f"{output}{color}{active} {icon}{self.RESET}"

        return f"{output} "

    def getFileIndexShown(self):
        output = ""

        for index in range(0, len(self.files)):
            color = self.COLORS["file"]
            extra = ""

            if index == self.fileNameIndex:
                color = self.COLORS["fileAct"]
                extra = self.getPatchIndexShown()

            output = f"{output}{color}|{self.RESET}{extra}"

        return output
