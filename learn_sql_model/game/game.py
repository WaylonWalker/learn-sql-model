import atexit

from typer import Typer
from websocket import create_connection

from learn_sql_model.config import get_config
from learn_sql_model.console import console
from learn_sql_model.game.light import Light
from learn_sql_model.game.map import Map
from learn_sql_model.game.menu import Menu
from learn_sql_model.game.player import Player
from learn_sql_model.optional import _optional_import_

pygame = _optional_import_("pygame", group="game")

speed = 10

config = get_config()


class Client:
    def __init__(self):
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
        self.player = Player(self)
        self.menu = Menu(self)
        self.map = Map(self)
        self.light = Light(self)
        self.font = pygame.font.SysFont("", 50)
        self.joysticks = {}
        self.darkness = pygame.Surface(
            (self.screen.get_width(), self.screen.get_height())
        )

        atexit.register(self.quit)

    @property
    def ws(self):
        def connect():
            if "https" in config.api_client.url:
                url = f"wss://{config.api_client.url.replace('https://', '')}/wsecho"
            elif "http" in config.api_client.url:
                url = f"ws://{config.api_client.url.replace('http://', '')}/wsecho"
            else:
                url = f"ws://{config.api_client.url}/wsecho"
            self._ws = create_connection(url)

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
            self.elapsed = time / 100
            self.ticks += 1
            console.print(f"time: {time}")
            console.print(f"ticks: {self.ticks}")
        self.quit()

    def quit(self):
        self.running = False
        self.player.quit()

    def update(self):
        ...

    def render(self):
        self.screen.fill((0, 0, 0))
        self.map.render()
        self.player.render()
        light_level = 0
        self.darkness.fill((light_level, light_level, light_level))
        self.light.render()
        self.screen.blit(
            pygame.transform.scale(self.darkness, self.screen.get_size()).convert(),
            (0, 0),
            special_flags=pygame.BLEND_MULT,
        )

        # update the screen
        self.menu.render()
        pygame.display.flip()

    def handle_events(self):
        self.events = pygame.event.get()
        self.menu.handle_events(self.events)
        self.player.handle_events()
        for event in self.events:
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.JOYDEVICEADDED:
                # This event will be generated when the program starts for every
                # joystick, filling up the list without needing to create them manually.
                joy = pygame.joystick.Joystick(event.device_index)
                self.joysticks[joy.get_instance_id()] = joy
            if event.type == pygame.JOYDEVICEREMOVED:
                del self.joysticks[event.instance_id]

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
