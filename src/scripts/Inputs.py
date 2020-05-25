def prompts():
    import getch
    from ConsoleControl import console

    def merge(word, char):
        if char == "\n":
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
        elif char == "\n":
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
        elif char == "\n":
            return "FINISH"
        elif ord(char) == 27:
            return "BREAK_CHAR"
        else:
            return "UNKNOWN"

    def getOptionsWithStates(options):
        class opt():
            def __init__(self, content):
                self.state = False
                self.content = content

            def getStateString(self):
                return "+" if self.state else "-"

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
        inputConsole = console(1)
        finalTitle = finalTitle if finalTitle != "" else title
        word = content

        while True:
            wordToShow = word if word != "" else placeHolder
            inputConsole.setConsoleLine(0, 1, f"{title} {wordToShow}")
            inputConsole.refresh()

            char = getch.getch()
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

    def selectInput(title="", finalTitle="", options=[""], errorMessage=""):
        inputConsole = console(5)
        finalTitle = finalTitle if finalTitle != "" else title
        index = 0
        optionsLen = len(options)

        inputConsole.setConsoleLine(0, 1, title)

        while True:
            inputConsole.setConsoleLine(
                2, 4, options[(index - 1) % optionsLen])
            inputConsole.setConsoleLine(3, 4, options[index % optionsLen])
            inputConsole.setConsoleLine(
                4, 4, options[(index + 1) % optionsLen])
            inputConsole.refresh()

            char = getch.getch()
            state = getMovement(char)

            if state == "DOWN":
                index = index + 1
            elif state == "UP":
                index = index - 1
            elif state == "FINISH":
                break
            elif state == "BREAK_CHAR":
                print(errorMessage)
                exit()

        selectedOption = options[index % optionsLen]
        inputConsole.setConsoleLine(0, 1, f"{finalTitle} {selectedOption}")
        inputConsole.refresh()
        inputConsole.deleteLastLines(4)

        inputConsole.finish()

        return selectedOption

    def confirmInput(title="", content="", finalTitle="", errorMessage=""):
        inputConsole = console(1)
        finalTitle = finalTitle if finalTitle != "" else title
        word = content

        while True:
            inputConsole.setConsoleLine(0, 1, f"{title} {word}")
            inputConsole.refresh()

            char = getch.getch()
            state = getResponse(char)

            if state == "YES":
                word = "yes"
                break
            if state == "NO":
                word = "no"
                break
            if state == "FINISH":
                break
            if state == "BREAK_CHAR":
                print(errorMessage)
                exit()

        inputConsole.setConsoleLine(0, 1, f"{finalTitle} {word}")
        inputConsole.refresh()

        inputConsole.finish()

        return word

    def multiSelectInput(title="", finalTitle="", options=[""], errorMessage=""):
        inputConsole = console(5)
        finalTitle = finalTitle if finalTitle != "" else title
        index = 0
        optionsLen = len(options)
        optionsWithStates = getOptionsWithStates(options)

        inputConsole.setConsoleLine(0, 1, title)

        while True:
            optionAbove = optionsWithStates[(index - 1) % optionsLen]
            optionSelected = optionsWithStates[index % optionsLen]
            optionDown = optionsWithStates[(index + 1) % optionsLen]

            inputConsole.setConsoleLine(
                2, 4, f"{optionAbove.getStateString()} {optionAbove.content}")

            inputConsole.setConsoleLine(
                3, 4, f"{optionSelected.getStateString()} {optionSelected.content}")

            inputConsole.setConsoleLine(
                4, 4, f"{optionDown.getStateString()} {optionDown.content}")

            inputConsole.refresh()

            char = getch.getch()
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

        selectedOptions = getOptionsSelected(optionsWithStates)
        selectedOptionsString = ", ".join(getOptionContents(selectedOptions))

        inputConsole.setConsoleLine(
            0, 1, f"{finalTitle} {selectedOptionsString}")
        inputConsole.refresh()
        inputConsole.deleteLastLines(4)

        inputConsole.finish()

        return selectedOptions

    class prompts_ui():
        def text(self, **arg):
            return textInput(**arg)

        def select(self, **arg):
            return selectInput(**arg)

        def confirm(self, **arg):
            return confirmInput(**arg)

        def multiSelect(self, **arg):
            return multiSelectInput(**arg)

    return prompts_ui()
