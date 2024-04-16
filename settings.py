from pygame import (MULTIGESTURE, MOUSEBUTTONDOWN, KEYDOWN, MOUSEBUTTONUP, FINGERMOTION, FINGERUP, QUIT, MOUSEWHEEL,
                    display, key, draw, event, font, mouse, time, image, transform,
                    Vector2, Rect, Surface,
                    init, quit as squit,
                    K_ESCAPE, K_RETURN)
from pgti import TextInputVisualizer, TextInputManager
from json import loads, load, dump
from requests import get as r_get
from threading import Thread
from random import shuffle
from shutil import rmtree
from pathlib import Path
from typing import Tuple
from typing import Dict
import os


class Switch:
    def __init__(self, truth: bool = False, swithable: bool = True, name: str = "boolean"):
        self.switchable = swithable
        self.truth = truth
        self.name = name

    @property
    def switch(self):
        self.truth = not self.truth
        return self.truth

    def draw(self, pos: Tuple[int, int]):
        if self.truth:
            if self.switchable:
                if c_p_r(*MPos, *pos, *sw_size):
                    win.blit(sw_on_over, pos)
                else:
                    win.blit(sw_on, pos)
            else:
                win.blit(sw_on_disabled, pos)
        else:
            if self.switchable:
                if c_p_r(*MPos, *pos, *sw_size):
                    win.blit(sw_off_over, pos)
                else:
                    win.blit(sw_off, pos)
            else:
                win.blit(sw_off_disabled, pos)
        MAINFONT.drat(self.name, font_antialias, (pos[0]+sw_size[0]+4, pos[1]+(sw_size[1]-MAINFONT.h)/2), win)


class Slider:
    def __init__(self, num: int = 0, name: str = "variable"):
        self.name = name
        self.on = False
        self.num = num


class Slider:
    #slid_pw = 20
    #slid_h = 24
    #slid_SC = 4
    def __init__(self, name: str, number: int) -> None:
        self.width = WIDTH/2
        self.w = WIDTH/40
        self.height = font_size
        self.name = name
        self.on = False
        self.n = number

    def draw(self):
        out = Surface((WIDTH/2+self.w, self.height))
        out.set_colorkey((0, 0, 0))
        draw.rect(out, (69, 69, 69), (0, 0, self.width+self.w, self.height), 2)
        draw.rect(out, (255, 255, 255) if self.on else (69, 69, 69), (self.n*WIDTH/200, 0, self.w, self.height))

        print(((WIDTH/2-FONT.size(f"{self.n}")[0]-2, (self.height-FONT.get_height())/2),
               (2+self.w, (self.height-FONT.get_height())/2)))
        out.blits((FONT.render(f"{self.n}", 1, (127, 127, 127)),
        (WIDTH/2-FONT.size(f"{self.n}")[0]-2, (self.height-FONT.get_height())/2)),
                  (FONT.render(self.name, 1, (127, 127, 127)),
                  (2+self.w, (self.height-FONT.get_height())/2)))
        return out


gamedir = Path(__file__).parent
with open(gamedir/"config.json", "r") as f:
    global options_raw
    options_raw = load(f)
    font_size = options_raw["font_size"]

init()
WIN = display.set_mode()
WIDTH, HEIGHT = SC_RES = Vector2(WIN.get_size())
FONT = font.SysFont('Arial', font_size, bold=True)
CLOCK = time.Clock()

Cbuttonua = (63, 63, 63)  # (43, 52, 59)
Cbuttona = (4, 104, 170)
Cbg = (18, 18, 18)
Ctxt = (207, 212, 218)
Ctxt2 = (164, 161, 171)

current_page = 0
delta = 1/60
tagsoffs = load_progress = page_sliding_offset = ysly = yslys = ttr = 0
tagsearch = tagsearchaa = untag = page_sliding = False
PLysize = pitems = pdy = 1
settings_items = []
mouse_pos = Vector2()

tags_textarea = TextInputVisualizer(manager=TextInputManager(validator=lambda i: tagsearch and len(i) < 64),
                                   font_object=FONT, font_color=Ctxt)

Rless_pics = Rect(0,         0,  50, 50)
Rmore_pics = Rect(50,        0,  50, 50)
Rprev_page = Rect(WIDTH-110, 0,  50, 50)
Rnext_page = Rect(WIDTH-60,  0,  50, 50)
Rreload = Rect(WIDTH/2-100,  0, 100, 50)
Rclear = Rect(WIDTH/2,       0, 100, 50)

for i in options_raw.items():
    print(f"{i[0]} = {i[1]}")
    if type(i[1]) == int:
        settings_items.append((Slider(i[0], i[1])))

while True:
    ysly = min(max(ysly+yslys, -PLysize+HEIGHT), 0)
    yslys = yslys*0.95
    yslys = min(max(yslys, -100), 100)
    WIN.fill(Cbg)

    mouse_pos.update(mouse.get_pos())
    mouse_pressed = mouse.get_pressed()
    keys_pressed = key.get_pressed()
    events = event.get()

    tags_textarea.update(events)

    for i in settings_items:
        if mouse_pressed[0] and i.hovered:
            i.n = min(max((mouse_position.x-WIDTH/4-slid_pw/2)/WIDTH/200, 0), 100)
        i.draw()

    for e in events:
        if e.type == QUIT or keys_pressed[K_ESCAPE]:
            squit()
            quit()
        elif e.type == KEYDOWN:
            if e.key == K_ESCAPE:
                squit()
                quit()
        elif e.type == MOUSEBUTTONDOWN and e.button == 1:
            mouse_down = True
            if PLysize > HEIGHT and Rect((WIDTH-10, -HEIGHT*ysly/PLysize, 10, HEIGHT/PLysize*HEIGHT)).collidepoint(mouse_pos):
                page_sliding = True
                page_sliding_offset = -mouse_pos.y-HEIGHT*ysly/PLysize
        elif e.type == MOUSEBUTTONUP:
            page_sliding = False
        elif e.type == FINGERMOTION and not page_sliding:
            yslys += e.dy*HEIGHT/delta
        elif e.type == FINGERUP:
            mouse.set_pos(0,0)
        elif e.type == MOUSEWHEEL:
            yslys += e.y*HEIGHT*delta
    if mouse_pressed[0]:
        if page_sliding:
            yslys = (((-page_sliding_offset-mouse_pos.y)*PLysize/HEIGHT-ysly)*delta+yslys)*4

    WIN.blits([(FONT.render(f"{i}", 1, Ctxt2), (25, HEIGHT/2+25*j),) for j, i in enumerate((1/delta, ysly, yslys, PLysize+ysly-HEIGHT))])
    display.flip()
    delta = CLOCK.tick(60)/1000
    if not delta:
        delta = 1/60
