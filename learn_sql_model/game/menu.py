from pydantic import BaseModel
from typing import Tuple, Callable

import pygame

screen_sizes = [
    (480, 360),    # 360p
    (640, 480),    # VGA
    (800, 600),    # SVGA
    (1024, 768),   # XGA
    (1280, 720),   # HD 720p
    (1366, 768),   # HD 1366x768
    (1600, 900),   # HD+ 1600x900
    (1920, 1080),  # Full HD 1080p
    (2560, 1440),  # 2K / QHD 1440p
    (3840, 2160)   # 4K / UHD 2160p
]



class MenuItem(BaseModel):
    display_text: str
    on_click: Callable = None
    text_color: Tuple[str, str, str] = (0, 0, 0)        




class Menu:
    def __init__(self, game):
        pygame.font.init()

        self.game = game
        self.hamburger = Hamburger(game)
        self.menu_width = min(max(200, self.game.screen.get_width()
                              * 0.8), self.game.screen.get_width())
        self.menu_height = min(max(200, self.game.screen.get_height()
                                   * 0.8), self.game.screen.get_height())
        self.x = (self.game.screen.get_width() - self.menu_width) / 2
        self.y = (self.game.screen.get_height() - self.menu_height) / 2
        self.color = (100, 100, 100)
        self.is_menu_open = False

        self.surface = pygame.Surface((self.menu_width, self.menu_height))
        self.font = pygame.font.SysFont("", 50)
        self.screen_size_index = False
        self.padding = 10

        self.items = [
            MenuItem(display_text='Menu'),
            MenuItem(display_text='Screen Size'),
            MenuItem(display_text=f'{self.game.screen.get_width()}x{self.game.screen.get_height()}', color=(50, 0, 0))
        ]

    def render(self):
        if self.is_menu_open:
            self.surface.fill(self.color)

            pos = (self.padding, self.padding)
            for item in self.items:
                text = self.font.render(item.display_text, True, item.text_color)
                self.surface.blit(text, pos)
                pos = (pos[0], pos[1] + 50)

            # put text in the menu surface
            # text = self.font.render("Menu", True, (0, 0, 0))
            # self.surface.blit(text, (0, 0))
            # text = self.font.render("Screen Size", True, (0, 0, 0))
            # self.surface.blit(text, (0, 60))
            # text = self.font.render(
            #     f'{self.game.screen.get_width()}x{self.game.screen.get_height()}', True, (25, 25, 25))
            # self.surface.blit(text, (10, 120))
            #
            self.game.screen.blit(self.surface, (self.x, self.y))
            
        self.hamburger.render()

    def get_mouse_pos(self):
        'get mouse position relative to self.surface'
        x, y = pygame.mouse.get_pos()
        return x - self.x, y - self.y

    def handle_click(self):
        self.hamburger.handle_click(self)
        pos = self.get_mouse_pos()
        print(pos)
        if pos[1] > 120 and pos[1] < 180 and pos[0] > 0 and pos[0] < self.menu_width:
            if self.screen_size_index is False:
                self.screen = pygame.display.set_mode(screen_sizes[0])
                self.screen_size_index = 0
            if self.screen_size_index == len(screen_sizes) - 1:
                self.screen_size_index = 0
            else:
                self.screen_size_index += 1
            self.screen = pygame.display.set_mode(screen_sizes[self.screen_size_index])


class Hamburger:
    def __init__(self, game):

        self.game = game
        self.hamburger_width = 50
        self.bar_height = self.hamburger_width / 4
        self.bar_spacing = self.hamburger_width / 20
        self.hamburger_height = self.bar_height * 3 + self.bar_spacing * 2
        self.x = self.game.screen.get_width() - self.hamburger_width - 20
        self.y = 20
        self.color = (100, 100, 100)
        self.rect = pygame.Rect(self.x, self.y, self.hamburger_width,
                                self.hamburger_height)
        self.surface = pygame.Surface(
            (self.hamburger_width, self.hamburger_height))

    def render(self):
        pygame.draw.rect(self.surface, self.color,
                         (0, 0, self.hamburger_width, self.bar_height),)
        pygame.draw.rect(self.surface, self.color,
                         (0, self.bar_height + self.bar_spacing, self.hamburger_width, self.bar_height),)
        pygame.draw.rect(self.surface, self.color,
                         (0, 2 * (self.bar_height + self.bar_spacing), self.hamburger_width, self.bar_height),)

        self.game.screen.blit(self.surface, (self.x, self.y))


    def handle_click(self, menu):
        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            menu.is_menu_open = not menu.is_menu_open
