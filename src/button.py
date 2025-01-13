import pygame as pg

import util

COLOR_INACTIVE = pg.Color('white')
COLOR_ACTIVE = pg.Color((50, 50, 50))

pg.font.init()

class CallBack:
    def run(self):
        pass

class Button:
    def __init__(self, x, y, w, h, text='',):

        self.height = h
        self.fake_rect = pg.Rect(x, y, w, h)
        self.rect = pg.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = pg.font.Font(None, int(h * 0.8)).render(text, True, "black")
        self.active = False

    def handle_event(self, event, callback: CallBack = None):

        session = None

        if event.type == pg.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                if callback is not None:
                    session = callback.run()
                self.color = COLOR_ACTIVE
        if event.type == pg.MOUSEBUTTONUP:
            self.color = COLOR_INACTIVE

        return session

    def draw(self, screen, mode="top_left"):
        # Blit the rect.
        self.rect = pg.Rect(
            util.align_x(self.fake_rect.x, self.fake_rect.w, mode),
            util.align_y(self.fake_rect.y, self.fake_rect.h, mode),
            self.fake_rect.w,
            self.fake_rect.h
        )

        pg.draw.rect(screen, self.color, self.rect, 0)
        centering = self.height * 0.3

        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x + centering, self.rect.y + centering))