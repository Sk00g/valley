

class BattleExecutor:
    def __init__(self, left_units, right_units, grid):
        self.all_units = left_units + right_units
        self.left_units = left_units
        self.right_units = right_units
        self.grid = grid

    def execute(self, unit_orders):
        print('doing awesome battle stuff now')
        print(str(unit_orders))