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


class Client:
    def __init__(self):
        hero = HeroFactory().build(size=50, x=100, y=100)
        self.hero = HeroCreate(**hero.dict()).post()

        self.screen = pygame.display.set_mode((800, 600))
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

        atexit.register(self.quit)

    @property
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

    def check_events(self):
        pass

    def check_collisions(self):
        pass


game_app = Typer()


@game_app.command()
def run():
    client = Client()
    client.run()


if __name__ == "__main__":
    game_app()
