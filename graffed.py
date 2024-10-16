from pygame import (KEYDOWN, MOUSEBUTTONDOWN, MOUSEBUTTONUP, MOUSEWHEEL, QUIT, TEXTINPUT,
                    display, event, font, image, mouse, time, transform, draw,
                    K_ESCAPE, K_LCTRL, K_LSHIFT,
                    Color, Surface, Vector2,
                    K_l, K_o, K_s,
                    init, quit as squit)
from potaget import open_file_as, save_file_as, c_p_r
from sys import argv, exit
from pathlib import Path


# CLASSES
class Camera:
    def __init__(self, pos: tuple[int, int] = (0, 0)):
        self.x, self.y = -pos[0], -pos[1]

    @property
    def pos(self) -> tuple[int, int]:
        return (int(self.x), int(self.y))

    def update(self, to: tuple[float, float]):
        self.x += to[0]
        self.y += to[1]


class Slider:
    def __init__(self, pos: tuple[int, int], size: tuple[int, int],
                 scale: int, min: int, max: int, base_color: str = '#454545', slider_color: str = '#565656'):
        self.max = max
        self.x, self.y = pos
        self.w, self.h = size
        self.min: float = min
        self._num: float = self.min
        self.base_color: str = base_color
        self.scale_ratio = scale/max
        self.slider_color = slider_color
        self.scale = max*self.scale_ratio

    @property
    def num(self) -> int:
        return int(self._num)

    @num.setter
    def num(self, value: int | float):
        self._num = int(value)

    def slide_check(self):
        return self.x+self._num*self.scale_ratio <\
            mouse_pos[0] < self.x+self.w+self._num*self.scale_ratio and\
            self.y < mouse_pos[1] < self.y+self.h

    def draw(self):
        draw.aaline(WIN, self.base_color, (self.x,            self.y+self.h/2),
                                          (self.x+self.scale, self.y+self.h/2))
        draw.rect(WIN,   self.base_color, (self.x+self._num*self.scale_ratio,   self.y,
                                           self.w,   self.h))
        draw.rect(WIN, self.slider_color, (self.x+self._num*self.scale_ratio+1, self.y+1,
                                           self.w-2, self.h-2))


class Font:
    def __init__(self, pos: tuple[int, int], color: str = '#BBBBBB', scale: int = 6, name: str = 'Arial'):
        self.font = font.SysFont(name, scale)
        self.w = self.font.size('n')[0]
        self.h = self.font.get_height()
        self.indicator_pos = 0
        self.x, self.y = pos
        self.color = color
        self.text = ""

    def text_input(self, key_in: list[event.Event], text_in: list[event.Event], lining: bool = True):
        for i in text_in:
            char = i.__dict__["text"]
            if char != "":
                self.text += char
        for i in key_in:
            key = i.__dict__["unicode"]
            if key == "\x08":
                self.text = self.text[:-1]
            elif key == "\r":
                if lining:
                    self.text += "\n"
                else:
                    return True
        return False

    def draw(self, pos: tuple[int, int], text: str, antialias: bool, centering: int = 0):
        if centering:
            WIN.blits([(self.font.render(
                       text, antialias, self.color), (pos[0]-self.font.size(text)[0]/2, pos[1]+y*self.h))
                       for y, text in enumerate(text.replace('\b', ' | ').split('\n'))])
        else:
            WIN.blits([(self.font.render(
                       text, antialias, self.color), (pos[0], pos[1]+y*self.h))
                       for y, text in enumerate(text.replace('\b', ' | ').split('\n'))])

    def blit(self, antialias: bool):
        WIN.blits([(self.font.render(
                   text, antialias, self.color), (self.x, self.y+y*self.h))
                   for y, text in enumerate(self.text.split('\n'))])


