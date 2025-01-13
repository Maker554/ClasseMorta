import pygame as pg

import util

COLOR_INACTIVE = pg.Color('lightskyblue3')
COLOR_ACTIVE = pg.Color('dodgerblue2')

pg.font.init()

class InputBox:

    def __init__(self, x, y, w, h, text='', private = False):

        self.FONT = pg.font.Font(None, int(h * 0.8))

        self.height = h
        self.private = private
        self.fake_rect = pg.Rect(x, y, w, h)
        self.rect = pg.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = self.FONT.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.set_active()
            elif self.active:
                self.set_active(False)

        if event.type == pg.KEYDOWN:
            if self.active:
                if event.key == pg.K_RETURN:
                    self.set_active()

                elif event.key == pg.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                if not self.private:
                    self.txt_surface = self.FONT.render(self.text, True, "white")
                else:
                    self.txt_surface = self.FONT.render(len(self.text)*'#', True, "white")

    def update(self):
        # Resize the box if the text is too long.
        width = max(self.fake_rect.w, self.txt_surface.get_width() + 40)
        self.fake_rect.w = width

    def draw(self, screen, mode="top_left"):
        # Blit the rect.
        self.rect = pg.Rect(
            util.align_x(self.fake_rect.x, self.fake_rect.w, mode),
            util.align_y(self.fake_rect.y, self.fake_rect.h, mode),
            self.fake_rect.w,
            self.fake_rect.h
        )

        pg.draw.rect(screen, self.color, self.rect, 5)
        centering = self.height * 0.3

        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x + centering, self.rect.y + centering))

    def set_active(self, state = None):
        if state is None:
            state = not self.active
        self.active = state
        self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE