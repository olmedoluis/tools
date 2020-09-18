from os import name as _osName

if _osName == "nt":
    import ctypes

    class _CursorInfo(ctypes.Structure):
        _fields_ = [("size", ctypes.c_int), ("visible", ctypes.c_byte)]


class ConsoleControl:
    def __init__(self, lines="default"):
        from os import popen
        from sys import stdout

        self.stdout = stdout

        terminalHeight, terminalWidth = popen("stty size", "r").read().split()
        self.terminalWidth = int(terminalWidth) - 1
        self.terminalHeight = int(terminalHeight) - 1

        lines = self.terminalHeight if lines == "default" else lines

        self.display = (" " * (lines - 1)).split(" ")

        self.hide_cursor()

        for emptyValue in self.display:
            print(emptyValue)

    def hide_cursor(self):
        if _osName == "nt":
            ci = _CursorInfo()
            handle = ctypes.windll.kernel32.GetStdHandle(-11)
            ctypes.windll.kernel32.GetConsoleCursorInfo(handle, ctypes.byref(ci))
            ci.visible = False
            ctypes.windll.kernel32.SetConsoleCursorInfo(handle, ctypes.byref(ci))
        elif _osName == "posix":
            self.stdout.write("\033[?25l")
            self.stdout.flush()

    def show_cursor(self):
        if _osName == "nt":
            ci = _CursorInfo()
            handle = ctypes.windll.kernel32.GetStdHandle(-11)
            ctypes.windll.kernel32.GetConsoleCursorInfo(handle, ctypes.byref(ci))
            ci.visible = True
            ctypes.windll.kernel32.SetConsoleCursorInfo(handle, ctypes.byref(ci))
        elif _osName == "posix":
            self.stdout.write("\033[?25h")
            self.stdout.flush()

    def _cursorUp(self, times):
        self.stdout.write(f"\x1b[{times}A")

    def _cleanLine(self):
        self.stdout.write(f"\x1b[2K")

    def setConsoleLine(self, row=0, column=0, content=""):
        self.display[row] = " " * column + content

    def refresh(self):
        count = len(self.display)
        self._cursorUp(count)
        for line in self.display:
            self._cleanLine()
            print(line)

    def deleteLastLines(self, lines):
        lastNumberOfLines = len(self.display)
        newNumberOfLines = lastNumberOfLines - lines
        self.display = (" " * (newNumberOfLines)).split(" ")
        for i in range(0, lines):
            self._cleanLine()
            self._cursorUp(1)

    def finish(self):
        self.show_cursor()


def getGetch():
    from os import name

    if name == "nt":
        import msvcrt

        return msvcrt.getch

    def getch():
        import sys
        import tty
        import termios

        try:
            fd = sys.stdin.fileno()
            old = termios.tcgetattr(fd)
        except:
            return chr(27)
        try:
            tty.setraw(fd)
            return sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)

    return getch

