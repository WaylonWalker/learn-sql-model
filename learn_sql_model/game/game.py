import atexit

import pygame
from typer import Typer
from websocket import create_connection

from learn_sql_model.config import get_config
from learn_sql_model.console import console
from learn_sql_model.factories.hero import HeroFactory
from learn_sql_model.models.hero import HeroCreate, HeroDelete, HeroUpdate, Heros

speed = 10

pygame.font.init()  # you have to call this at the start,
# if you want to use this module.
my_font = pygame.font.SysFont("Comic Sans MS", 30)

config = get_config()

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


class Menu:
    def __init__(self, game):

        self.game = game
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

    def render(self):
        if self.is_menu_open:
            self.surface.fill(self.color)
            # put text in the menu surface
            text = self.font.render("Menu", True, (0, 0, 0))
            self.surface.blit(text, (0, 0))
            text = self.font.render("Screen Size", True, (0, 0, 0))
            self.surface.blit(text, (0, 60))
            text = self.font.render(
                f'{self.game.screen.get_width()}x{self.game.screen.get_height()}', True, (25, 25, 25))
            self.surface.blit(text, (10, 120))

            self.game.screen.blit(self.surface, (self.x, self.y))

    def get_mouse_pos(self):
        'get mouse position relative to self.surface'
        x, y = pygame.mouse.get_pos()
        return x - self.x, y - self.y

    def handle_click(self):
        print('checking click on menu')
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
        self.menu_width = 50
        self.bar_height = self.menu_width / 4
        self.bar_spacing = self.menu_width / 20
        self.menu_height = self.bar_height * 3 + self.bar_spacing * 2
        self.x = self.game.screen.get_width() - self.menu_width - 20
        self.y = 20
        self.color = (100, 100, 100)
        self.menu = Menu(self.game)
        self.rect = pygame.Rect(self.x, self.y, self.menu_width,
                                self.menu_height)
        self.surface = pygame.Surface(
            (self.menu_width, self.menu_height))

    def render(self):
        pygame.draw.rect(self.surface, self.color,
                         (0, 0, self.menu_width, self.bar_height),)
        pygame.draw.rect(self.surface, self.color,
                         (0, self.bar_height + self.bar_spacing, self.menu_width, self.bar_height),)
        pygame.draw.rect(self.surface, self.color,
                         (0, 2 * (self.bar_height + self.bar_spacing), self.menu_width, self.bar_height),)

        self.game.screen.blit(self.surface, (self.x, self.y))

        self.menu.render()

    def handle_click(self):
        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            self.menu.is_menu_open = not self.menu.is_menu_open
        self.menu.handle_click()


class Client:
    def __init__(self):
        hero = HeroFactory().build(size=50, x=100, y=100)
        self.hero = HeroCreate(**hero.dict()).post()

        # self.screen = pygame.display.set_mode((800, 600))
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        pygame.display.set_caption("Learn SQL Model")
        self.clock = pygame.time.Clock()
        self.running = True
        self.screen.fill((0, 0, 0))

        self.moving_up = False
        self.moving_down = False
        self.moving_left = False
        self.moving_right = False
        self.ticks = 0
        self.others = []
        self.hamburger = Hamburger(self)

        atexit.register(self.quit)

    @ property
    def ws(self):
        def connect():
            self._ws = create_connection(
                f"ws://{config.api_client.url.replace('https://', '')}/wsecho"
            )

        if not hasattr(self, "_ws"):
            connect()
        if not self._ws.connected:
            connect()
        return self._ws

    def run(self):
        while self.running:
            console.print("running")
            console.print("handle_events")
            self.handle_events()
            console.print("update")
            self.update()
            console.print("render")
            self.render()
            time = self.clock.tick(60)
            self.ticks += 1
            console.print(f"time: {time}")
            console.print(f"ticks: {self.ticks}")
        self.quit()

    def quit(self):
        try:
            HeroDelete(id=self.hero.id).delete()
        except:
            pass

    def update(self):
        if self.moving_up:
            self.hero.y -= speed
        if self.moving_down:
            self.hero.y += speed
        if self.moving_left:
            self.hero.x -= speed
        if self.moving_right:
            self.hero.x += speed

        if self.hero.x < 0 + self.hero.size:
            self.hero.x = 0 + self.hero.size
        if self.hero.x > self.screen.get_width() - self.hero.size:
            self.hero.x = self.screen.get_width() - self.hero.size
        if self.hero.y < 0 + self.hero.size:
            self.hero.y = 0 + self.hero.size
        if self.hero.y > self.screen.get_height() - self.hero.size:
            self.hero.y = self.screen.get_height() - self.hero.size

        if self.ticks % 5 == 0 or self.ticks == 0:
            console.print("updating")
            update = HeroUpdate(**self.hero.dict(exclude_unset=True))
            console.print(update)
            self.ws.send(update.json())
            console.print("sent")

            raw_heros = self.ws.recv()
            console.print(raw_heros)
            self.others = Heros.parse_raw(raw_heros)

    def render(self):
        self.screen.fill((0, 0, 0))

        for other in self.others.heros:
            if other.id != self.hero.id:
                pygame.draw.circle(
                    self.screen, (255, 0, 0), (other.x, other.y), other.size
                )
                self.screen.blit(
                    my_font.render(other.name, False, (255, 255, 255), 1),
                    (other.x, other.y),
                )

        pygame.draw.circle(
            self.screen, (0, 0, 255), (self.hero.x, self.hero.y), self.hero.size
        )
        self.screen.blit(
            my_font.render(self.hero.name, False, (255, 255, 255)),
            (self.hero.x, self.hero.y),
        )

        # update the screen
        self.hamburger.render()
        pygame.display.flip()

    def handle_events(self):
        self.events = pygame.event.get()
        for event in self.events:
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                if event.key == pygame.K_LEFT:
                    self.moving_left = True
                if event.key == pygame.K_RIGHT:
                    self.moving_right = True
                if event.key == pygame.K_UP:
                    self.moving_up = True
                if event.key == pygame.K_DOWN:
                    self.moving_down = True
                # wasd
                if event.key == pygame.K_w:
                    self.moving_up = True
                if event.key == pygame.K_s:
                    self.moving_down = True
                if event.key == pygame.K_a:
                    self.moving_left = True
                if event.key == pygame.K_d:
                    self.moving_right = True
                # controller left joystick

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self.moving_left = False
                if event.key == pygame.K_RIGHT:
                    self.moving_right = False
                if event.key == pygame.K_UP:
                    self.moving_up = False
                if event.key == pygame.K_DOWN:
                    self.moving_down = False
                # wasd
                if event.key == pygame.K_w:
                    self.moving_up = False
                if event.key == pygame.K_s:
                    self.moving_down = False
                if event.key == pygame.K_a:
                    self.moving_left = False
                if event.key == pygame.K_d:
                    self.moving_right = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    self.hamburger.handle_click()

    def check_events(self):
        pass

    def check_collisions(self):
        pass


game_app = Typer()


@ game_app.command()
def run():
    client = Client()
    client.run()


if __name__ == "__main__":
    game_app()
