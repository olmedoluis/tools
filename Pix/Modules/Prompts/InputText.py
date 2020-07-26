def text(
    title="", content="", placeHolder="", finalTitle="", errorMessage="", colors={}
):
    from .Console import ConsoleControl, getGetch
    from .CharactersInterpreter import merge
    from .Theme import INPUT_THEME

    getch = getGetch()
    inputConsole = ConsoleControl(1)

    COLORS = {**INPUT_THEME, **colors}
    RESET = COLORS["reset"]
    FONT_COLOR = COLORS["font"]

    word = content
    finalTitle = finalTitle if finalTitle != "" else title

    while True:
        wordToShow = word if word != "" else placeHolder
        color = FONT_COLOR if word != "" else COLORS["slight"]

        inputConsole.setConsoleLine(0, 1, f"{title} {color}{wordToShow}{RESET}")
        inputConsole.refresh()

        char = getch()
        newWord, state = merge(word, char)
        word = newWord

        if state == "FINISH":
            break
        if state == "BREAK_CHAR":
            print(errorMessage)
            inputConsole.finish()
            exit()

    inputConsole.setConsoleLine(0, 1, f"{finalTitle} {FONT_COLOR}{wordToShow}{RESET}")
    inputConsole.refresh()

    inputConsole.finish()

    return word if word != "" else placeHolder
