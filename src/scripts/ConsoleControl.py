def console(height):
    import sys

    code = "\x1b["
    log = sys.stdout.write

    def cursorUp(times):
        log(f"{code}{times}A")

    def cleanLine():
        log(f"{code}2K")

    class term():
        def __init__(self, lines):
            self.display = (" " * (lines + 1)).split(" ")
            self.test = []
            print()
            print()

        def getCode(self, string):
            return f"\x1b[{string}"

        def show(self, data):
            self.display = data

        def refresh(self):
            count = len(self.display)
            cursorUp(count)
            # log(self.getCode(f"{count}B"))
            for line in self.display:
                cleanLine()
                print(line)

        def show1(self, row, string):
            # self.display[row] = string
            proof = [*self.display]
            proof[row] = string
            self.display = proof

        def finish(self):
            print()

    return term(height)
