from pygame import (display, event, font, image, key, time, transform,
                    Surface, Vector3,
                    K_ESCAPE, K_s,
                    init, quit,
                    QUIT)
from sys import argv, exit
from typing import Tuple


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

    def draw(self, win: Surface, pos: tuple[int, int], text: str, antialias: bool, centering: int = 0):
        if centering:
            win.blits([(self.font.render(text, antialians, self.color),
                       (pos[0]-self.font.size(text)[0]/2, pos[1]+y*self.h))
                       for y, text in enumerate(text.replace("\b", " | ").split("\n"))])
        else:
            win.blits([(self.font.render(text, antialias, self.color),
                       (pos[0], pos[1]+y*self.h))
                       for y, text in enumerate(text.replace("\b", " | ").split("\n"))])

    def blit(self, win: Surface, antialians: int):
        win.blits([(self.font.render(text, antialians, self.color),
                   (self.x, self.y+y*self.h))
                   for y, text in enumerate(self.text.split("\n"))])


def pic_to_pal(color: Tuple[int, int, int] = (255, 0, 0)):
    to = Vector3(color[0], color[1], color[2])
    res = (to[0]//64*64,
           to[1]//64*64,
           to[2]//64*64)
    # a = 444
    # or i in RGBcolor:
    #    d = i.distance_to(to)
    #    if d<a:
    #        res = i
    #        a = d
    return res


def rgb_to_hex(color: Tuple[int, int, int] = (255, 0, 0)):
    hr = f"{int(color[0]): 0x}"
    hg = f"{int(color[1]): 0x}"
    hb = f"{int(color[2]): 0x}"
    return f"""#{str(hr if color[0] > 9 else hr+"0")
                 }{str(hg if color[1] > 9 else hg+"0")
                   }{str(hb if color[2] > 9 else hb+"0")}"""


def hex_to_rgb(color: str = "#ff0000"):
    color = color.replace("#", "", 1)
    return (int(color[0]+color[1], base=16),
            int(color[2]+color[3], base=16),
            int(color[4]+color[5], base=16))


if __name__ == "__main__":
    init()
    SC_RES = [800, 600]
    imagg = image.load("icon.png"if len(argv) == 1 else argv[1])
    if imagg.get_size()[0] < SC_RES[0]:
        SC_RES[0] = imagg.get_size()[0]
    if imagg.get_size()[1] < SC_RES[1]:
        SC_RES[1] = imagg.get_size()[1]
    WIN = (display.set_mode(SC_RES))
    display.set_icon(image.load("assets\\icon.bmp").convert())

    RGBcolor = (Vector3(32,  8,   32),  Vector3(255, 200, 150), Vector3(32,  32,  96),
                Vector3(64,  128, 200), Vector3(255, 160, 140), Vector3(255, 128, 64),
                Vector3(255, 48,  48),  Vector3(255, 144, 144), Vector3(160, 96,  128),
                Vector3(255, 96,  128),
                Vector3(136, 136, 160), Vector3(221, 224, 241), Vector3(254, 255, 255),
                Vector3(0,   194, 255), Vector3(0,   140, 255), Vector3(0,   150, 214),
                Vector3(171, 255, 104), Vector3(63,  187, 74),  Vector3(0,   134, 74),
                Vector3(255, 255, 117), Vector3(255, 206, 0),   Vector3(233, 163, 0),
                Vector3(255, 163, 125), Vector3(255, 108, 80),  Vector3(201, 78,  62),
                Vector3(255, 150, 150), Vector3(255, 72,  101), Vector3(192, 88,  139),
                Vector3(255, 179, 228), Vector3(255, 144, 202), Vector3(230, 108, 167),
                Vector3(171, 134, 255), Vector3(137, 107, 214), Vector3(102, 80,  160),
                Vector3(255, 227, 227), Vector3(255, 202, 184), Vector3(246, 171, 160),
                Vector3(219, 145, 145), Vector3(187, 103, 122), Vector3(144, 79,  90))
    # PixelObjevt = ("#EEA5A3", "#CB7689", "#9D5A64", #BROWN
    #                "#FFF0F0", "#FFE8D0", "#FFC3B5", #BEIGE
    #                "#C198FF", "#997EAB", "#725BAD", #VIOLET
    #                "#FFCCFC", "#FF9CDB", "#FF7CBA", #PINK
    #                "#FFAAAA", "#FF5273", "#CE3B56", #RED
    #                "#FFBA8F", "#FF7C5B", "#D75947", #ORANGE
    #                "#FFFF86", "#FFEB00", "#F6BA00", #YELLOW
    #                "#C3FF77", "#48D155", "#009352", #GREEN
    #                "#00CEFF", "#009BFF", "#0076ED", #BLUE
    #                "#9C9FAD", "#CED1D9", "#FFFFFF", #WHITE
    #                "#1F1F29", "#444454", "#6D6F7F")#BLACK
    image_size = imagg.get_size()
    font_antialias = 1
    CLOCK = time.Clock()
    MAINFONT = Font((0, 0), "#9A9A9A", 16)

    for y in range(image_size[1]):
        for x in range(image_size[0]):
            imagg.set_at((x, y), pic_to_pal(imagg.get_at((x, y))))

        if y % 10 == 0:
            keys = key.get_pressed()
            if keys[K_ESCAPE] or event.get(QUIT):
                quit()
                exit()

            WIN.fill("#000000")
            WIN.blit(transform.smoothscale(imagg, SC_RES), (0, 0))
            MAINFONT.draw(WIN, (SC_RES[0]/2, 0), "\b".join(map(str, (int(CLOCK.get_fps()), (y/image_size[1])*100))), font_antialias, 1)
            CLOCK.tick(60)
            display.flip()

    while 1:
        WIN.fill("#000000")
        WIN.blit(transform.scale(imagg, SC_RES), (0, 0))

        keys = key.get_pressed()

        if keys[K_ESCAPE] or event.get(QUIT):
            quit()
            exit()
        elif keys[K_s]:
            image.save(imagg, f"{argv[1].split('.')[0]}_out.png")
            quit()
            exit()

        MAINFONT.draw(WIN, (SC_RES[0]/2, 0), "\b".join(map(str, (int(CLOCK.get_fps()), (y/image_size[1])*100))), font_antialias, 1)
        CLOCK.tick(60)
        display.flip()
