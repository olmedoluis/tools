from sys import stdout
from os import name as osName

if osName == "nt":
    import ctypes

    class _CursorInfo(ctypes.Structure):
        _fields_ = [("size", ctypes.c_int), ("visible", ctypes.c_byte)]


def hide_cursor():
    if osName == "nt":
        ci = _CursorInfo()
        handle = ctypes.windll.kernel32.GetStdHandle(-11)
        ctypes.windll.kernel32.GetConsoleCursorInfo(handle, ctypes.byref(ci))
        ci.visible = False
        ctypes.windll.kernel32.SetConsoleCursorInfo(handle, ctypes.byref(ci))
    elif osName == "posix":
        stdout.write("\033[?25l")
        stdout.flush()


def show_cursor():
    if osName == "nt":
        ci = _CursorInfo()
        handle = ctypes.windll.kernel32.GetStdHandle(-11)
        ctypes.windll.kernel32.GetConsoleCursorInfo(handle, ctypes.byref(ci))
        ci.visible = True
        ctypes.windll.kernel32.SetConsoleCursorInfo(handle, ctypes.byref(ci))
    elif osName == "posix":
        stdout.write("\033[?25h")
        stdout.flush()


code = "\x1b["


def _cursorUp(times):
    stdout.write(f"{code}{times}A")


def _cleanLine():
    stdout.write(f"{code}2K")


class ConsoleControl:
    def __init__(self, lines):
        self.display = (" " * (lines - 1)).split(" ")

        hide_cursor()

        for emptyValue in self.display:
            print(emptyValue)

    def setConsoleLine(self, row=0, column=0, content=""):
        self.display[row] = " " * column + content

    def refresh(self):
        count = len(self.display)
        _cursorUp(count)
        for line in self.display:
            _cleanLine()
            print(line.replace("$C", "❚"))

    def deleteLastLines(self, lines):
        lastNumberOfLines = len(self.display)
        newNumberOfLines = lastNumberOfLines - lines
        self.display = (" " * (newNumberOfLines)).split(" ")
        for i in range(0, lines):
            _cleanLine()
            _cursorUp(1)

    def finish(self):
        show_cursor()

