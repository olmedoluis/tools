from time import sleep
import getch
from ConsoleControl import console


# prompts({
#     "type": "multitext",
#     "title": "que ondis?",
#     "placeholder": "weon",
#     "children": [{"name": "type", "placeholder": "feat", "title": "escribi el tipo:"}, {"name": "type", "placeholder": "feat", "title": "escribi el scope:"}, {"name": "about"}],
#     "template": "{}({}):{}"
# })

class prompt():
    def __init__(self, variety, title="", placeHolder="", children=[], template=""):
        self.variety = variety
        self.title = title
        self.placeHolder = placeHolder
        self.children = children
        self.template = template


def simpleTextInput(data):
    currentPrompt = prompt(**data)
    word = ""
    title = f" {currentPrompt.title}"
    placeHolder = currentPrompt.placeHolder

    print()
    while True:
        wordShown = word if word != "" else placeHolder
        formatedWord = f"\t{wordShown}$C"
        myTerm.show([title, "", formatedWord])
        myTerm.refresh()
        char = getch.getch()
        if not char.isalpha():
            break
        word += char
    print()

    return word if word != "" else placeHolder


myTerm = console(0)

try:
    simpleTextInput({
        "variety": "multitext",
        "title": "que ondis?",
        "placeHolder": "weon"
    })
finally:
    myTerm.finish()
exit()


# simpleTextInput({
#     "variety": "multitext",
#     "title": "que ondis?",
#     "placeHolder": "weon"
# })
