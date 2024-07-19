from pygame import (display, draw, event, font, image, key, mouse, time,
                    Rect, Vector2,
                    init, quit,
                    K_ESCAPE,
                    QUIT)


def box_check(point: Vector2, box: Rect):
    return box.collidepoint(point)


if __name__ == "__main__":
    init()
    WIN = (display.set_mode())
    SC_RES = WIN.get_size()
    colors = (("#E79F9D", "#C57184", "#985660"),
              ("#FFF9F7", "#FFDFC8", "#FFBCAE"),
              ("#BA92FF", "#9476E3", "#6E58A9"),
              ("#FFC4F4", "#FF9ED9", "#F777B4"),
              ("#FFA4A4", "#FF4E6F", "#C73853"),
              ("#FFB389", "#FF7758", "#D15544"),
              ("#FFFF81", "#FFE200", "#F0B300"),
              ("#BBFF72", "#45C952", "#008F50"),
              ("#00C9FF", "#0096FF", "#0071E5"),
              ("#FFFFFF", "#C6C9D3", "#9699A9"),
              ("#696B7C", "#424252", "#1E1E28"))
    display.set_icon(image.load("assets/icon.bmp").convert())

    colors_size = (len(colors[0])*50, len(colors)*50)
    color = colors[-1][-1]

    CLOCK = time.Clock()
    MAINFONT = font.SysFont("consolas", 16, bold=True)

    while True:
        WIN.fill(color)

        mouse_keys = mouse.get_pressed()
        mouse_x, mouse_y = mouse_pos = Vector2(mouse.get_pos())

        if key.get_pressed()[K_ESCAPE] or event.get(QUIT):
            break

        if mouse_keys[0]:
            if mouse_y < colors_size[0] and mouse_x < colors_size[1]:
                for x, clrs in enumerate(colors):
                    for y, clr in enumerate(clrs):
                        if Rect(x*50, y*50, 50, 50).collidepoint(mouse_pos):
                            color = colors[x][y]
        [[draw.rect(WIN, clr, (x*50, y*50, 50, 50))
          for y, clr in enumerate(clrs)]
         for x, clrs in enumerate(colors)]
        WIN.blits([(MAINFONT.render(i, 1, "#424252"), (2, 2+16*j)) for j, i in enumerate(map(str, (int(CLOCK.get_fps()), str(mouse_pos)[1:-1], color)))])
        CLOCK.tick(60)
        display.flip()
    quit()