class Pic:
    def __init__(self, path_to_file: str):
        rimage = image.load(path_to_file).convert()
        self.filename = path_to_file
        self.rimage = rimage
        self.surfsize = (rimage.get_width(), rimage.get_height())
        self.image = transform.scale(self.rimage, (self.surfsize[0]*scale_ratio,
                                                   self.surfsize[1]*scale_ratio))

    def resize(self):
        self.image = transform.scale(self.rimage, (self.surfsize[0]*scale_ratio,
                                                   self.surfsize[1]*scale_ratio))

    def regen(self):
        self.image = transform.scale(self.rimage, (self.surfsize[0]*scale_ratio,
                                                   self.surfsize[1]*scale_ratio))

    def draw(self, offset: tuple[float, float]):
        WIN.blit(self.image, (-offset[0]*scale_ratio,
                              -offset[1]*scale_ratio))

    def save(self, filename: str = ''):
        image.save(self.rimage, str(gamedir/'{self.filename if filename == ''else filename}'))

    # INSTRUMENTS
    def pencil(self):
        width = scale_slider.num
        draw.line(self.rimage, color, world_l_pos, world_m_pos, width)
        draw.circle(self.rimage, color, world_l_pos, width/2)
        draw.circle(self.rimage, color, world_m_pos, width/2)
        self.image = transform.scale(self.rimage, (self.surfsize[0]*scale_ratio,
                                                   self.surfsize[1]*scale_ratio))

    def line(self):
        liline = world_m_pos-world_p_pos
        k = liline.y/liline.x if liline.x != 0 and liline.y != 0 else 1e+32
        truth_width = int(scale_slider.num*((2/(2-min(abs(k), abs(1/k))))**0.5))  # holy moly, dont try to understand, it just works
        draw.line(self.rimage, color, world_p_pos, world_m_pos, truth_width)
        # TODO: make soft eges
        # draw.circle(self.rimage, color, world_p_pos, width/2)
        # draw.circle(self.rimage, color, world_m_pos, width/2)
        self.image = transform.scale(self.rimage, (
            self.surfsize[0]*scale_ratio,
            self.surfsize[1]*scale_ratio))

    def rect(self):
        pos1 = screen_to_world((max(pen_pos[0], mouse_pos[0]), max(mouse_pos[1], pen_pos[1])))
        pos2 = screen_to_world((min(pen_pos[0], mouse_pos[0]), min(mouse_pos[1], pen_pos[1])))
        draw.rect(self.rimage, color, (*pos2, pos1[0]-pos2[0], pos1[1]-pos2[1]))
        self.image = transform.scale(self.rimage, (self.surfsize[0]*scale_ratio,
                                                   self.surfsize[1]*scale_ratio))

    def pipette(self) -> tuple[int, int, int]:
        try:
            colour: Color = self.rimage.get_at(tuple(map(int, world_m_pos)))
            return colour.r, colour.g, colour.b
        except IndexError:
            return color


