def select(
    title="", finalTitle="", options=[""], errorMessage="", selectedColor="\x1b[32m"
):
    from .Console import ConsoleControl, getGetch
    from .CharactersInterpreter import getMovement
    from .Theme import INPUT_THEME, INPUT_ICONS

    inputConsole = ConsoleControl(5)
    getch = getGetch()
    RESET = INPUT_THEME["reset"]

    selectedOption = ""

    try:
        finalTitle = finalTitle if finalTitle != "" else title
        index = 0
        optionsLen = len(options)

        inputConsole.setConsoleLine(0, 1, title)

        while True:
            color = INPUT_THEME["slight"]
            inputConsole.setConsoleLine(
                2, 6, f"{color}{options[(index - 1) % optionsLen]}{RESET}"
            )

            color = INPUT_THEME["selection"]
            inputConsole.setConsoleLine(
                3, 4, f"{color}❤ {options[index % optionsLen]}{RESET}"
            )

            color = INPUT_THEME["slight"]
            inputConsole.setConsoleLine(
                4, 6, f"{color}{options[(index + 1) % optionsLen]}{RESET}"
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

