from .Console import ConsoleControl

def prompts():
    def getGetch():
        from os import name

        if name == "nt":
            import msvcrt

            return msvcrt.getch

        def getch():
            import sys
            import tty
            import termios

            try:
                fd = sys.stdin.fileno()
                old = termios.tcgetattr(fd)
            except:
                return chr(27)
            try:
                tty.setraw(fd)
                return sys.stdin.read(1)
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old)

        return getch

    getch = getGetch()

    def merge(word, char):
        if ord(char) == 13:
            return word, "FINISH"
        elif ord(char) == 27:
            return word, "BREAK_CHAR"
        elif char == "\x7f":
            return word[:-1], "BACKSPACE"
        elif len(char) == 1:
            return word + char, "VALID_CHAR"
        else:
            return word, "UNKNOWN"

    def getMovement(char):
        charLower = char.lower()

        if charLower == "a":
            return "LEFT"
        elif charLower == "d":
            return "RIGHT"
        elif charLower == "w":
            return "UP"
        elif charLower == "s":
            return "DOWN"
        elif ord(char) == 13:
            return "FINISH"
        elif ord(char) == 27:
            return "BREAK_CHAR"
        else:
            return "UNKNOWN"

    def getResponse(char):
        charLower = char.lower()

        if charLower == "y":
            return "YES"
        elif charLower == "n":
            return "NO"
        elif ord(char) == 13:
            return "FINISH"
        elif ord(char) == 27:
            return "BREAK_CHAR"
        else:
            return "UNKNOWN"

    def getOptionsWithStates(options):
        class opt:
            def __init__(self, content):
                self.state = False
                self.content = content

            def getStateString(self):
                return "❤" if self.state else "⚬"

            def setState(self, newState):
                self.state = newState

        output = []
        for option in options:
            output.append(opt(option))

        return output

    def getOptionsSelected(options):
        output = []
        for option in options:
            if option.state:
                output.append(option)
        return output

    def getOptionContents(options):
        output = []
        for option in options:
            if option.state:
                output.append(option.content)
        return output

    def textInput(title="", content="", placeHolder="", finalTitle="", errorMessage=""):
        inputConsole = ConsoleControl(1)
        word = content
        finalTitle = finalTitle if finalTitle != "" else title

        while True:
            wordToShow = word if word != "" else placeHolder
            inputConsole.setConsoleLine(0, 1, f"{title} {wordToShow}")
            inputConsole.refresh()

            char = getch()
            newWord, state = merge(word, char)
            word = newWord

            if state == "FINISH":
                break
            if state == "BREAK_CHAR":
                print(errorMessage)
                exit()

        inputConsole.setConsoleLine(0, 1, f"{finalTitle} {wordToShow}")
        inputConsole.refresh()

        inputConsole.finish()

        return word if word != "" else placeHolder

    def selectInput(
        title="", finalTitle="", options=[""], errorMessage="", selectedColor="\x1b[32m"
    ):
        inputConsole = ConsoleControl(5)
        selectedOption = ""
        try:
            finalTitle = finalTitle if finalTitle != "" else title
            index = 0
            optionsLen = len(options)

            inputConsole.setConsoleLine(0, 1, title)

            while True:
                color = "\x1b[2m"
                inputConsole.setConsoleLine(
                    2, 6, f"{color}{options[(index - 1) % optionsLen]}\x1b[0m"
                )

                color = selectedColor
                inputConsole.setConsoleLine(
                    3, 4, f"{color}\x1b[1m❤ {options[index % optionsLen]}\x1b[0m"
                )

                color = "\x1b[2m"
                inputConsole.setConsoleLine(
                    4, 6, f"{color}{options[(index + 1) % optionsLen]}\x1b[0m"
                )
                inputConsole.refresh()

                char = getch()
                state = getMovement(char)

                if state == "DOWN":
                    index = index + 1
                elif state == "UP":
                    index = index - 1
                elif state == "FINISH" or state == "RIGHT":
                    break
                elif state == "BREAK_CHAR":
                    print(errorMessage)
                    inputConsole.deleteLastLines(3)
                    exit()

            selectedOption = options[index % optionsLen]
            inputConsole.setConsoleLine(0, 1, f"{finalTitle} {selectedOption}")
            inputConsole.refresh()

        finally:
            inputConsole.deleteLastLines(4)

            inputConsole.finish()

            return selectedOption

    def confirmInput(title="", finalTitle=""):
        inputConsole = ConsoleControl(1)
        word = False
        try:
            finalTitle = finalTitle if finalTitle != "" else title

            while True:
                inputConsole.setConsoleLine(0, 1, f"{title}")
                inputConsole.refresh()

                char = getch()
                state = getResponse(char)

                if state == "YES":
                    word = True
                    break
                if state == "NO":
                    word = False
                    break
                if state == "FINISH":
                    break
                if state == "BREAK_CHAR":
                    exit()

            inputConsole.setConsoleLine(0, 1, f"{finalTitle} {word}")
            inputConsole.refresh()

        finally:
            inputConsole.finish()

            return word

    def multiSelectInput(
        title="", finalTitle="", options=[""], errorMessage="", selectedColor="\x1b[32m"
    ):
        inputConsole = ConsoleControl(5)
        selectedOptions = []
        try:
            finalTitle = finalTitle if finalTitle != "" else title
            index = 0
            optionsLen = len(options)
            optionsWithStates = getOptionsWithStates(options)

            inputConsole.setConsoleLine(0, 1, title)

            while True:
                optionAbove = optionsWithStates[(index - 1) % optionsLen]
                optionSelected = optionsWithStates[index % optionsLen]
                optionDown = optionsWithStates[(index + 1) % optionsLen]

                color = selectedColor if optionAbove.state else "\x1b[2m"
                inputConsole.setConsoleLine(
                    2,
                    4,
                    f"{color}{optionAbove.getStateString()} {optionAbove.content}\x1b[0m",
                )

                color = (
                    f"{selectedColor}\x1b[1m"
                    if optionSelected.state
                    else "\x1b[1m\x1b[37m"
                )
                inputConsole.setConsoleLine(
                    3,
                    4,
                    f"{color}{optionSelected.getStateString()} {optionSelected.content}\x1b[0m",
                )

                color = selectedColor if optionDown.state else "\x1b[2m"
                inputConsole.setConsoleLine(
                    4,
                    4,
                    f"{color}{optionDown.getStateString()} {optionDown.content}\x1b[0m",
                )

                inputConsole.refresh()

                char = getch()
                state = getMovement(char)

                if state == "DOWN":
                    index = index + 1
                elif state == "UP":
                    index = index - 1
                elif state == "RIGHT":
                    optionSelected.setState(True)
                elif state == "LEFT":
                    optionSelected.setState(False)
                elif state == "FINISH":
                    break
                elif state == "BREAK_CHAR":
                    print(errorMessage)
                    exit()

            selectedOptionsWithStates = getOptionsSelected(optionsWithStates)
            selectedOptions = getOptionContents(selectedOptionsWithStates)
            selectedOptionsString = ", ".join(selectedOptions)

            inputConsole.setConsoleLine(0, 1, f"{finalTitle} {selectedOptionsString}")
            inputConsole.refresh()

        except:
            inputConsole.deleteLastLines(1)
            selectedOptions = "UNKNOWN_ERROR"

        finally:
            inputConsole.deleteLastLines(4)

            inputConsole.finish()
            return selectedOptions

    class prompts_ui:
        def __init__(self):
            self.box = {
                "MultiSelect": multiSelectInput,
                "Text": textInput,
                "Select": selectInput,
                "Confirm": confirmInput,
            }

        def text(self, **arg):
            return textInput(**arg)

        def select(self, **arg):
            return selectInput(**arg)

        def confirm(self, **arg):
            return confirmInput(**arg)

        def multiSelect(self, **arg):
            return multiSelectInput(**arg)

        def many(self, inputs):
            output = []
            for inputData in inputs:
                currentInput = self.box[inputData["type"]]
                inputData.pop("type")
                out = currentInput(**inputData)
                if out == "":
                    break
                output.append(out)

            return output

    return prompts_ui()
