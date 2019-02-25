import json
import random
import pygame
import suie
import asset_manager
from timer import Timer
import factory
from floating_text import FloatingText
from animated_sprite import Animation, Facing
from vector import Vector
from grid import Grid, CellColor, Cell
from .game_scene import GameScene
from pygame.locals import *


class BattlePhase:
    ORDER = "Order"
    TARGET = "Target"
    EXECUTION = "Execution"
    WAITING = "Waiting"


class BattleScene(GameScene):
    def __init__(self):
        GameScene.__init__(self)

        self.background = suie.Image(asset_manager.load_image('wcBattleBackground.png'), (0, 0))

        self.grid = Grid(Vector(suie.SCREEN_WIDTH // 2 - 144, 100), (6, 6))

        self.left_units = []
        self.right_units = []
        for i in range(3):
            self.left_units.append(factory.generate_avatar('footman', 12 + i))
            self.right_units.append(factory.generate_avatar('footman', 14 + i))

        self._arrange_units()

        self.current_phase = BattlePhase.ORDER
        self.active = "left"
        self.turn_count = 1
        self.avatar_icons = []

        self._setup_panels()
        self._start_turn('left')

        # self.grid.debug_fill()

    def _update_panels(self):
        self.info_label.set_text("ACTIVE: %s | PHASE: %s | TURN #: %s" % (self.active, self.current_phase, self.turn_count))

        for icon in self.avatar_icons:
            self.lineup_panel.remove_child(icon)

        self.avatar_icons.clear()
        active_group = self.left_units if self.active == 'left' else self.right_units
        for i in range(len(active_group)):
            self.avatar_icons.append(suie.AvatarIcon((i * (suie.AvatarIcon.WIDTH + 2), 0), active_group[i]))
            self.lineup_panel.add_child(self.avatar_icons[i])

    def _start_turn(self, who):
        self.active = who
        if who == "left":
            self.turn_count += 1
        self.current_phase = BattlePhase.ORDER

        self._update_panels()

    def _setup_panels(self):
        self.lineup_panel = suie.Panel((5, suie.SCREEN_HEIGHT - 90), (360, 80))

        border = suie.Border((0, 0), (80, 80))
        self.target_panel = suie.Panel((suie.SCREEN_WIDTH - 85, suie.SCREEN_HEIGHT - 85), (80, 80), [border])

        border = suie.Border((0, 0), (320, 80))
        self.action_panel = suie.Panel((375, suie.SCREEN_HEIGHT - 85), (320, 80), [border])

        border = suie.Border((0, 0), (600, 20))
        self.info_label = suie.Label((10, 6),
                           "ACTIVE: %s | PHASE: %s | TURN #: %s" % (self.active, self.current_phase, self.turn_count),
                           font_size=10)
        self.info_panel = suie.Panel((2, 2), (600, 20), [border, self.info_label])

        self.hud_panel = suie.Panel((0, 0), (suie.SCREEN_WIDTH, suie.SCREEN_HEIGHT),
                                    [self.info_panel, self.lineup_panel, self.target_panel, self.action_panel])

    def _lineup_units(self, unit_list, xcoord: int):
        size = len(unit_list)
        if size == 1:
            unit_list[0].set_cell(self.grid[xcoord, 2])
        elif size == 2:
            unit_list[0].set_cell(self.grid[xcoord, 2])
            unit_list[1].set_cell(self.grid[xcoord, 3])
        elif size == 3:
            unit_list[0].set_cell(self.grid[xcoord, 1])
            unit_list[1].set_cell(self.grid[xcoord, 3])
            unit_list[2].set_cell(self.grid[xcoord, 5])
        elif size == 4:
            unit_list[0].set_cell(self.grid[xcoord, 1])
            unit_list[1].set_cell(self.grid[xcoord, 2])
            unit_list[2].set_cell(self.grid[xcoord, 3])
            unit_list[3].set_cell(self.grid[xcoord, 4])
        elif size == 5:
            for i in range(5):
                unit_list[i].set_cell(self.grid[xcoord, i + 1])
        elif size == 6:
            for i in range(6):
                unit_list[i].set_cell(self.grid[xcoord, i])

    def _arrange_units(self):
        for unit in self.left_units:
            unit.sprite.set_facing(Facing.RIGHT)
        for unit in self.right_units:
            unit.sprite.set_facing(Facing.LEFT)

        self._lineup_units(self.left_units, 0)
        self._lineup_units(self.right_units, 5)


    def cleanup(self):
        pass

    def update(self, event_list, elapsed):
        for unit in self.left_units:
            unit.update(elapsed)
        for unit in self.right_units:
            unit.update(elapsed)
        FloatingText.update_all(elapsed)
        self.hud_panel.update(event_list)

        for event in event_list:
            if event.type == MOUSEMOTION:
                for unit in self.left_units + self.right_units:
                    x, y = pygame.mouse.get_pos()
                    if unit.cell.get_rect().collidepoint(x, y):
                        unit.cell.set_fill_color(CellColor.BLUE)
                        unit.cell.set_border_color((150, 150, 255, 255))
                    else:
                        unit.cell.set_fill_color(CellColor.SHADOW)
                        unit.cell.set_border_color(None)

            if event.type == MOUSEBUTTONDOWN:
                for unit in self.left_units + self.right_units:
                    x, y = pygame.mouse.get_pos()
                    if unit.cell.get_rect().collidepoint(x, y):


            if event.type == KEYDOWN:
        #         if event.key == K_a:
        #             print(self.avatar_icons[0]._get_final_position())
        #         elif event.key == K_b:
        #             self.bar.set_fill(self.bar.get_fill() + 0.1)
        #         elif event.key == K_c:
        #             self.footman.move((200, 200))
        #         elif event.key == K_d:
        #             self.footman.move((100, 200))
        #         elif event.key == K_e:
        #             self.footman.sprite.start_animation(Animation.DEATH)
                if event.key == K_f:
                    self.left_units[0].alter_life(random.randrange(-23, -4))
        #         elif event.key == K_g:
        #             self.enemy.sprite.set_facing(Facing.RIGHT)
        #         elif event.key == K_h:
        #             self.enemy.sprite.set_facing(Facing.LEFT)


    def draw(self, screen):
        self.background.draw(screen)
        self.grid.draw(screen)

        for unit in self.left_units:
            unit.draw(screen)
        for unit in self.right_units:
            unit.draw(screen)

        FloatingText.draw_all(screen)
        self.hud_panel.draw(screen)
