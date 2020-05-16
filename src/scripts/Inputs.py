from time import sleep
import os
import sys
import time
import getch
from ConsoleControl import console


def terminal(height):
    my_terminal = console(height)

    class terminal_ui():
        def showAt(self, data):
            my_terminal.show(data)

        def refresh(self):
            my_terminal.refresh()

    return terminal_ui()


# prompts({
#     "type": "multitext",
#     "title": "que ondis?",
#     "placeholder": "weon",
#     "children": [{"name": "type", "placeholder": "feat", "title": "escribi el tipo:"}, {"name": "type", "placeholder": "feat", "title": "escribi el scope:"}, {"name": "about"}],
#     "template": "{}({}):{}"
# })

myTerm = terminal(2)
myTerm.showAt(["hola", "holi"])

myTerm.refresh()
time.sleep(1)

myTerm.showAt(["noice", "aaa"])
# myTerm.showAt(1, "holis")
myTerm.refresh()
time.sleep(1)

# myTerm.finish()

exit()
