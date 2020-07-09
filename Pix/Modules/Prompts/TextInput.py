def textInput(title="", content="", placeHolder="", finalTitle="", errorMessage=""):
    from .Console import ConsoleControl, getGetch
    from .CharactersInterpreter import merge

    getch = getGetch()
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
