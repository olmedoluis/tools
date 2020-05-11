import curses
from time import sleep

word = ""
last_word = ""


def prompts(data):
    if not "placeholder" in data:
        data["placeholder"] = ""

    if not "title" in data:
        data["title"] = ""

    def setup():
        title = data["title"]

        stdscr.addstr(1, 0, f" {title}")

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
            elif char == "KEY_BACKSPACE":
                word = word[:-1]
            else:
                word += char

    def multitext():
        print("multiselect")
        sleep(5)

    prompts_store = {
        "text": text,
        "multitext": multitext
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
