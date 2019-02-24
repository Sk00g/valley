import pygame
import math
from vector import Vector
from cell import Cell
from collections import deque

"""
cell_count = (wide, high))
"""
# CONSTANTS
class CellColor:
    RED = (200, 50, 50, 120)
    GREEN = (50, 200, 50, 120)
    BLUE = (50, 50, 200, 120)


# blocked_cells parameter should be a list of tuples with the coordinates of blocked cells
class Grid:
    def __init__(self, origin: Vector, cell_count, blocked_cells=None):
        self._origin = origin
        self._cell_list = list()
        self.cell_count = cell_count

        if not blocked_cells:
            blocked_cells = []

        for x in range(cell_count[0]):
            self._cell_list.append(list())
            for y in range(cell_count[1]):
                self._cell_list[x].append(Cell((x, y), origin) if (x, y) not in blocked_cells else Cell((x, y), origin, False))

    # Input tuple coordinates and return Cell object at those coordinates
    def __getitem__(self, key):
        if key[0] < 0 or key[0] > self.cell_count[0] - 1:
            return None
        if key[1] < 0 or key[1] > self.cell_count[1] - 1:
            return None
        return self._cell_list[key[0]][key[1]]

    def reset_cell_colors(self):
        for row in self._cell_list:
            for cell in row:
                cell.clear_color()

    # Set cell_list to None if you want to fill entire grid
    def set_cell_fill_colors(self, coords_list, fill_color):
        if not coords_list:
            for row in self._cell_list:
                for cell in row:
                    cell.set_fill_color(fill_color)
        else:
            for coords in coords_list:
                self[coords].set_fill_color(fill_color)

    # Important pathfinding algorithm, basically an A* without heuristic, return list of cells in order
    def find_path(self, start_cell, end_cell):
        frontier = deque([start_cell])
        explored = []
        while end_cell not in frontier and len(frontier) > 0:
            active = frontier.popleft()
            explored.append(active)
            for cell in self.get_neighbours(active):
                if not cell:
                    continue
                if cell.pathable and not cell.occupant and cell not in explored and cell not in frontier:
                    frontier.append(cell)
                    cell.path_parent = active

        # If frontier is empty at this point, there is no valid path
        if len(frontier) == 0:
            return None
        else:
            path = [end_cell]
            while start_cell not in path:
                path.append(path[len(path) - 1].path_parent)
            # Don't include start
            path.remove(start_cell)
            return path

    def draw(self, screen: pygame.Surface):
        for row in self._cell_list:
            for cell in row:
                cell.draw(screen)

    def get_distance(self, start: Cell, end: Cell, pathable=False):
        if not pathable:
            return math.fabs(start[0] - end[0]) + math.fabs(start[1] - end[1])
        else:
            return len(self.find_path(start, end)) - 1

    def get_neighbours(self, cell: Cell):
        x, y = cell.coords[0], cell.coords[1]
        return [self[(x+1, y)], self[(x-1, y)], self[(x, y+1)], self[(x, y-1)]]

    def debug_fill(self):
        for row in self._cell_list:
            for cell in row:
                if cell.occupant or not cell.pathable:
                    cell.set_fill_color(CellColor.BLUE)
                else:
                    cell.set_fill_color(CellColor.GREEN)

