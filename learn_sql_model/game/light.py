from learn_sql_model.console import console
from learn_sql_model.optional import _optional_import_

pygame = _optional_import_("pygame", group="game")

class Light:
    def __init__(self, game):
        self.game = game

    def render(self):
        mx, my = pygame.mouse.get_pos()
        v = pygame.math.Vector2(mx - self.game.player.hero.x, my - self.game.player.hero.y)
        v.scale_to_length(1000)
        
        for r in range(0, 360):
            _v = v.rotate(r)
            pygame.draw.line(
                self.game.screen,
                (255,250,205),
                (self.game.player.hero.x, self.game.player.hero.y),
                (self.game.player.hero.x + _v.x, self.game.player.hero.y + _v.y),
                50
                            )
