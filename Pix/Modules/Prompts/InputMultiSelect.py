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


def multiSelect(
    title="", finalTitle="", options=[""], errorMessage="", selectedColor="\x1b[32m"
):
    from .Console import ConsoleControl, getGetch
    from .CharactersInterpreter import getMovement

    getch = getGetch()
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
                f"{selectedColor}\x1b[1m" if optionSelected.state else "\x1b[1m\x1b[37m"
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
