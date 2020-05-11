import curses

word = ""
last_word = ""

outputs = []


def prompts(data):
    word = ""
    last_word = ""
    if not "placeholder" in data:
        data["placeholder"] = ""

    if not "title" in data:
        data["title"] = ""

    def setup():
        title = data["title"]

        stdscr.addstr(0, 0, "")
        stdscr.addstr(1, 0, f" {title}")
        stdscr.addstr(4, 0, "")

    def text():
        global word, last_word

        def getDisplayString(word):
            placeholder = data["placeholder"]

            if word == "":
                return placeholder

            return word

        while True:
            stdscr.clear()
            setup()

            user_input = getDisplayString(word)
            stdscr.addstr(3, 0, f"\t{user_input}")
            stdscr.refresh()

            last_word += word

            try:
                char = stdscr.getkey()
            except:
                break

            if "\n" in char:
                break
            elif char == "\x7f":
                word = word[:-1]
            else:
                word += char

            outputs.append(char)

    prompts_store = {
        "text": text
    }

    actual_prompt = prompts_store[data["type"]]

    stdscr = curses.initscr()
    curses.cbreak()
    stdscr.keypad(True)

    try:
        actual_prompt()
    finally:
        curses.nocbreak()
        stdscr.keypad(False)
        curses.echo()
        curses.endwin()


prompts({
    "type": "text",
    "placeholder": "weon",
    "title": "que onda weon?"
})

exit()
