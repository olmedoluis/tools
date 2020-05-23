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
    def __init__(self, variety, title="", placeHolder="", children=[], template="", content=""):
        self.variety = variety
        self.title = title
        self.placeHolder = placeHolder
        self.children = children
        self.template = template
        self.content = content


def simpleTextInput(data):
    myTerm = console(2)

    currentPrompt = prompt(**data)
    word = ""
    title = f" {currentPrompt.title}"
    placeHolder = currentPrompt.placeHolder

    while True:
        wordShown = word if word != "" else placeHolder
        formatedWord = f"\t{wordShown}$C"
        myTerm.show([title, "", formatedWord])
        myTerm.refresh()
        char = getch.getch()
        if not char.isalpha():
            break
        word += char

    return word if word != "" else placeHolder


class ShownValue():
    def __init__(self, placeHolder):
        self.placeHolder = placeHolder
        self.showPlaceHolder = True

    def getValue(self, string):
        if self.showPlaceHolder == True and string == "":
            return self.placeHolder

        elif self.showPlaceHolder == False and string == "":
            self.showPlaceHolder = True
            return self.placeHolder

        elif self.showPlaceHolder == True and string == self.placeHolder:
            self.showPlaceHolder = False
            return self.placeHolder

        output = string.replace(
            self.placeHolder, "") if self.showPlaceHolder == True else string
        return output


def multiTextInput(data):
    myTerm = console(2)

    word = ""
    currentPrompt = prompt(**data)
    children = currentPrompt.children
    index = 0
    childrenAvailable = len(children)

    childrenContents = []
    childrenPlaceHolders = []
    for child in children:
        childPrompt = prompt(**child)
        defaultValue = ShownValue(childPrompt.placeHolder)
        childrenPlaceHolders.append(defaultValue)

        initValue = defaultValue.getValue(childPrompt.content)

        childrenContents.append(initValue)

    while True:
        indexInRange = index % childrenAvailable
        child = children[indexInRange]
        childContent = childrenContents[indexInRange]
        childPlaceHolder = childrenPlaceHolders[indexInRange]
        childPrompt = prompt(**child)
        title = childPrompt.title
        myTerm.setConsoleLine(0, title)

        formatWord = currentPrompt.template.format(*childrenContents)
        myTerm.setConsoleLine(1, formatWord)
        myTerm.refresh()
        char = getch.getch()

        if char == "\n":
            index = index + 1
            childrenContents[indexInRange] = childContent
            if indexInRange == childrenAvailable - 1:
                break
            continue
        # elif not char.isalpha():
        #     break

        childrenContents[indexInRange] = childPlaceHolder.getValue(
            childContent + char)

    myTerm.finish()
    return word if word != "" else currentPrompt.template.format(*childrenContents)


wea = multiTextInput({
    "variety": "multitext",
    "title": "que ondis?",
    "placeHolder": "weon",
    "children": [{"variety": "type", "placeHolder": "feat", "title": "escribi el tipo:"}, {"variety": "type", "placeHolder": "scope", "title": "tira el scope:"}, {"variety": "type", "title": "escribi la descri:"}],
    "template": "{0}({1}):{2}"
})
exit()


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
