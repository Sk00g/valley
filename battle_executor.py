"""
loop defenders that haven't retaliated. Start with fastest

Acquire target based on nearest grid enemy (will likely be defender if any)

Apply above attack sequence. Damage is 50%. Defend bonus still applies (25% if defender attack defender). Don't cut retaliate damage with defender bonus. So retaliate should deal 50% damage, not 25%

Move back to origin

END LOOP

All units move back to lineup

Wait 1 second

Return to call scene
"""

import suie
from timer import Timer
from floating_text import FloatingText
from enums import BattleAction
from animated_sprite import Facing


SCENE_SIZE = 450, 400
# This % damage reduced when unit is Guarding
GUARD_BONUS = 0.25
# This multiplied by distance equals move duration in ms
DISTANCE_MS_FACTOR = 9.3
# Damage dealt by defending unit that is attacking
DEFEND_ATTACK_FACTOR = 0.5


class BattleExecutor:
    def __init__(self, left_units, right_units, grid):
        self.all_units = left_units + right_units
        self.left_units = left_units
        self.right_units = right_units
        self.grid = grid

        self.shadow_panel = suie.Panel((0, 0), (suie.SCREEN_WIDTH, suie.SCREEN_HEIGHT))
        self._generate_shadows()

        self.end_action = None
        self.count = 0
        self.orders = {}

        # Keep track of original cells to return to
        self.original_cells = {}

        # Unordered list of defenders
        self.defenders = []

        # Store list of attackers by speed
        self.attackers = []

        # Unordered list of units who are defended
        self.defendees = []

        # Ordered list of units who are selfish
        self.guarders = []

        # Unordered list of units who have been attacked
        self.attacked = []

        # Dict of defender's defensive cells
        self.defensive_cells = {}

        # List of defenders that weren't attacked and so will do a 50% attack
        self.attacking_defenders = []

    def _generate_shadows(self):
        size = (suie.SCREEN_WIDTH - SCENE_SIZE[0]) // 2, (suie.SCREEN_HEIGHT - SCENE_SIZE[1]) // 2 + 2
        self.shadow_panel.add_child(suie.Rectangle((0, 0), (suie.SCREEN_WIDTH, size[1]), (0, 0, 0, 180)))
        self.shadow_panel.add_child(suie.Rectangle((0, size[1] - 2), (size[0], suie.SCREEN_HEIGHT - size[1] + 2), (0, 0, 0, 180)))
        self.shadow_panel.add_child(suie.Rectangle((size[0] - 2, suie.SCREEN_HEIGHT - size[1]), (suie.SCREEN_WIDTH, size[1]), (0, 0, 0, 180)))
        self.shadow_panel.add_child(suie.Rectangle((suie.SCREEN_WIDTH - size[0], size[1] - 2), (size[0], SCENE_SIZE[1]), (0, 0, 0, 180)))

    def _generate_info(self):
        for avatar in self.orders:
            self.original_cells[avatar] = avatar.cell

            target = self.orders[avatar]['target']
            order = self.orders[avatar]['order']

            if order == BattleAction.DEFEND:
                self.defenders.append(avatar)
                self.defendees.append(target)

            elif order == BattleAction.ATTACK:
                self.attackers.append(avatar)

            elif order == BattleAction.GUARD:
                self.guarders.append(avatar)

        self.attackers.sort(key=lambda mem: mem.speed, reverse=True)
        self.guarders.sort(key=lambda mem: mem.speed, reverse=True)

        # print('Attackers:', len(self.attackers))
        # print('Defenders:', len(self.defenders))
        # print('Defendees:', len(self.defendees))
        # print('Guarders:', len(self.guarders))

    def either_team_is_dead(self):
        return len([unit for unit in self.left_units if unit.is_alive()]) < 1 or\
               len([unit for unit in self.right_units if unit.is_alive()]) < 1

    def get_defender_of(self, avatar):
        for unit in self.defenders:
            if self.orders[unit]['target'] == avatar:
                return unit

    def get_nearest_enemy(self, avatar):
        enemies = self.left_units if avatar in self.right_units else self.right_units
        nearest = None
        nearest_path = 100
        for unit in enemies:
            if unit.is_alive():
                dist = self.grid.get_grid_distance(avatar.cell, unit.cell)
                if dist < nearest_path:
                    nearest_path = dist
                    nearest = unit

        return nearest

    def execute(self, unit_orders, end_action, turn_count):
        self.end_action = end_action
        self.grid.reset_cell_colors()
        self.orders = unit_orders

        FloatingText.create_new(FloatingText("ROUND %d" % turn_count,
                                             (suie.SCREEN_WIDTH // 2 - 80, 150),
                                             (255, 255, 255), font_size=20))

        self._generate_info()

        Timer.create_new(Timer(2000, self.stage1))

    # Move defenders and attackers to appropriate position
    def stage1(self):
        for attacker in self.attackers:
            cellx, celly = attacker.cell.coords
            sign = 1 if attacker in self.left_units else -1
            attacker.move(self.grid[cellx + 1 * sign, celly])

        for defender in self.defenders:
            defended = self.orders[defender]['target']
            cellx, celly = defended.cell.coords
            sign = 1 if defender in self.left_units else -1
            defender.move(self.grid[cellx + 1 * sign, celly])

        if not self.attackers and not self.defenders:
            self.final_stage()
            return

        if len(self.defenders) > 0:
            Timer.create_new(Timer(2000, self.next_attack))
        else:
            self.next_attack()

    def next_attack(self):
        if self.either_team_is_dead():
            self.stage3()
            return

        if self.count > 0:
            old_attacker = self.attackers[self.count - 1]
            facing = Facing.RIGHT if old_attacker in self.left_units else Facing.LEFT
            old_attacker.sprite.set_facing(facing)

        self.count += 1

        if self.count > len(self.attackers):
            self.stage2()
            return

        attacker = self.attackers[self.count - 1]
        target = self.orders[attacker]['target']
        tarx, tary = target.cell.coords
        sign = 1 if attacker in self.right_units else -1

        if not target.is_alive():
            tarx, tary = self.get_nearest_enemy(attacker).cell.coords
        elif target in self.defendees and self.get_defender_of(target).is_alive():
            tarx += 1 * sign

        tcell = self.grid[tarx + 1 * sign, tary]
        dist = self.grid.get_pixel_distance(attacker.cell, tcell)
        attacker.move(tcell)
        Timer.create_new(Timer(int(dist * DISTANCE_MS_FACTOR), self.do_attack1))

    def do_attack1(self):
        attacker = self.attackers[self.count - 1]
        sign = 1 if attacker in self.left_units else -1
        cellx, celly = attacker.cell.coords
        target = self.grid[cellx + 1 * sign, celly].occupant

        damage_factor = 1.0
        if target in self.guarders:
            damage_factor -= GUARD_BONUS
        attacker.attack_unit(target, damage_factor)
        self.attacked.append(target)

        if target in self.defenders:
            Timer.create_new(Timer(750, lambda: self.retaliate(target, attacker)))
        else:
            Timer.create_new(Timer(1000, self.finish_attack))

    def retaliate(self, retaliator, target):
        if retaliator.is_alive() and target.is_alive():
            retaliator.attack_unit(target, 0.5)
            self.attacked.append(target)

        Timer.create_new(Timer(750, self.finish_attack))

    def finish_attack(self):
        attacker = self.attackers[self.count - 1]
        if attacker.is_alive():
            cellx, celly = self.original_cells[attacker].coords
            sign = 1 if attacker in self.left_units else -1

            tcell = self.grid[cellx + 1 * sign, celly]
            dist = self.grid.get_pixel_distance(attacker.cell, tcell)
            attacker.move(tcell)
            Timer.create_new(Timer(int(dist * DISTANCE_MS_FACTOR), self.next_attack))
        else:
            Timer.create_new(Timer(500, self.next_attack))

    def stage2(self):
        self.attacking_defenders = [unit for unit in self.defenders if unit not in self.attacked]

        if len(self.attacking_defenders) > 0:
            self.count = 0
            self.next_defender_attack()
        else:
            self.stage3()

    def next_defender_attack(self):
        self.count += 1

        if self.count > len(self.attacking_defenders):
            self.stage3()
            return

        defender = self.attacking_defenders[self.count - 1]

        self.defensive_cells[defender] = defender.cell

        target = self.get_nearest_enemy(defender)
        tarx, tary = target.cell.coords
        sign = 1 if target in self.left_units else -1

        tcell = self.grid[tarx + 1 * sign, tary]
        dist = self.grid.get_pixel_distance(defender.cell, tcell)
        defender.move(tcell)

        timeout = int(dist * DISTANCE_MS_FACTOR)
        Timer.create_new(Timer(timeout, self.do_defender_attack1))

    def do_defender_attack1(self):
        defender = self.attacking_defenders[self.count - 1]
        sign = 1 if defender in self.left_units else -1
        cellx, celly = defender.cell.coords
        target = self.grid[cellx + 1 * sign, celly].occupant

        damage_factor = DEFEND_ATTACK_FACTOR
        if target in self.guarders:
            damage_factor -= GUARD_BONUS
        defender.attack_unit(target, damage_factor)

        Timer.create_new(Timer(750, self.finish_defend_attack))

    def finish_defend_attack(self):
        defender = self.attacking_defenders[self.count - 1]

        tcell = self.defensive_cells[defender]
        dist = self.grid.get_pixel_distance(defender.cell, tcell)
        defender.move(tcell)
        Timer.create_new(Timer(int(dist * DISTANCE_MS_FACTOR), self.about_face))
        Timer.create_new(Timer(int(dist * DISTANCE_MS_FACTOR) + 20, self.next_defender_attack))

    def about_face(self):
        defender = self.attacking_defenders[self.count - 1]
        defender.sprite.set_facing(Facing.RIGHT if defender in self.left_units else Facing.LEFT)

    def stage3(self):
        for avatar in self.original_cells:
            if avatar.is_alive() and avatar.cell != self.original_cells[avatar]:
                avatar.move(self.original_cells[avatar])
        Timer.create_new(Timer(500, self.final_stage))

    def final_stage(self):
        for avatar in self.left_units:
            avatar.sprite.set_facing(Facing.RIGHT)
        for avatar in self.right_units:
            avatar.sprite.set_facing(Facing.LEFT)

        Timer.create_new(Timer(2000, self.end_action))

        self.defenders.clear()
        self.defendees.clear()
        self.attackers.clear()
        self.guarders.clear()
        self.attacked.clear()
        self.defensive_cells.clear()
        self.attacking_defenders.clear()
        self.count = 0

    def update(self, event_list, elapsed):
        pass

    def draw(self, screen):
        self.shadow_panel.draw(screen)