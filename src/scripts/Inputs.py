from time import sleep
import getch
from ConsoleControl import console


# simpleTextInput({
#     "variety": "single-text",
#     "title": "que ondis?",
#     "placeHolder": "weon"
# })


# multiTextInput({
#     "variety": "multitext",
#     "title": "que ondis?",
#     "placeHolder": "weon",
#     "children": [{"variety": "type", "placeHolder": "feat", "title": "escribi el tipo:"}, {"variety": "type", "placeHolder": "scope", "title": "tira el scope:"}, {"variety": "type", "title": "escribi la descri:"}],
#     "template": "{0}({1}):{2}"
# })

def merge(word, char):
    if char == "\n":
        return word + char, "FINISH"
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


def getIndexValue(array, index, defaultValue=""):
    return array[index] if index < len(array) else defaultValue


def setIndexValue(array, index, value):
    if index < len(array):
        array[index] = value
    else:
        array.append(value)

    return array


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
        inputConsole.setConsoleLine(2, 4, options[(index - 1) % optionsLen])
        inputConsole.setConsoleLine(3, 4, options[index % optionsLen])
        inputConsole.setConsoleLine(4, 4, options[(index + 1) % optionsLen])
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


options = ["feature", "refactor", "bugfix", "style"]
output = selectInput(title="me das la data gil?", options=options)
# output = textInput(title="algo", placeHolder="answer")
print("output", output)

exit()
