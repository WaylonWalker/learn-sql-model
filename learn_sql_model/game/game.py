# using pygame make a game using Hero
# it should be gamepad and mouse compatible
# it should have a server that keeps track of the game logic
# it should have a renderer that renders the game
# it should have a client that sends commands to the server
#


import atexit

import pygame
import typer
from typer import Typer
from websocket import create_connection

from learn_sql_model.config import get_config
from learn_sql_model.models.hero import Hero, HeroCreate, HeroDelete, HeroUpdate, Heros

speed = 10

pygame.font.init()  # you have to call this at the start,
# if you want to use this module.
my_font = pygame.font.SysFont("Comic Sans MS", 30)

config = get_config()


class Client:
    def __init__(self, name, secret_name):
        self.hero = Hero(name=name, secret_name=secret_name, x=400, y=300, size=50)
        self.hero = HeroCreate(**self.hero.dict()).post()
        pygame.init()

        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Learn SQL Model")
        self.clock = pygame.time.Clock()
        self.running = True
        self.screen.fill((0, 0, 0))

        self.moving_up = False
        self.moving_down = False
        self.moving_left = False
        self.moving_right = False
        self.ws = create_connection(
            f"ws://{config.api_client.host}:{config.api_client.port}/wsecho"
        )

        self.ticks = 0

        atexit.register(self.quit)

    @property
    def others(self):
        raw_heros = self.ws.recv()
        return Heros.parse_raw(raw_heros)

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(60)
            self.ticks += 1
        self.quit()

    def quit(self):
        HeroDelete(id=self.hero.id).delete()

    def update(self):
        if self.moving_up:
            self.hero.y -= speed
        if self.moving_down:
            self.hero.y += speed
        if self.moving_left:
            self.hero.x -= speed
        if self.moving_right:
            self.hero.x += speed

        if self.ticks % 60 == 0:
            HeroUpdate(
                **{k: v for k, v in self.hero.dict().items() if v is not None}
            ).update()

    def render(self):
        # Console().print(self.hero)
        self.screen.fill((0, 0, 0))

        for other in self.others.heros:
            pygame.draw.circle(self.screen, (255, 0, 0), (other.x, other.y), other.size)
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


app = Typer()


@app.command()
def run(
    name: str = typer.Option(...),
    secret_name: str = typer.Option(...),
):
    client = Client(name, secret_name)
    client.run()


if __name__ == "__main__":
    app()
