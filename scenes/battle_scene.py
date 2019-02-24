import json
import suie
import asset_manager
from animated_sprite import AnimatedSprite, Animation
from .game_scene import GameScene
from pygame.locals import *

class BattleScene(GameScene):
    def __init__(self):
        GameScene.__init__(self)

        self.background = suie.Image(asset_manager.load_image('wcBattleBackground.png'), (0, 0))

        with open('pdata/wcAnimations.json', 'r') as file:
            sheet_data = json.load(file)
            self.footman = AnimatedSprite('assets/unit/soldier.png', **sheet_data['footman'])
            self.footman.set_position((100, 100))

        print(self.footman.attack_hit_timeout, self.footman.get_position(), self.footman._static_index)

    def cleanup(self):
        pass

    def update(self, event_list, elapsed):
        self.footman.update(elapsed)

        for event in event_list:
            if event.type == KEYDOWN:
                if event.key == K_a:
                    self.footman.set_static_index(self.footman._static_index + 1)
                elif event.key == K_b:
                    self.footman.start_animation(Animation.ATTACK, False)
                elif event.key == K_c:
                    self.footman.move((200, 200))
                elif event.key == K_d:
                    self.footman.move((100, 200))
                elif event.key == K_e:
                    self.footman.start_animation(Animation.DEATH)


    def draw(self, screen):
        self.background.draw(screen)
        self.footman.draw(screen)
