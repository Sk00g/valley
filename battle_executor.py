"""
LOOP

If all units have acted end execution

Move in front of unit to strike. If defended find 'next' available defender and move in front
If unit is dead find closest enemy unit.

Wait 1 second

Strike new target. Full for not defended. 50% for defended.
Defense bonus applies every time. Only retaliate once per unit per round.

Wait 500ms before retaliate

Retaliate does 50% damage, reduced before armor. Retaliate only applies if unit survives the attack

Wait 1 secons

Move back to origin if attacker is alive

Wait 1 second

END LOOP

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
GUARD_BONUS = 0.25
# This multiplied by distance equals move duration in ms
DISTANCE_MS_FACTOR = 10.0


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

        if len(self.defenders) > 0:
            Timer.create_new(Timer(2000, self.next_attack))
        else:
            self.next_attack()

    def next_attack(self):
        if self.either_team_is_dead():
            self.stage7()
            return

        self.count += 1

        if self.count > len(self.attackers):
            self.stage2()
            return

        attacker = self.attackers[self.count - 1]
        target = self.orders[attacker]['target']
        tarx, tary = target.cell.coords
        sign = 1 if attacker in self.right_units else -1

        if not target.is_alive():
            # find closest
            pass
        elif target in self.defendees:
            tarx += 1 * sign

        tcell = self.grid[tarx + 1 * sign, tary]
        dist = self.grid.get_pixel_distance(attacker.cell, tcell)
        print('dist:', dist)
        attacker.move(tcell)
        print('waiting %dms' % int(dist * DISTANCE_MS_FACTOR))
        Timer.create_new(Timer(int(dist * DISTANCE_MS_FACTOR), self.do_attack1))

    def do_attack1(self):
        attacker = self.attackers[self.count - 1]
        target = self.orders[attacker]['target']

        damage_factor = 1.0
        if target in self.guarders:
            damage_factor -= GUARD_BONUS
        attacker.attack_unit(target, damage_factor)

        if target in self.defenders:
            Timer.create_new(Timer(750, lambda: self.retaliate(target, attacker)))
        else:
            Timer.create_new(Timer(750, self.finish_attack))

    def retaliate(self, retaliator, target):
        retaliator.attack_unit(target, 0.5)
        Timer.create_new(Timer(750, self.finish_attack))

    def finish_attack(self):
        attacker = self.attackers[self.count - 1]
        cellx, celly = attacker.cell.coords
        sign = 1 if attacker in self.left_units else -1

        tcell = self.grid[cellx + 1 * sign, celly]
        dist = self.grid.get_pixel_distance(attacker.cell, tcell)
        attacker.move(tcell)
        print('waiting %dms' % int(dist * DISTANCE_MS_FACTOR))
        Timer.create_new(Timer(int(dist * DISTANCE_MS_FACTOR), self.next_attack))

    def stage2(self):
        self.stage7()

    def stage7(self):
        for avatar in self.original_cells:
            if avatar.cell != self.original_cells[avatar]:
                avatar.move(self.original_cells[avatar])
        Timer.create_new(Timer(2000, self.final_stage))

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
        self.count = 0

    def update(self, event_list, elapsed):
        pass

    def draw(self, screen):
        self.shadow_panel.draw(screen)