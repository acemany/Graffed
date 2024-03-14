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
    display.set_icon(image.load("assets\\icon.bmp").convert())

    colors = (("#EEA5A3", "#CB7689", "#9D5A64"),  # BROWN
              ("#FFF0F0", "#FFE8D0", "#FFC3B5"),  # BEIGE
              ("#C198FF", "#997EAB", "#725BAD"),  # VIOLET
              ("#FFCCFC", "#FF9CDB", "#FF7CBA"),  # PINK
              ("#FFAAAA", "#FF5273", "#CE3B56"),  # RED
              ("#FFBA8F", "#FF7C5B", "#D75947"),  # ORANGE
              ("#FFFF86", "#FFEB00", "#F6BA00"),  # YELLOW
              ("#C3FF77", "#48D155", "#009352"),  # GREEN
              ("#00CEFF", "#009BFF", "#0076ED"),  # BLUE
              ("#9C9FAD", "#CED1D9", "#FFFFFF"),  # WHITE
              ("#1F1F29", "#444454", "#6D6F7F"),  # BLACK
              ("#dfecff", "#73adff", "#4f98ff"),
              ("#b8d5ff", "#43b85b", "#68c67b"),
              ("#2C7F3D", "#fa963e", "#faaa63"),
              ("#fe4b4b", "#fe6e6e", "#233055"),
              ("#1C2643", "#17133c", "#151c34"),
              ("#233056", "#1c2644", "#0d1221"),
              ("#0D1221", "#52709c", "#748caf"),
              ("#4f5977", "#768ba9", "#868890"),
              ("#e7820a", "#b4b4b4", "#eefc08"),
              ("#F2F932", "#8781bd", "#30d5c8"),
              ("#3BCBFF", "#BD70D7", "#AB4873"),
              ("#31a93a", "#ec4058", "#e8bb00"))
    colors_size = (len(colors[0])*50, len(colors)*50)
    color = "#444454"
    font_antialias = 1

    CLOCK = time.Clock()
    MAINFONT = font.SysFont("consolas", 16)

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
        WIN.blit(MAINFONT.render("\b".join(map(str, (int(CLOCK.get_fps()), mouse_pos))), font_antialias, "#9C9FAD"), (SC_RES[0]/2, 0))
        CLOCK.tick(256)
        display.flip()
    quit()
