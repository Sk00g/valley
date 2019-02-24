import json
import random
import suie
import asset_manager
from floating_text import FloatingText
from animated_sprite import AnimatedSprite, Animation, Facing
from avatar import Avatar
from vector import Vector
from grid import Grid, CellColor, Cell
from .game_scene import GameScene
from pygame.locals import *

class BattleScene(GameScene):
    def __init__(self):
        GameScene.__init__(self)

        self.background = suie.Image(asset_manager.load_image('wcBattleBackground.png'), (0, 0))

        self.grid = Grid(Vector(100, 100), (10, 6))

        with open('pdata/wcAnimations.json', 'r') as file:
            sheet_data = json.load(file)
            self.footman_sprite = AnimatedSprite('assets/unit/soldier.png', **sheet_data['footman'])
            self.enemy_sprite = AnimatedSprite('assets/unit/soldier.png', **sheet_data['footman'])

        with open('pdata/wcUnits.json', 'r') as file:
            unit_data = json.load(file)
            self.footman = Avatar(self.footman_sprite, self.grid[1, 1], 12, **unit_data['footknight'])
            self.footman.sprite.set_facing(Facing.RIGHT)
            self.enemy = Avatar(self.enemy_sprite, self.grid[2, 1], 16, **unit_data['footknight'])

        print("Footman position:", self.footman.sprite.get_position())
        print("Footman cell position:", self.footman.cell.get_position())
        self.grid.debug_fill()

    def cleanup(self):
        pass

    def update(self, event_list, elapsed):
        self.footman.update(elapsed)
        self.enemy.update(elapsed)
        FloatingText.update_all(elapsed)

        for event in event_list:
            if event.type == KEYDOWN:
                if event.key == K_a:
                    self.footman.attack_unit(self.enemy)
                elif event.key == K_b:
                    self.enemy.attack_unit(self.footman)
                elif event.key == K_c:
                    self.footman.move((200, 200))
                elif event.key == K_d:
                    self.footman.move((100, 200))
                elif event.key == K_e:
                    self.footman.sprite.start_animation(Animation.DEATH)
                elif event.key == K_f:
                    self.footman.alter_life(random.randrange(-23, -4))
                elif event.key == K_g:
                    self.enemy.sprite.set_facing(Facing.RIGHT)
                elif event.key == K_h:
                    self.enemy.sprite.set_facing(Facing.LEFT)


    def draw(self, screen):
        self.background.draw(screen)
        self.grid.draw(screen)
        self.footman.draw(screen)
        self.enemy.draw(screen)
        FloatingText.draw_all(screen)
