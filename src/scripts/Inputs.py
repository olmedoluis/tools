import curses
from time import sleep

word = ""
last_word = ""


def prompts(data):
    if not "placeholder" in data:
        data["placeholder"] = ""

    if not "title" in data:
        data["title"] = ""

    def text_validator(word, char):
        if "\n" in char:
            return False
        elif char == "KEY_BACKSPACE":
            return word[:-1]
        else:
            word += char
            return word

    def text(validator, prefix="", root=3, postfix="", placeholder="", title=""):
        global word, last_word
        word = ""
        last_word = ""

        def getDisplayString(word):
            if word == "":
                return placeholder

            return word

        while True:
            stdscr.clear()

            stdscr.addstr(1, 1, f"{title}")

            user_input = getDisplayString(word)

            formated_user_input = f"{prefix}{user_input}{postfix}"
            stdscr.addstr(4, root, formated_user_input)
            stdscr.addstr(4, root, f"{prefix}{user_input}")

            stdscr.refresh()

            last_word += word

            try:
                char = stdscr.getkey()
            except:
                break

            validation = validator(word, char)

            if validation == False:
                break

            word = validation

        return word if word != "" else placeholder

    def multitext(validator):
        template = data["template"]

        names = []
        children = data["children"]

        for child in children:
            names.append(child["name"])
            if not "placeholder" in child:
                child["placeholder"] = child["name"]

            if not "title" in child:
                child["title"] = ""

        for index in range(0, len(names)):
            child = children[index]
            prefix, postfix = template.replace("{}", "$", 1).split("$", 1)
            postfix = postfix.format(*names[index + 1:])

            value = text(text_validator, prefix=prefix,
                         postfix=postfix, placeholder=child["placeholder"], title=child["title"])

            template = template.replace("{}", value, 1)

        return template

    prompts_store = {
        "text": {"prompt": text, "validator": text_validator},
        "multitext": {"prompt": multitext, "validator": text_validator}
    }

    selectedPrompt = prompts_store[data["type"]]

    stdscr = curses.initscr()
    curses.cbreak()
    stdscr.keypad(True)
    result = ""
    try:
        actual_prompt = selectedPrompt["prompt"]
        validator = selectedPrompt["validator"]
        result = actual_prompt(validator)
    finally:
        curses.nocbreak()
        stdscr.keypad(False)
        curses.echo()
        curses.endwin()
        print(result)


prompts({
    "type": "multitext",
    "title": "que ondis?",
    "placeholder": "weon",
    "children": [{"name": "type", "placeholder": "feat", "title": "escribi el tipo:"}, {"name": "type", "placeholder": "feat", "title": "escribi el scope:"}, {"name": "about"}],
    "template": "{}({}):{}"
})

exit()
