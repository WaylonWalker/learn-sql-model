from learn_sql_model.console import console
from learn_sql_model.models.hero import HeroCreate, HeroDelete, HeroUpdate, Heros
from learn_sql_model.optional import _optional_import_

pygame = _optional_import_("pygame", group="game")
HeroFactory = _optional_import_(
    "learn_sql_model.factories.hero",
    "HeroFactory",
    group="game",
)


class Player:
    def __init__(self, game):
        hero = HeroFactory().build(size=25, x=100, y=100)
        self.hero = HeroCreate(**hero.dict()).post()

        self.game = game
        self.others = [] #Heros(heros=[])
        self.width = 16
        self.height = 16
        self.white = (255, 255, 255)
        self.x = self.game.screen.get_width() / 2
        self.y = self.game.screen.get_height() / 2
        self.speed = 5
        self.max_speed = 5
        self.image = pygame.image.load("player.png").convert_alpha()
        self.x_last = self.x
        self.y_last = self.y
        self.hitbox_surface = pygame.Surface((self.width, self.height))
        self.hitbox_surface.fill(self.white)
        pygame.draw.rect(
            self.hitbox_surface, (255, 0, 0), (0, 0, self.width, self.height), 1
        )
        self.hitbox_surface.set_alpha(0)
        self.moving_up = False
        self.moving_down = False
        self.moving_left = False
        self.moving_right = False
        self.joysticks = {}

    def rename_hero(self):
        old_hero = self.hero
        hero = HeroFactory().build(
            size=self.hero.size, x=self.hero.x, y=self.hero.y, id=old_hero.id
        )
        self.hero = HeroCreate(**hero.dict()).post()

    def quit(self):
        try:
            HeroDelete(id=self.hero.id).delete()
        except RuntimeError:
            pass

    def handle_events(self):
        # Update the self
        for event in self.game.events:
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                if event.key == pygame.K_LEFT:
                    self.speed = self.max_speed
                    self.moving_left = True
                if event.key == pygame.K_RIGHT:
                    self.speed = self.max_speed
                    self.moving_right = True
                if event.key == pygame.K_UP:
                    self.speed = self.max_speed
                    self.moving_up = True
                if event.key == pygame.K_DOWN:
                    self.speed = self.max_speed
                    self.moving_down = True
                # wasd
                if event.key == pygame.K_w:
                    self.speed = self.max_speed
                    self.moving_up = True
                if event.key == pygame.K_s:
                    self.speed = self.max_speed
                    self.moving_down = True
                if event.key == pygame.K_a:
                    self.speed = self.max_speed
                    self.moving_left = True
                if event.key == pygame.K_d:
                    self.speed = self.max_speed
                    self.moving_right = True

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

        for joystick in self.joysticks.values():
            if abs(joystick.get_axis(0)) > 0.2:
                self.x += joystick.get_axis(0) * 10 * self.speed * self.elapsed
            if abs(joystick.get_axis(1)) > 0.2:
                self.y += joystick.get_axis(1) * 10 * self.speed * self.elapsed

            if abs(joystick.get_axis(3)) > 0.2 and abs(joystick.get_axis(4)) > 0.2:
                pygame.mouse.set_pos(
                    (
                        pygame.mouse.get_pos()[0] + joystick.get_axis(3) * 32,
                        pygame.mouse.get_pos()[1] + joystick.get_axis(4) * 32,
                    )
                )
            elif abs(joystick.get_axis(3)) > 0.2:
                pygame.mouse.set_pos(
                    (
                        pygame.mouse.get_pos()[0] + joystick.get_axis(3) * 32,
                        pygame.mouse.get_pos()[1],
                    )
                )
            elif abs(joystick.get_axis(4)) > 0.2:
                pygame.mouse.set_pos(
                    (
                        pygame.mouse.get_pos()[0],
                        pygame.mouse.get_pos()[1] + joystick.get_axis(4) * 32,
                    )
                )
        if self.moving_left:
            self.hero.x -= self.speed
        if self.moving_right:
            self.hero.x += self.speed
        if self.moving_up:
            self.hero.y -= self.speed
        if self.moving_down:
            self.hero.y += self.speed
        # Check for self collisions with the walls and the black tiles on the map
        if self.hero.x < 0:
            self.hero.x = 0
        if self.hero.x > self.game.screen.get_width() - self.width:
            self.hero.x = self.game.screen.get_width() - self.width
        if self.hero.y < 0:
            self.hero.y = 0
        if self.hero.y > self.game.screen.get_height() - self.height:
            self.hero.y = self.game.screen.get_height() - self.height

        self.pos = pygame.math.Vector2(self.hero.x, self.hero.y)

        if self.game.map.point_check_collision(self.pos.x, self.pos.y):
            start_pos = pygame.math.Vector2(self.x_last, self.y_last)
            end_pos = pygame.math.Vector2(self.hero.x, self.hero.y)
            movement_vector = end_pos - start_pos
            try:
                movement_direction = movement_vector.normalize()
            except ZeroDivisionError:
                end_pos = pygame.math.Vector2(self.hero.x + 128, self.hero.y + 128)
                movement_vector = end_pos - start_pos
                movement_direction = movement_vector.normalize()
            movement_speed = 0.05

            self.hero.x = self.x_last
            self.hero.y = self.y_last

            self.pos = pygame.math.Vector2(start_pos)

            while self.game.map.point_check_collision(self.pos.x, self.pos.y):
                self.pos += movement_speed * movement_direction
                self.hero.x = self.pos.x
                self.hero.y = self.pos.y

            self.pos -= movement_speed * movement_direction
            self.hero.x = self.pos.x
            self.hero.y = self.pos.y

        self.x_last = self.hero.x
        self.y_last = self.hero.y

        if self.game.ticks % 5 == 0 or self.game.ticks == 0:
            console.print("updating")
            update = HeroUpdate(**self.hero.dict(exclude_unset=True))
            console.print(update)
            self.game.ws.send(update.json())
            console.print("sent")

            raw_heros = self.game.ws.recv()
            console.print(raw_heros)
            self.others = Heros.parse_raw(raw_heros)

    def draw(self):
        self.move()
        self.game.screen.blit(
            pygame.transform.scale(self.image, (16, 16)),
            (self.x - 8 - self.game.map.offset.x, self.y - 8 - self.game.map.offset.y),
        )

    def render(self):
        for other in self.others.heros:
            if other.id != self.hero.id:
                pygame.draw.circle(
                    self.game.screen, (255, 0, 0), (other.x, other.y), other.size
                )
                self.game.screen.blit(
                    self.game.font.render(other.name, False, (255, 255, 255), 1),
                    (other.x, other.y),
                )

        pygame.draw.circle(
            self.game.screen, (0, 0, 255), (self.hero.x, self.hero.y), self.hero.size
        )
        self.game.screen.blit(
            self.game.font.render(self.hero.name, False, (255, 255, 255), 1),
            (self.hero.x, self.hero.y),
        )
