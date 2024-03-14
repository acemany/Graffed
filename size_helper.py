from pygame import (display, event, font, image, key, mouse, time, transform, draw,
                    KEYDOWN, MOUSEBUTTONDOWN, MOUSEBUTTONUP, MOUSEWHEEL, QUIT,
                    K_ESCAPE, K_SPACE,
                    init, quit as squit,
                    Surface)
# from triangled import draw_polygon
from potaget import c_p_r
from typing import Tuple
from sys import exit


class Font:
    def __init__(self, pos: Tuple[int, int], color: str = "#BBBBBB", scale: int = 6, name: str = "Arial"):
        self.font = font.SysFont(name, scale)
        self.w = self.font.size("n")[0]
        self.h = self.font.get_height()
        self.indicator_pos = 0
        self.x, self.y = pos
        self.color = color
        self.text = ""

    def text_input(self, key_in: Tuple, text_in: Tuple, lining: bool = True):
        for i in text_in:
            char = i.__dict__["text"]
            if char != "":
                self.text += char
        for i in key_in:
            key = i.__dict__["unicode"]
            if key == "\x08":
                self.text = self.text[: -1]
            elif key == "\r":
                if lining:
                    self.text += "\n"
                else:
                    return True
        return False

    def draw(self, win: Surface, pos: Tuple[int, int], text: str, antialians: int, centering: int = 0):
        if centering:
            win.blits([(self.font.render(text, antialians, self.color),
                       (pos[0]-self.font.size(text)[0]/2, pos[1]+y*self.h))
                       for y, text in enumerate(text.replace("\b", " | ").split("\n"))])
        else:
            win.blits([(self.font.render(text, antialians, self.color),
                       (pos[0], pos[1]+y*self.h))
                       for y, text in enumerate(text.replace("\b", " | ").split("\n"))])

    def blit(self, win: Surface, antialians: int):
        win.blits([(self.font.render(text, antialians, self.color),
                   (self.x, self.y+y*self.h))
                   for y, text in enumerate(self.text.split("\n"))])


if __name__ == "__main__":
    init()
    SC_RES = WIDTH, HEIGHT = (800, 600)
    WIN = (display.set_mode(SC_RES))
    display.set_icon(image.load("icon.jpg").convert())

    # VARIABLES
    # rect_icon = image.load("assets\\instruments\\rect.png")
    # rect_icon.set_colorkey("#FF00FF")
    # rect_icon.fill((0, 0, 0))
    # TISize = rect_icon.get_size()[0]
    block_move = [False, 0]
    TISize = 24
    copper_wall_icon = transform.scale(image.load(
        "icon.jpg"), (TISize, TISize))
    grass_wall_icon = transform.scale(image.load(
        "icon.jpg"), (TISize, TISize))
    stone_wall_icon = transform.scale(image.load(
        "icon.jpg"), (TISize, TISize))
    sand_wall_icon = transform.scale(image.load(
        "icon.jpg"), (TISize, TISize))
    char_wall_icon = transform.scale(image.load(
        "icon.jpg"), (TISize, TISize))
    copper_wall_icon.set_colorkey("#FF00FF")
    grass_wall_icon .set_colorkey("#FF00FF")
    stone_wall_icon .set_colorkey("#FF00FF")
    sand_wall_icon  .set_colorkey("#FF00FF")
    char_wall_icon  .set_colorkey("#FF00FF")
    blocks = ([copper_wall_icon, ([6, 6])],
              [grass_wall_icon, ([6+TISize, 6])],
              [stone_wall_icon, ([6+TISize*2, 6])],
              [sand_wall_icon, ([6+TISize*3, 6])],
              [char_wall_icon, ([6, 6+TISize])])

    offset = (0, 0)
    font_antialias = True
    offsetting = True
    floor_ratio = 1

    CLOCK = time.Clock()
    MAINFONT = Font((0, 0), "#9A9A9A", 16)

    while True:
        WIN.fill("#454545")

        key_down = not not event.get(KEYDOWN)
        keys = key.get_pressed()

        mouse_keys = mouse.get_pressed()
        mouse_key_down = not not event.get(MOUSEBUTTONDOWN)
        mouse_key_up = not not event.get(MOUSEBUTTONUP)
        mouse_pos = mouse.get_pos()

        for i in event.get(MOUSEWHEEL, 0):
            floor_ratio = int(floor_ratio+(i.y if (floor_ratio+i.y)//1 > 1 else 0))
        if keys[K_ESCAPE] or event.get(QUIT):
            [print(block[1])for block in blocks]
            squit()
            exit()
        for i, block in enumerate(blocks):
            if c_p_r(*mouse_pos, block[1][0]-1, block[1][1]-1, *block[0].get_size()):
                if mouse_key_down and mouse_keys[0]:
                    block_move = [True, i]
                    if offsetting:
                        offset = (blocks[i][1][0]-mouse_pos[0],
                                  blocks[i][1][1]-mouse_pos[1])
                MAINFONT.draw(WIN, mouse_pos,
                              f"\n  {blocks[i][1][0]}, {blocks[i][1][1]}", font_antialias, 0)
                break
        if mouse_key_up:
            block_move = [False, 0]
        elif key_down:
            if keys[K_SPACE]:
                offsetting = not offsetting
        elif block_move[0]:
            if offsetting:
                blocks[block_move[1]][1] = [mouse_pos[0]//floor_ratio*floor_ratio+offset[0],
                                            mouse_pos[1]//floor_ratio*floor_ratio+offset[1]]
            else:
                blocks[block_move[1]][1] = [mouse_pos[0]//floor_ratio*floor_ratio,
                                            mouse_pos[1]//floor_ratio*floor_ratio]

        WIN.blits(blocks)
        draw.polygon(WIN, (255, 255, 255), [(int(block[1][0]+block[0].get_size()[0]/2), int(block[1][1]+block[0].get_size()[1]/2))for block in blocks])
        MAINFONT.draw(WIN, (SC_RES[0]/2, 0), "\b".join(map(str, (int(CLOCK.get_fps()), mouse_pos[0], block_move, TISize, floor_ratio))), font_antialias, 1)
        CLOCK.tick(60)
        display.flip()
