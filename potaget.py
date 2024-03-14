from tkinter.filedialog import askopenfilename, asksaveasfilename
from pygame import (display, event, font, Surface, Vector2, Rect)
from datetime import datetime, timedelta, timezone
from platform import system
from typing import Tuple
from tkinter import Tk


__all__ = ["c_c_c", "c_c_r", "c_r_r", "c_p_c", "c_p_r", "orient",
           "log", "open_file_as", "save_file_as",
           "MainFont"]


class MainFont:
    def __init__(self, pos: Tuple[int, int], color: str = "#BBBBBB", scale: int = 6):
        self.WIN = display.get_surface()
        self.font = font.Font("gameFont.woff", scale)
        self.w = self.font.size("n")[0]
        self.h = self.font.get_height()
        self.indicator_pos = 0
        self.x, self.y = pos
        self.color = color
        self.text = ""

    def text_input(self, key_in: event.Event, text_in: event.Event, lining: bool = True):
        key = key_in .__dict__["unicode"]
        char = text_in.__dict__["text"]
        if key == "\x08":
            self.text = self.text[:-1:]
        elif lining and key == "\r":
            self.text += "\n"
        elif char != "":
            self.text += char
        print(text_in, " ", char)

    def draw(self, text: str, antialians: int, pos: Tuple[int, int], centering: int = 0, bgcolor: str = None):
        if bgcolor is not None:
            if centering:
                self.WIN.blits([(self.font.render(text, antialians, self.color, bgcolor),
                                (pos[0]-self.font.size(text)[0]/2, pos[1]+y*self.h))
                                for y, text in enumerate(text.split("\n"))])
            else:
                self.WIN.blits([(self.font.render(text, antialians, self.color, bgcolor),
                                (pos[0], pos[1]+y*self.h))
                                for y, text in enumerate(text.split("\n"))])
        else:
            if centering:
                self.WIN.blits([(self.font.render(text, antialians, self.color),
                                (pos[0]-self.font.size(text)[0]/2, pos[1]+y*self.h))
                                for y, text in enumerate(text.split("\n"))])
            else:
                self.WIN.blits([(self.font.render(text, antialians, self.color),
                                (pos[0], pos[1]+y*self.h))
                                for y, text in enumerate(text.split("\n"))])

    def drat(self, text: str, antialians: int, pos: Tuple[int, int], win: Surface, centering: int = 0):
        if centering:
            win.blits([(self.font.render(text, antialians, self.color),
                       (pos[0]-self.font.size(text)[0]/2, pos[1]+y*self.h))
                       for y, text in enumerate(text.split("\n"))])
        else:
            win.blits([(self.font.render(text, antialians, self.color),
                       (pos[0], pos[1]+y*self.h))
                       for y, text in enumerate(text.split("\n"))])

    def blit(self, antialians: int):
        self.WIN.blits([(self.font.render(text, antialians, self.color),
                        (self.x, self.y+y*self.h))
                        for y, text in enumerate(self.text.split("\n"))])


def log(e: str):
    with open("log.txt", "a") as file:
        file.write(f"\n{datetime.now(timezone(timedelta(hours=3, minutes=0), 'Moscow'))} - {e}\n")


def open_file_as(file_type: str):
    "Ask the user to select a file to open"
    root = Tk()
    root.withdraw()
    root.wm_attributes("-topmost", 1)
    if file_type is None or (system() == "Darwin"):
        file_path = askopenfilename(parent=root)
    else:
        file_types = [("Image file", "*.png;*.jpg;*.jpeg;*.ico;*.gif;*.bmp"), ("All files", "*")]\
            if file_type == "image"else\
                     [("Micdustry save file", "*.msav"), ("All files", "*")] if file_type == "msave" else\
                     [("All files", "*")]
        file_path = askopenfilename(parent=root, filetypes=file_types)
    root.update()

    return file_path if file_path else None


def save_file_as(file_type: str):
    "Ask the user to select a file to save"
    root = Tk()
    root.withdraw()
    root.wm_attributes("-topmost", 1)
    if file_type is None or (system() == "Darwin"):
        file_path = asksaveasfilename(parent=root)
    else:
        file_types = [("Image file", "*.png;*.jpg;*.jpeg;*.ico;*.gif;*.bmp"), ("All files", "*")]\
            if file_type == "image" else\
                     [("Micdustry save file", "*.msav"), ("All files", "*")]if file_type == "msave"else\
                     [("All files", "*")]
        file_path = asksaveasfilename(parent=root, filetypes=file_types)
    root.update()
    return file_path if file_path else None


def orient(c: Vector2, a: Vector2, b: Vector2):
    lin = b-a
    return (lin.y*c.x-lin.x*c.y+b.x*a.y-b.y*a.x)/lin.length()


def c_c_c(cx1, cy1, cr1, cx2, cy2, cr2) -> bool:
    return Vector2.distance_to((cx1, cy1), (cx2, cy2)) < cr1+cr2


def c_c_r(cx, cy, cr, bx, by, bw, bh):
    return ((max(bx, min(cx, bx+bw))-cx)**2+(max(by, min(cy, by+bh))-cy)**2)**0.5 < cr


def c_r_r(bx1, by1, bw1, bh1, bx2, by2, bw2, bh2) -> bool:
    return Rect.colliderect((bx1, by1, bw1, bh1), (bx2, by2, bw2, bh2))


def c_p_c(px, py, cx, cy, cr) -> bool:
    return Vector2.distance_to((px, py), cx, cy) < cr


def c_p_r(px, py, rx, ry, rw, rh) -> bool:
    return Rect(rx, ry, rw, rh).collidepoint(px, py)
