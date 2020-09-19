def confirm(title="", final_title="", colors={}, error_message=""):
    from .Console import ConsoleControl, getGetch
    from .CharactersInterpreter import get_response
    from .Theme import INPUT_THEME

    FONT_COLOR = ({**INPUT_THEME, **colors})["font"]
    getch = getGetch()
    input_console = ConsoleControl(1)

    word = False

    while True:
        input_console.setConsoleLine(0, 1, f"{title}")
        input_console.refresh()

        char = getch()
        state = get_response(char)

        if state == "YES":
            word = True
            break
        elif state == "NO":
            word = False
            break
        elif state == "FINISH":
            break
        elif state == "BREAK_CHAR":
            input_console.finish()
            print(error_message)
            exit()

    final_title = final_title if final_title != "" else title

    input_console.setConsoleLine(0, 1, f"{final_title} {FONT_COLOR}{word}")
    input_console.refresh()
    input_console.finish()

    return word
