import pygame as pg

import util

pg.font.init()

class Label:
    def __init__(self, text: str, size = 32, color = "white"):

        self.FONT = pg.font.Font(None, size)
        self.image = self.FONT.render(text, True, color)
        self.text = text
        self.color = color

    def change_text(self, text: str):
        self.image = self.FONT.render(text, True, self.color)
        self.text = text

    def draw(self, display, position = (0, 0), mode=""):
        display.blit(self.image, util.align(position, self.image,  mode))