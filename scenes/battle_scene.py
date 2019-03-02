import json
import random
import pygame
import suie
import asset_manager
from timer import Timer
import factory
from battle_executor import BattleExecutor
from floating_text import FloatingText
from animated_sprite import Animation, Facing
from vector import Vector
from grid import Grid, CellColor, Cell
from sfx import SFX
from .game_scene import GameScene
from pygame.locals import *


class BattlePhase:
    ORDER = "Order"
    TARGET = "Target"
    EXECUTION = "Execution"
    WAITING = "Waiting"

class BattleAction:
    ATTACK = "Attack"
    DEFEND = "Defend"
    NEXT_UNIT = "Next Unit"
    SKIP = "Skip"
    CANCEL = "Cancel"

ARROW_OFFSET = (4, -50)


class BattleScene(GameScene):
    def __init__(self):
        GameScene.__init__(self)

        self.background = suie.Image(asset_manager.load_image('wcBattleBackground.png'), (0, 0))
        self.selection_arrow = SFX('assets/ui/rotatingArrow.png', (7, 2), (40, 40), (0, 0), 0, 13, True, frame_speed=80)
        self.action_sfx = None

        self.grid = Grid(Vector(suie.SCREEN_WIDTH // 2 - 144, 100), (6, 6))

        self.left_units = []
        self.right_units = []
        for i in range(3):
            self.left_units.append(factory.generate_avatar('footman', 12 + i))
            self.right_units.append(factory.generate_avatar('footman', 14 + i))

        self.executor = BattleExecutor(self.left_units, self.right_units, self.grid)

        self._arrange_units()

        self.current_phase = BattlePhase.ORDER
        self.active = "left"
        self.turn_count = 0

        """ Save unit orders in this dict. Ex/
        Avatar: { order: BattleAction.ATTACK, target: Avatar2 },
        Avatar2: { order: BattleAction.DEFEND, target: Avatar3 },  etc...
        """
        self.unit_orders = {}

        self.avatar_icons = []
        self.action_icons = []

        self.selected_avatar = None
        self.hovered_avatar = None
        self.selected_action = None

        self._setup_panels()
        self._start_turn('left')

        # self.grid.debug_fill()

    def _avatar_has_order(self, avatar):
        return avatar in self.unit_orders

    def _start_turn(self, who):
        self.active = who
        if who == "left":
            self.turn_count += 1

        self.current_phase = BattlePhase.ORDER
        self.selected_avatar = None
        self.selected_action = None

        for unit in self.left_units + self.right_units:
            unit.cell.set_fill_color(CellColor.SHADOW)
            unit.cell.set_border_color(None)

        self._update_panels()

    def _end_turn(self):
        if self.active == 'left':
            self._start_turn('right')
        else:
            self.current_phase = BattlePhase.EXECUTION
            self.executor.execute(self.unit_orders)

            self.unit_orders = {}

            # Check for battle finish here
            self._start_turn('left')

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

    def _select_action(self, action):
        active_units = self.left_units if self.active == "left" else self.right_units

        if self.current_phase == BattlePhase.ORDER:
            if action == BattleAction.ATTACK:
                self.current_phase = BattlePhase.TARGET
                FloatingText.create_new(FloatingText("attack", self.selected_avatar.sprite.get_center(), [255] * 4))
                self.selected_action = BattleAction.ATTACK
                self._update_panels()
            elif action == BattleAction.DEFEND:
                self.current_phase = BattlePhase.TARGET
                FloatingText.create_new(FloatingText("defend", self.selected_avatar.sprite.get_center(), [255] * 4))
                self.selected_action = BattleAction.DEFEND
                self._update_panels()
            elif action == BattleAction.NEXT_UNIT:
                empty_unit = False
                for unit in active_units:
                    if not unit in self.unit_orders:
                        empty_unit = True
                if not empty_unit:
                    self._end_turn()
                    return

                index = active_units.index(self.selected_avatar)
                index += 1 if index < (len(active_units) - 1) else -index
                self._select_avatar(active_units[index])
            elif action == BattleAction.SKIP:
                self.unit_orders[self.selected_avatar] = { "order": BattleAction.SKIP }
                self._select_action(BattleAction.NEXT_UNIT)

        elif self.current_phase == BattlePhase.TARGET:
            if action == BattleAction.CANCEL:
                self.current_phase = BattlePhase.ORDER
                self._update_panels()

    def _hover_avatar(self, avatar, flag: bool):
        if flag and not self.hovered_avatar:
            self.hovered_avatar = avatar

            if avatar == self.selected_avatar:
                return

            active_units = self.left_units if self.active == "left" else self.right_units

            if self.current_phase == BattlePhase.ORDER:
                color = CellColor.BLUE if avatar in active_units else CellColor.RED
                bcolor = CellColor.BLUE_HIGHLIGHT if avatar in active_units else CellColor.SHADOW_HIGHLIGHT
            elif self.current_phase == BattlePhase.TARGET:
                color = CellColor.GREEN if avatar in active_units else CellColor.RED
                bcolor = CellColor.GREEN_HIGHLIGHT if avatar in active_units else CellColor.RED_HIGHLIGHT
            elif self.current_phase in [BattlePhase.WAITING, BattlePhase.EXECUTION]:
                color, bcolor = CellColor.SHADOW, CellColor.SHADOW_HIGHLIGHT

            avatar.cell.set_fill_color(color)
            avatar.cell.set_border_color(bcolor)
        elif not flag:
            self.hovered_avatar = None

            if avatar == self.selected_avatar:
                return

            avatar.cell.set_fill_color(CellColor.SHADOW)
            avatar.cell.set_border_color(None)

    def _clear_selection(self):
        if self.selected_avatar:
            self.selected_avatar.cell.set_fill_color(CellColor.SHADOW)
            self.selected_avatar.cell.set_border_color(None)

        self.selected_avatar = None
        self._update_panels()

    def _select_avatar(self, avatar):
        active_units = self.left_units if self.active == "left" else self.right_units

        if self.current_phase == BattlePhase.ORDER:
            if avatar in active_units:
                self._clear_selection()

                self.selected_avatar = avatar
                avatar.cell.set_fill_color(CellColor.ORANGE)
                avatar.cell.set_border_color(CellColor.ORANGE_HIGHLIGHT)
                self.selection_arrow.position = (avatar.sprite.get_center() + ARROW_OFFSET)
                self._update_panels()

        elif self.current_phase == BattlePhase.TARGET and self.selected_action == BattleAction.ATTACK:
            if not avatar in active_units:
                self.unit_orders[self.selected_avatar] = { "order": BattleAction.ATTACK, "target": avatar }
                x, y = avatar.sprite.get_center()
                self.action_sfx = SFX('assets/sfx/retaliate.png', (16, 1), (64, 64), (x - 10, y - 50), 0, 15, frame_speed=80)
                self.current_phase = BattlePhase.ORDER
                self._select_action(BattleAction.NEXT_UNIT)
        elif self.current_phase == BattlePhase.TARGET and self.selected_action == BattleAction.DEFEND:
            if avatar in active_units:
                self.unit_orders[self.selected_avatar] = {"order": BattleAction.DEFEND, "target": avatar}
                x, y = avatar.sprite.get_center()
                self.action_sfx = SFX('assets/sfx/shield.png', (10, 1), (64, 64), (x - 10, y - 50), 0, 9, frame_speed=80)
                self.current_phase = BattlePhase.ORDER
                self._select_action(BattleAction.NEXT_UNIT)

    def _handle_events(self, event_list):
        for event in event_list:
            if event.type == KEYDOWN:
                if event.key == K_BACKSPACE:
                    if self.current_phase == BattlePhase.ORDER:
                        self._clear_selection()
                    elif self.current_phase == BattlePhase.TARGET:
                        self._select_action(BattleAction.CANCEL)

            elif event.type == MOUSEMOTION:
                x, y = pygame.mouse.get_pos()
                if self.hovered_avatar and not self.hovered_avatar.cell.get_rect().collidepoint(x, y):
                    self._hover_avatar(self.hovered_avatar, False)
                for unit in self.left_units + self.right_units:
                    if unit.cell.get_rect().collidepoint(x, y):
                        self._hover_avatar(unit, True)

            elif event.type == MOUSEBUTTONDOWN:
                for unit in self.left_units + self.right_units:
                    x, y = pygame.mouse.get_pos()
                    if unit.cell.get_rect().collidepoint(x, y):
                        self._select_avatar(unit)

    def update(self, event_list, elapsed):
        for unit in self.left_units:
            unit.update(elapsed)
        for unit in self.right_units:
            unit.update(elapsed)

        FloatingText.update_all(elapsed)
        self.hud_panel.update(event_list)

        self._handle_events(event_list)

    def draw(self, screen):
        self.background.draw(screen)
        self.grid.draw(screen)

        for unit in self.left_units:
            unit.draw(screen)
        for unit in self.right_units:
            unit.draw(screen)

        if self.selected_avatar:
            self.selection_arrow.draw(screen)
        if self.action_sfx:
            self.action_sfx.draw(screen)

        FloatingText.draw_all(screen)
        self.hud_panel.draw(screen)

    def cleanup(self):
        pass

    # --- HUD FUNCTIONALITY ---
    def _letter_from_order(self, order):
        if order == BattleAction.SKIP:
            return "S"
        elif order == BattleAction.DEFEND:
            return "D"
        elif order == BattleAction.ATTACK:
            return "A"

    def _update_panels(self):
        active_group = self.left_units if self.active == 'left' else self.right_units

        self.info_label.set_text("ACTIVE: %s | PHASE: %s | TURN #: %s" % (self.active, self.current_phase, self.turn_count))

        for icon in self.avatar_icons:
            self.lineup_panel.remove_child(icon)
        self.avatar_icons.clear()

        if self.current_phase == BattlePhase.ORDER:
            for i in range(len(active_group)):
                icon = suie.AvatarIcon((i * (suie.AvatarIcon.WIDTH + 2), 0), active_group[i])
                if active_group[i] == self.selected_avatar:
                    icon.highlight(True)
                if active_group[i] in self.unit_orders:
                    icon.set_action(self._letter_from_order(self.unit_orders[active_group[i]]["order"]))
                self.avatar_icons.append(icon)
                self.lineup_panel.add_child(icon)

        for icon in self.action_icons:
            self.action_panel.remove_child(icon)
        self.action_icons.clear()

        if self.current_phase == BattlePhase.ORDER and self.selected_avatar:
            self.action_icons.append(suie.ActionIcon((0, 0),
                                                     lambda: self._select_action(BattleAction.ATTACK),
                                                     "a", 116))
            self.action_icons.append(suie.ActionIcon((suie.ActionIcon.WIDTH + 2, 0),
                                                     lambda: self._select_action(BattleAction.DEFEND),
                                                     "d", 164))
            self.action_icons.append(suie.ActionIcon(((suie.ActionIcon.WIDTH + 2) * 2, 0),
                                                     lambda: self._select_action(BattleAction.NEXT_UNIT),
                                                     "n", 170))
            self.action_icons.append(suie.ActionIcon(((suie.ActionIcon.WIDTH + 2) * 3, 0),
                                                     lambda: self._select_action(BattleAction.SKIP),
                                                     "s", 91))

        elif self.current_phase == BattlePhase.TARGET and self.selected_avatar:
            self.action_icons.append(suie.ActionIcon((0, 0), lambda: self._select_action(BattleAction.CANCEL), "c", 91))

        for icon in self.action_icons:
            self.action_panel.add_child(icon)

    def _setup_panels(self):
        self.lineup_panel = suie.Panel((5, suie.SCREEN_HEIGHT - 90), (360, 80))

        border = suie.Border((0, 0), (80, 80))
        self.target_panel = suie.Panel((suie.SCREEN_WIDTH - 85, suie.SCREEN_HEIGHT - 85), (80, 80), [border])

        self.action_panel = suie.Panel((375, suie.SCREEN_HEIGHT - 85), (320, 80))

        border = suie.Border((0, 0), (600, 20))
        self.info_label = suie.Label((10, 6),
                           "ACTIVE: %s | PHASE: %s | TURN #: %s" % (self.active, self.current_phase, self.turn_count),
                           font_size=10)
        self.info_panel = suie.Panel((2, 2), (600, 20), [border, self.info_label])

        self.hud_panel = suie.Panel((0, 0), (suie.SCREEN_WIDTH, suie.SCREEN_HEIGHT),
                                    [self.info_panel, self.lineup_panel, self.target_panel, self.action_panel])
