"""
Shadow entire screen except grid
Float text 'ROUND #' then disappear
Wait 2 seconds

Defending units move immediately all at once
Multiple units defending the same ally will stack in a preset pattern
@ 1 2
    2
@ 1 4
    3 5

Wait 3 seconds

Fastest attacking unit starts. Speed tie broken by random

LOOP

If all enemies dead end execution
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


SCENE_SIZE = 450, 400


class BattleExecutor:
    def __init__(self, left_units, right_units, grid):
        self.all_units = left_units + right_units
        self.left_units = left_units
        self.right_units = right_units
        self.grid = grid

        self.shadow_panel = suie.Panel((0, 0), (suie.SCREEN_WIDTH, suie.SCREEN_HEIGHT))
        self._generate_shadows()

        self.end_action = None

    def _generate_shadows(self):
        size = (suie.SCREEN_WIDTH - SCENE_SIZE[0]) // 2, (suie.SCREEN_HEIGHT - SCENE_SIZE[1]) // 2 + 2
        self.shadow_panel.add_child(suie.Rectangle((0, 0), (suie.SCREEN_WIDTH, size[1]), (0, 0, 0, 180)))
        self.shadow_panel.add_child(suie.Rectangle((0, size[1] - 2), (size[0], suie.SCREEN_HEIGHT - size[1] + 2), (0, 0, 0, 180)))
        self.shadow_panel.add_child(suie.Rectangle((size[0] - 2, suie.SCREEN_HEIGHT - size[1]), (suie.SCREEN_WIDTH, size[1]), (0, 0, 0, 180)))
        self.shadow_panel.add_child(suie.Rectangle((suie.SCREEN_WIDTH - size[0], size[1] - 2), (size[0], SCENE_SIZE[1]), (0, 0, 0, 180)))

    def execute(self, unit_orders, end_action):
        self.end_action = end_action
        self.grid.reset_cell_colors()

        Timer.create_new(Timer(10000, self.end_action))

    def update(self, event_list, elapsed):
        pass

    def draw(self, screen):
        self.shadow_panel.draw(screen)
