# FUNCTIONS
def rect_to_hcv(color: tuple[int, int, int], x: int, y: int):
    saturation = (255-x)/32+1
    height = 255-y
    return (int(127-(127-color[0])/saturation)*height//255,
            int(127-(127-color[1])/saturation)*height//255,
            int(127-(127-color[2])/saturation)*height//255)


def rgb_to_hex(color: tuple[int, int, int] = (255, 0, 0)):
    hr = f"{int(color[0]): 0x}"
    hg = f"{int(color[1]): 0x}"
    hb = f"{int(color[2]): 0x}"
    return f"""#{str(hr if color[0] > 9 else hr+'0')
                 }{str(hg if color[1] > 9 else hg+'0')
                   }{str(hb if color[2] > 9 else hb+'0')}"""


def hex_to_rgb(color: str = '#ff0000'):
    color = color.replace('#', '', 1)
    return (int(color[0]+color[1], base=16),
            int(color[2]+color[3], base=16),
            int(color[4]+color[5], base=16))


def screen_to_world(pos: tuple[float, float] | Vector2 | list[float]):
    return Vector2((pos[0]+CAMERA.pos[0])/scale_ratio+GRAFFED_FILE.surfsize[0]/2,
                   (pos[1]+CAMERA.pos[1])/scale_ratio+GRAFFED_FILE.surfsize[1]/2)


if __name__ == "__main__":
    # INIT
    init()
    gamedir = Path(__file__).parent
    WIN = (display.set_mode())
    SC_RES = WIN.get_size()

    display.set_icon(image.load(gamedir/'assets/icon.bmp').convert())

    # VARIABLES
    pen_pos = (0, 0)
    color: tuple[int, int, int] = (255, 0, 0)
    scale_ratio = 1
    font_antialias = True
    change_color = False
    mouse_pos = Vector2()
    last_mouse_pos = Vector2(0, 0)
    slider_move = (False, 0)
    editor_category = "environment"
    instrument = "line"  # pipette, pencil, line, rect
    graffed_file_name: str = "testing.png" if len(argv) == 1 else argv[1]

    # SURFACES
    TOOLBAR_SURFACE = Surface((200, SC_RES[1]))
    draw.rect(TOOLBAR_SURFACE, '#454545', (0,  0,  200, SC_RES[1]))
    draw.rect(TOOLBAR_SURFACE, '#676767', (0,  0,  198, SC_RES[1]))
    pipette_icon = image.load(gamedir/'assets/instruments/pipette.png')
    pencil_icon = image.load(gamedir/'assets/instruments/pencil.png')
    line_icon = image.load(gamedir/'assets/instruments/line.png')
    rect_icon = image.load(gamedir/'assets/instruments/rect.png')
    TISize = line_icon.get_size()[0]
    pipette_icon.set_colorkey('#FF00FF')
    pencil_icon .set_colorkey('#FF00FF')
    line_icon   .set_colorkey('#FF00FF')
    rect_icon   .set_colorkey('#FF00FF')
    TOOLBAR_SURFACE.blits(((pipette_icon, (6,        5)),
                           (pencil_icon,  (6,        5+TISize)),
                           (line_icon,    (6+TISize, 5)),
                           (rect_icon,    (6+TISize, 5+TISize))))

    # CLASSES
    CLOCK = time.Clock()
    GRAFFED_FILE = Pic(graffed_file_name)
    MAINFONT = Font((0, 0), '#9A9A9A', 16)
    color_font = Font((0, 0), '#9A9A9A', 16)
    CAMERA = Camera((SC_RES[0]//2, SC_RES[1]//2))
    slider_red = Slider((6, 76), (TISize//2, TISize), 180, 0, 255, '#CC3333')
    slider_green = Slider((6, 76+25), (TISize//2, TISize), 180, 0, 255, '#33CC33')
    slider_blue = Slider((6, 76+50), (TISize//2, TISize), 180, 0, 255, '#3333CC')
    scale_slider = Slider((6, 76+75), (TISize//2, TISize), 180, 1, 256, '#454545')
    slider_red.num, slider_green.num, slider_blue.num = color

    while True:
        WIN.fill('#404040')
        GRAFFED_FILE.draw((CAMERA.pos[0]/scale_ratio+GRAFFED_FILE.surfsize[0]/2,
                           CAMERA.pos[1]/scale_ratio+GRAFFED_FILE.surfsize[1]/2))

        keys_down = event.get(KEYDOWN)
        text_in = event.get(TEXTINPUT)

        mouse_keys_down = event.get(MOUSEBUTTONDOWN)
        mouse_keys_up = event.get(MOUSEBUTTONUP)
        mouse_keys = mouse.get_pressed()
        mouse_pos.update(mouse.get_pos())
        mouse_x, mouse_y = mouse_pos
        world_l_pos = screen_to_world(last_mouse_pos)
        world_m_pos = screen_to_world(mouse_pos)
        world_p_pos = screen_to_world(pen_pos)

        for i in event.get(MOUSEWHEEL, 0):
            new = scale_ratio+i.__dict__['y']/8
            if 0 < new < 32:
                scale_ratio = new
                GRAFFED_FILE.resize()

        if change_color:
            if color_font.text_input(keys_down, text_in, False):
                change_color = False
                try:
                    color = hex_to_rgb(color_font.text)
                    slider_red.num, slider_green.num, slider_blue.num = color
                except ValueError as e:
                    print(e)

        if event.get(QUIT):
            squit()
            exit()
        for i in mouse_keys_down:
            if i.__dict__['button'] == 1:
                if mouse_x < 200:
                    if slider_red.slide_check():
                        slider_move = (True, 0)
                    elif slider_green.slide_check():
                        slider_move = (True, 1)
                    elif slider_blue .slide_check():
                        slider_move = (True, 2)
                    elif scale_slider.slide_check():
                        slider_move = (True, 3)
                    else:
                        slider_move = (False, 0)
                        if c_p_r(mouse_pos.x, mouse_pos.y,   6,        80,       98,         20):
                            color_font.text = rgb_to_hex(color)
                            change_color = True
                        elif c_p_r(mouse_pos.x, mouse_pos.y, 6,        5,        TISize, TISize):
                            instrument = "pipette"
                        elif c_p_r(mouse_pos.x, mouse_pos.y, 6,        5+TISize, TISize, TISize):
                            instrument = "pencil"
                        elif c_p_r(mouse_pos.x, mouse_pos.y, 6+TISize, 5,        TISize, TISize):
                            instrument = "line"
                        elif c_p_r(mouse_pos.x, mouse_pos.y, 6+TISize, 5+TISize, TISize, TISize):
                            instrument = "rect"
                elif instrument == "line" or instrument == "rect" and mouse_x > 200:
                    pen_pos = mouse_pos[:]
        for i in mouse_keys_up:
            if i.__dict__['button'] == 1:
                slider_move = (False, 0)
                if mouse_x >= 200:
                    if instrument == "line":
                        GRAFFED_FILE.line()
                    elif instrument == "rect":
                        GRAFFED_FILE.rect()
        for i in keys_down:
            if i.__dict__['key'] == K_ESCAPE:
                squit()
                exit()
            if i.__dict__['key'] == K_LCTRL:
                if i.__dict__['key'] == K_s:
                    GRAFFED_FILE.save(save_file_as() if i.__dict__['key'] == K_LSHIFT else '')
                elif i.__dict__['key'] == K_l:
                    GRAFFED_FILE.__init__(graffed_file_name)
                elif i.__dict__['key'] == K_o:
                    try:
                        graffed_file_name = open_file_as()
                        assert not not graffed_file_name
                        GRAFFED_FILE.__init__(graffed_file_name)
                    except FileNotFoundError:
                        pass

        if mouse_keys[0]:
            if mouse_x < 200:
                if slider_move[0]:
                    slid = (slider_red, slider_green, slider_blue, scale_slider)[slider_move[1]]
                    slid.num = max(min(mouse_x/slid.scale_ratio-12, slid.max), slid.min)
                    color = (slider_red.num, slider_green.num, slider_blue.num)
            else:
                slider_move = (False, 0)
                if instrument == "pencil":
                    GRAFFED_FILE.pencil()
                elif instrument == "pipette":
                    color = GRAFFED_FILE.pipette()
                    slider_red  .num = color[0]
                    slider_green.num = color[1]
                    slider_blue .num = color[2]
                elif instrument == "line":
                    liline = mouse_pos-pen_pos
                    k = liline.y/liline.x if liline.x != 0 and liline.y != 0 else 1e+32
                    width = int(scale_slider.num*scale_ratio*((2/(2-min(abs(k), abs(1/k))))**0.5))
                    # draw.circle(WIN, (0, 0, 0), pen_pos,   width/2)
                    # draw.circle(WIN, (0, 0, 0), mouse_pos, width/2)
                    draw.line(WIN, color, pen_pos, mouse_pos, width)

                elif instrument == "rect":
                    pos1 = (max(pen_pos[0], mouse_pos[0]), max(mouse_pos[1], pen_pos[1]))
                    pos2 = (min(pen_pos[0], mouse_pos[0]), min(mouse_pos[1], pen_pos[1]))
                    draw.rect(WIN, color, (*pos2, pos1[0]-pos2[0], pos1[1]-pos2[1]))
        elif mouse_keys[1]:
            CAMERA.update(((last_mouse_pos[0]-mouse_pos[0]),
                           (last_mouse_pos[1]-mouse_pos[1])))
        last_mouse_pos = mouse_pos.xy

        WIN.blit(TOOLBAR_SURFACE, (0, 0))
        draw.rect(WIN, color, (6, 56, TISize, TISize))
        MAINFONT    .draw((8+TISize, 56), f"""{color_font.text.upper() if change_color else
                                               rgb_to_hex(color).upper()}""", font_antialias, 0)
        slider_red  .draw()
        slider_green.draw()
        slider_blue .draw()
        scale_slider.draw()

        MAINFONT.draw((SC_RES[0]//2, 0), '\b'.join(map(str, (scale_ratio*100//1,
                                                             instrument,
                                                             mouse_pos,
                                                             graffed_file_name))), font_antialias, 1)
        CLOCK.tick(60)
        display.flip()
