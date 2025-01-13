import pygame as pg

import util

pg.font.init()

class Label:
    def __init__(self, text: str, size = 32, color = "white"):

        FONT = pg.font.Font(None, size)
        self.image = FONT.render(text, True, color)

    def draw(self, display, position = (0, 0), mode=""):
        display.blit(self.image, util.align(position, self.image,  mode))