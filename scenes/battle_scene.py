import suie
import asset_manager
from .game_scene import GameScene

class BattleScene(GameScene):
    def __init__(self):
        GameScene.__init__(self)

        self.background = suie.Image(asset_manager.load_image('wcBattleBackground.png'), (0, 0))

    def cleanup(self):
        pass

    def update(self, event_list, elapsed):
        pass

    def draw(self, screen):
        self.background.draw(screen)
