def console(height):
    import sys
    import os

    if os.name == 'nt':
        import msvcrt
        import ctypes

        class _CursorInfo(ctypes.Structure):
            _fields_ = [("size", ctypes.c_int), ("visible", ctypes.c_byte)]

    def hide_cursor():
        if os.name == 'nt':
            ci = _CursorInfo()
            handle = ctypes.windll.kernel32.GetStdHandle(-11)
            ctypes.windll.kernel32.GetConsoleCursorInfo(
                handle, ctypes.byref(ci))
            ci.visible = False
            ctypes.windll.kernel32.SetConsoleCursorInfo(
                handle, ctypes.byref(ci))
        elif os.name == 'posix':
            sys.stdout.write("\033[?25l")
            sys.stdout.flush()

    def show_cursor():
        if os.name == 'nt':
            ci = _CursorInfo()
            handle = ctypes.windll.kernel32.GetStdHandle(-11)
            ctypes.windll.kernel32.GetConsoleCursorInfo(
                handle, ctypes.byref(ci))
            ci.visible = True
            ctypes.windll.kernel32.SetConsoleCursorInfo(
                handle, ctypes.byref(ci))
        elif os.name == 'posix':
            sys.stdout.write("\033[?25h")
            sys.stdout.flush()

    code = "\x1b["
    log = sys.stdout.write

    def cursorUp(times):
        log(f"{code}{times}A")

    def cursorDown(times):
        log(f"{code}{times}B")

    def cleanLine():
        log(f"{code}2K")

    class term():
        def __init__(self, lines):
            self.display = (" " * (lines - 1)).split(" ")

            for emptyValue in self.display:
                print(emptyValue)

        def getCode(self, string):
            return f"\x1b[{string}"

        def show(self, data):
            self.display = data

        def setConsoleLine(self, row=0, column=0, content=""):
            self.display[row] = " " * column + content

        def refresh(self):
            count = len(self.display)
            cursorUp(count)
            for line in self.display:
                cleanLine()
                print(line.replace("$C", "❚"))

        def deleteLastLines(self, lines):
            lastNumberOfLines = len(self.display)
            newNumberOfLines = lastNumberOfLines - lines
            self.display = (" " * (newNumberOfLines)).split(" ")
            cursorUp(lines)

        def finish(self):
            show_cursor()

    hide_cursor()
    return term(height)
