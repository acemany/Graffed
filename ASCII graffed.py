from pygame import (MOUSEBUTTONDOWN, MOUSEBUTTONUP, QUIT, TEXTINPUT,
                    display, event, font, image, mouse, time,
                    init, quit,
                    Vector2)
from sys import path as game_path
from typing import Tuple


class Camera:
    def __init__(self, pos: Tuple[int, int] = (0, 0)):
        self.position = -Vector2(pos)

    @property
    def pos(self) -> Tuple[int, int]:
        return self.position.x.__int__(), self.position.y.__int__()

    @pos.setter
    def pos(self, pos: Tuple[int, int]):
        self.position.update(pos)

    def update(self, to: Tuple[int, int]):
        self.position += to


class Font:
    def __init__(self, scale: int = 16, name: str = f"{game_path[0]}/console.ttf"):  # MS serif
        self.font = font.Font(name, scale)
        self.w, self.h = self.font.size("n")

    def render(self, pos: Tuple[int, int], text: str, color: str, antialians: int, centering: int = 0):
        WIN.blits([(self.font.render(text, antialians, color, (32, 32, 32)), (
                   pos[0]-(self.font.size(text)[0]/2 if centering else 0), pos[1]+y*self.h))
                   for y, text in enumerate(text.replace("\b", " | ").split("\n"))])


if __name__ == "__main__":
    SC_RES = (600, 450)
    init()
    gamedir = f"{game_path[0]}"
    WIN = (display.set_mode(SC_RES))
    display.set_icon(image.load(f"{gamedir}\\assets\\icon.bmp").convert())

    MAINFONT = Font()
    font_antialias = 1
    last_mouse_pos = (0, 0)
    # PIC_SCALE = (SC_RES[0]//MAINFONT.w+1, SC_RES[1]//MAINFONT.h+1)
    # ASCII_pic = [["# " for x in range(PIC_SCALE[0])]for y in range(PIC_SCALE[1])]
    gradient = " .-' = +*0# @"
    with open(f"{gamedir}/database.acemany", "r") as file:
        ASCII_pic = [[chr for chr in chrs]for chrs in file.read().split("\n")]
    PIC_SCALE = (ASCII_pic[0].__len__(), ASCII_pic.__len__())
    paint_char = "w"
    paint = 0

    CLOCK = time.Clock()
    CAMERA = Camera()

    while True:
        WIN.fill("#000000")

        mouse_keys_down = event.get(MOUSEBUTTONDOWN)
        mouse_keys = mouse.get_pressed()
        mouse_keys_up = event.get(MOUSEBUTTONUP)
        mouse_x, mouse_y = mouse_pos = mouse.get_pos()
        for i in event.get(TEXTINPUT):
            paint_char = i.text

        for e in event.get():
            if e.type == QUIT:
                quit()

        for i in mouse_keys_down:
            if i.button == 1:
                paint = 1
        if paint:
            charx = int(mouse_x-CAMERA.position.x)//MAINFONT.w
            chary = int(mouse_y-CAMERA.position.y)//MAINFONT.h
            if -1 < charx < PIC_SCALE[0] and -1 < chary < PIC_SCALE[1]:
                ASCII_pic[chary][charx] = paint_char
        if mouse_keys[1]:
            CAMERA.update(((mouse_x-last_mouse_pos[0]),
                           (mouse_y-last_mouse_pos[1])))
        for i in mouse_keys_up:
            if i.button == 1:
                paint = 0
        last_mouse_pos = mouse_pos[:]

        [MAINFONT.render(CAMERA.position+(0, y*MAINFONT.h), chars.__str__()[2: -1: 5], "#FFFFFF",
         font_antialias, 0)for y, chars in enumerate(ASCII_pic)]

        MAINFONT.render((SC_RES[0]/2, 0), "\b".join(map(str, (int(CLOCK.get_fps()), mouse_pos, CAMERA.pos, paint_char))), "#707070", font_antialias, 1)
        display.flip()
        CLOCK.tick(60)
