import time
import sys
from pynput.keyboard import Key, Listener
from pynput import keyboard


def selection():
    pass


question = "que onda perro?"
texto = ""
template = "{}({}){}"
last_frame = ""
frame = ""
outputs = []


def on_press(key):
    global texto

    keyString = '{0}'.format(key)

    if key == keyboard.Key.esc:
        return False

    if key == keyboard.Key.space:
        texto += " "
        update_screen(texto)

    if key == keyboard.Key.backspace:
        texto += "\b"
        update_screen(texto)

    if len(keyString) != 3:
        return

    texto += keyString[1]
    update_screen(texto)


def update_screen(textToShow):
    global template, last_frame, frame, texto

    clean_up = '\b' * (len(last_frame) + 2)
    last_frame = textToShow

    sys.stdout.write(clean_up)
    sys.stdout.write(textToShow)
    sys.stdout.flush()
    outputs.append(textToShow)


with Listener(on_press=on_press) as listener:
    try:
        listener.join()
    except KeyboardInterrupt:
        print("\ntexto", texto)
        # print("outputs", outputs)
        print("frame", frame)
        print("buffer", sys.stdout.buffer)
exit()
