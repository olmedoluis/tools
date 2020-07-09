def confirm(title="", finalTitle=""):
    from .Console import ConsoleControl, getGetch
    from .CharactersInterpreter import getResponse

    getch = getGetch()
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

