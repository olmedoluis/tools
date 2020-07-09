def select(
    title="", finalTitle="", options=[""], errorMessage="", selectedColor="\x1b[32m"
):
    from .Console import ConsoleControl, getGetch
    from .CharactersInterpreter import getMovement

    inputConsole = ConsoleControl(5)
    getch = getGetch()

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

