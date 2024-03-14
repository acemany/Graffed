from pygame import (display, key, event, font, mouse, time,
                    MULTIGESTURE, KEYDOWN, QUIT,
                    init, quit as squit,
                    K_ESCAPE,
                    Vector2)
from pgti import TextInputVisualizer, TextInputManager
from pathlib import Path
from sys import exit
# from potaget import log

init()
WIN = display.set_mode()
WIDTH, HEIGHT = SC_RES = Vector2(WIN.get_size())
FONT = font.SysFont('Arial', 16, bold=True)
CLOCK = time.Clock()
key.set_repeat(200, 25)
gamedir = Path(__file__).parent

excepp = ""
CodeObrabotanny = ""
exec("from pygame import *; from math import *")

Cbuttonua = (63, 63, 63)  # (43, 52, 59)
Cbuttona = (4, 104, 170)  #
Cbg = (18, 18, 18)  #
Ctxt = (207, 212, 218)  #
Ctxt2 = (164, 161, 171)  #

delta = 100/6
mouse_pos = Vector2()

with open(gamedir/"code.py", "r") as f:
    tag_textarea = TextInputVisualizer(manager=TextInputManager(f.read(), validator=lambda i: True),
                                       font_object=FONT, font_color=Ctxt)


def queuit():
    with open(gamedir/"code.py", "w") as f:
        f.write(tag_textarea.value)
    squit()
    exit()


CodeObrabotanny = tag_textarea.value.replace("\x0E", "\n")

while 1:
    WIN.fill(Cbg)

    mouse_pos.update(mouse.get_pos())
    mouse_pressed = mouse.get_pressed()
    keys_pressed = key.get_pressed()
    events = event.get()

    for e in events:
        if e.type == QUIT or e.type == MULTIGESTURE:
            queuit()
        elif e.type == KEYDOWN:
            if e.key == K_ESCAPE:
                queuit()

    tag_textarea.update(events)
    CodeObrabotanny = tag_textarea.value.replace("\x0E", "\n")

    try:
        exec(CodeObrabotanny)
        excepp = ""
    except Exception as e:
        excepp = str(e)

    CodeObrabotanny = f"{CodeObrabotanny[:tag_textarea._manager.cursor_pos]}|{CodeObrabotanny[tag_textarea._manager.cursor_pos:]}"

    WIN.blits([(FONT.render(f"{i}", 1, Ctxt2), (25, 25+25*j),)
               for j, i in enumerate([1000/delta, *CodeObrabotanny.split("\n"), excepp])])
    display.flip()
    delta = CLOCK.tick(60)
    if not delta:
        delta = 100/6
