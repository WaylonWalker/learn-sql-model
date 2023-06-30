from learn_sql_model.optional import _optional_import_

pygame = _optional_import_("pygame", group="game")


class Light:
    def __init__(self, game):
        self.game = game
        self.surf = pygame.Surface(
            (self.game.screen.get_width(), self.game.screen.get_height())
        )
        # pil_image = Image.new("RGBA", (1000, 500))
        # pil_draw = ImageDraw.Draw(pil_image)
        # pil_draw.pieslice((-1500, -100, 1000, 600), 340, 20, fill=(255, 250, 205))
        # pil_image = pil_image.filter(ImageFilter.GaussianBlur(radius=5))

        # mode = pil_image.mode
        # size = pil_image.size
        # data = pil_image.tobytes()

        # self.image = pygame.image.fromstring(data, size, mode)

        # for r in range(-25, 25):
        #     _v = v.rotate(r)
        #     pygame.draw.line(
        #         self.game.screen,
        #         (255, 250, 205),
        #         (0, 50),
        #         (0 + _v.x, self.game.player.hero.y + _v.y),
        #         50,
        #     )

    def render(self):
        self.surf.fill((0, 0, 0))
        mx, my = pygame.mouse.get_pos()
        v = pygame.math.Vector2(
            mx - self.game.player.hero.x, my - self.game.player.hero.y
        )
        v.scale_to_length(self.game.player.hero.flashlight_strength)
        self.game.player.hero.flashlight_angle = v.angle_to(pygame.math.Vector2(0, 1))
        # self.game.screen.blit(
        #     pygame.transform.rotate(self.image, pygame.math.Vector2(0, 0).angle_to(v)),
        #     (self.game.player.hero.x, self.game.player.hero.y - 250),
        # )

        for r in range(-25, 25):
            _v = v.rotate(r)
            pygame.draw.line(
                self.surf,
                (255, 250, 205),
                (self.game.player.hero.x, self.game.player.hero.y),
                (self.game.player.hero.x + _v.x, self.game.player.hero.y + _v.y),
                50,
            )

        for other in self.game.player.others.__root__:
            v = pygame.math.Vector2(0, 1)
            v = v.rotate(-other.flashlight_angle)
            v.scale_to_length(other.flashlight_strength)
            for r in range(-25, 25):
                _v = v.rotate(r)
                pygame.draw.line(
                    self.surf,
                    (255, 250, 205),
                    (other.x, other.y),
                    (other.x + _v.x, other.y + _v.y),
                    50,
                )

        # draw a circle
        pygame.draw.circle(
            self.surf,
            (255, 250, 205),
            (self.game.player.hero.x, self.game.player.hero.y),
            self.game.player.hero.lanturn_strength,
        )

        for other in self.game.player.others.__root__:
            pygame.draw.circle(
                self.surf,
                (255, 250, 205),
                (other.x, other.y),
                other.lanturn_strength,
            )

        self.game.darkness.blit(
            pygame.transform.scale(self.surf, self.game.screen.get_size()).convert(),
            (0, 0),
        )


def render_flashlight(light, strength, angle):

    # self.darkness.blit(
    #     pygame.transform.smoothscale(
    #         self.spot, [self.light_power, self.light_power]
    #     ),
    #     (self.x - self.light_power / 2, self.y - self.light_power / 2),
    # )
    for r in range(-25, 25):
        _v = v.rotate(r)
        pygame.draw.line(
            light,
            (255, 250, 205),
            (self.game.player.hero.x, self.game.player.hero.y),
            (self.game.player.hero.x + _v.x, self.game.player.hero.y + _v.y),
            50,
        )
