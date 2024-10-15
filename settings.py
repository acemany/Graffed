from pygame import (MOUSEBUTTONDOWN, MOUSEBUTTONUP, MOUSEWHEEL, FINGERMOTION, FINGERUP,
                    QUIT, KEYDOWN,
                    display, key, draw, event, font, mouse, time,
                    Vector2, Rect, Surface, Color,
                    init, quit as squit,
                    K_ESCAPE)
from pgti import TextInputVisualizer, TextInputManager
from atexit import register as regexit
from json import load, dumps
from pathlib import Path


class Button:
    def __init__(self, name: str, truth: bool):
        self.n: bool = truth
        self.name: str = name
        self.hovered: bool = False

    @property
    def switch(self) -> bool:
        self.n = not self.n
        return self.n

    def rect(self, y: float) -> tuple[float, float, float, float]:
        return (WIDTH//4, y, font_size+FONT.size(self.name)[0], font_size)

    def draw(self) -> Surface:
        out: Surface = Surface((font_size+FONT.size(self.name)[0]+3, font_size))
        out.fill(Cbg)

        if self.hovered:
            if self.n:
                draw.circle(out, (69, 69, 69), (font_size/2, font_size/2), 10)
                draw.circle(out, (255, 255, 255), (font_size/2, font_size/2), 10, 3)
                draw.circle(out, (255, 255, 255), (font_size/2, font_size/2), 5)  # out.blit(sw_on_over, (0, 0))
            else:
                draw.circle(out, (69, 69, 69), (font_size/2, font_size/2), 10)
                draw.circle(out, (255, 255, 255), (font_size/2, font_size/2), 10, 3)  # out.blit(sw_on, (0, 0))
        else:
            if self.n:
                draw.circle(out, (69, 69, 69), (font_size/2, font_size/2), 10)
                draw.circle(out, (127, 127, 127), (font_size/2, font_size/2), 10, 3)
                draw.circle(out, (127, 127, 127), (font_size/2, font_size/2), 5)  # out.blit(sw_off_over, (0, 0))
            else:
                draw.circle(out, (69, 69, 69), (font_size/2, font_size/2), 10)
                draw.circle(out, (127, 127, 127), (font_size/2, font_size/2), 10, 3)  # out.blit(sw_off, (0, 0))

        out.blit(FONT.render(self.name, True, (127, 127, 127)), (font_size+4, (font_size-font_size)/2))
        return out


class Slider:
    # slid_pw: int = 20
    # slid_h: int = 24
    # slid_SC: int = 4
    def __init__(self, name: str, number: float, min: float = 0, max: float = 100) -> None:
        self.min: float = min
        self.max: float = max
        self.width: float = WIDTH//2
        self.w: float = WIDTH//40
        self.height: float = font_size * 1.5
        self.name: str = name
        self.hovered: bool = False
        self.n: float = number

    def rect(self, y: int) -> tuple[float, float, float, float]:
        return (int(WIDTH/4+self.n*WIDTH/2/self.max), y, self.w, self.height)

    def draw(self) -> Surface:
        out: Surface = Surface((WIDTH/2+self.w, self.height))
        out.fill(Cbg)

        draw.rect(out, (69, 69, 69), (0, 0, self.width+self.w, self.height), 2)
        draw.rect(out, (255, 255, 255) if self.hovered else (69, 69, 69), (self.n*WIDTH/2/self.max, 0, self.w, self.height))

        out.blits((
            (FONT.render(f"{self.n}", True, (127, 127, 127)),
             (WIDTH/2-FONT.size(f"{self.n}")[0]-2, (self.height-FONT.get_height())/2)),
            (FONT.render(self.name, True, (127, 127, 127)),
             (2+self.w, (self.height-FONT.get_height())/2))))
        return out


def exitt():
    with open(file_path/"config.json", "w") as f:
        f.write(dumps(options_raw, indent=4))


regexit(exitt)

file_path = Path(__file__).parent
with open(file_path/"config.json", "r") as f:
    global options_raw
    options_raw = load(f)
    font_size: int = options_raw["font_size"]

init()
CLOCK: time.Clock = time.Clock()

Cbuttonua: Color = Color(63, 63, 63)  # (43, 52, 59)
Cbuttona: Color = Color(4, 104, 170)
Cbg: Color = Color(18, 18, 18)
Ctxt: Color = Color(207, 212, 218)
Ctxt2: Color = Color(164, 161, 171)

delta: float = 1/60
WIN = display.set_mode()
WIDTH, HEIGHT = SC_RES = Vector2(WIN.get_size())
FONT = font.SysFont('Monospace', font_size, bold=True)
tagsoffs: int = 0
page_sliding_offset: float = 0
ysly: float = 0
yslys: float = 0
ttr: float = 0
tagsearch: bool = False
tagsearchaa: bool = False
untag: bool = False
page_sliding: bool = False
PLysize = pitems = pdy = 1
settings_items: list[Button | Slider] = []
mouse_pos: Vector2 = Vector2()


tags_textarea: TextInputVisualizer = TextInputVisualizer(manager=TextInputManager(validator=lambda a: len(a) < 64),
                                                         font_object=FONT, font_color=Ctxt)
Rless_pics = Rect(0,         0,  50, 50)
Rmore_pics = Rect(50,        0,  50, 50)
Rprev_page = Rect(WIDTH-110, 0,  50, 50)
Rnext_page = Rect(WIDTH-60,  0,  50, 50)
Rreload = Rect(WIDTH/2-100,  0, 100, 50)
Rclear = Rect(WIDTH/2,       0, 100, 50)

for name, value in options_raw.items():
    print(f"{name} = {value!r}")
    if isinstance(value, bool):
        settings_items.append(Button(name, value))
    elif isinstance(value, (int, float)):
        settings_items.append(Slider(name, value, max=(5 if name == "tape_scale" else
                                                       100)))
settings_surfaces: list[Surface] = [Surface((0, 0)) for _ in range(len(settings_items))]


while True:
    ysly = min(max(ysly+yslys, -PLysize+HEIGHT), 0)
    yslys = yslys*0.95
    yslys = min(max(yslys, -100), 100)
    WIN.fill(Cbg)

    events: list[event.Event] = event.get()
    mouse_pos.update(mouse.get_pos())
    mouse_pressed: tuple[bool, bool, bool] = mouse.get_pressed()
    keys_pressed: key.ScancodeWrapper = key.get_pressed()

    tags_textarea.update(events)

    for j, i in enumerate(settings_items):
        if mouse_pressed[0] and i.hovered:
            if isinstance(i, Slider):
                i.n = min(max((mouse_pos.x-WIDTH/4-i.w/2)/WIDTH*2*i.max, i.min), i.max) if i.name == "tape_scale" else\
                    int(min(max((mouse_pos.x-WIDTH/4-i.w/2)/WIDTH*2*i.max, i.min), i.max))
            elif isinstance(i, Button):
                if event.get(MOUSEBUTTONUP, pump=False):
                    i.n = not i.n
            else:
                raise Exception("Invalid element \"{}\"")

        settings_surfaces[j] = i.draw()

    for e in events:
        if e.type == QUIT or keys_pressed[K_ESCAPE]:
            squit()
            exitt()
            quit()
        elif e.type == KEYDOWN:
            if e.key == K_ESCAPE:
                squit()
                exitt()
                quit()
        elif e.type == MOUSEBUTTONDOWN and e.button == 1:
            for j, i in enumerate(settings_items):
                if i.hovered and type(i) is Button:
                    i.n = i.switch
                    options_raw[i.name] = i.n
                    settings_surfaces[j] = i.draw()
            mouse_down = True
            if PLysize > HEIGHT and Rect((WIDTH-10, -HEIGHT*ysly/PLysize, 10, HEIGHT/PLysize*HEIGHT)).collidepoint(mouse_pos):
                page_sliding = True
                page_sliding_offset = -mouse_pos.y-HEIGHT*ysly/PLysize
        elif e.type == MOUSEBUTTONUP:
            page_sliding = False
        elif e.type == FINGERMOTION and not page_sliding:
            yslys += e.dy*HEIGHT/delta
        elif e.type == FINGERUP:
            mouse.set_pos(0, 0)
        elif e.type == MOUSEWHEEL:
            yslys += e.y*HEIGHT*delta
    if mouse_pressed[0]:
        if page_sliding:
            yslys = (((-page_sliding_offset-mouse_pos.y)*PLysize/HEIGHT-ysly)*delta+yslys)*4

    _: int = 4
    for j, i in enumerate(settings_surfaces):
        k: Slider | Button = settings_items[j]
        k.hovered = Rect(k.rect(_)).collidepoint(mouse_pos)
        WIN.blit(i, (WIDTH/4, _))
        _ += i.get_height() + 4
    # WIN.blits(
    #     ((FONT.render(f"{i[0]} = {i[1]}", 1, Ctxt2), (0, 25*j))
    #      for j, i in enumerate((k for k in locals().items() if (k[0][:2] and k[0] not in ("MOUSEBUTTONDOWN", "KEYDOWN", "MOUSEBUTTONUP", "FINGERMOTION", "FINGERUP", "QUIT", "MOUSEWHEEL",
    #                                                                                       "display", "key", "draw", "event", "font", "mouse", "time",
    #                                                                                       "Vector2", "Rect", "Surface",
    #                                                                                       "init", "squit",
    #                                                                                       "K_ESCAPE",
    #                                                                                       "TextInputVisualizer", "TextInputManager",
    #                                                                                       "load", "dumps",
    #                                                                                       "Path",
    #                                                                                       "regexit",))))))
    display.flip()
    delta = CLOCK.tick(60)/1000
