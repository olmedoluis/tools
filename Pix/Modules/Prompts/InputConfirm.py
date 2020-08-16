def confirm(title="", finalTitle="", colors={}, errorMessage=""):
    from .Console import ConsoleControl, getGetch
    from .CharactersInterpreter import getResponse
    from .Theme import INPUT_THEME

    FONT_COLOR = ({**INPUT_THEME, **colors})["font"]
    getch = getGetch()
    inputConsole = ConsoleControl(1)

    word = False
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
            inputConsole.finish()
            print(errorMessage)
            exit()

    inputConsole.setConsoleLine(0, 1, f"{finalTitle} {FONT_COLOR}{word}")
    inputConsole.refresh()

    inputConsole.finish()

    return word

