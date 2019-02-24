import pygame
from vector import Vector


# CONSTANTS
CELL_SIZE = 48
BORDER_WIDTH = 2
BORDER_MARGIN = 2


class Cell:
    def __init__(self, coords, origin=(0, 0), pathable=True):
        self.coords = coords
        self.pathable = pathable
        self.occupant = None
        self._origin = origin
        self._border_color = None
        self._fill_color = None
        self._image = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA, 32)

        # For pathfinding only
        self.path_parent = None

    def _render(self):
        if not self._border_color and not self._fill_color:
            self._image = None
        else:
            self._image = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA, 32)

        if self._fill_color:
            pygame.draw.rect(self._image,
                             self._fill_color,
                             pygame.Rect(BORDER_MARGIN, BORDER_MARGIN,
                                         CELL_SIZE - (BORDER_MARGIN * 2),
                                         CELL_SIZE - (BORDER_MARGIN * 2)))
        if self._border_color:
            pygame.draw.rect(self._image,
                             self._border_color,
                             pygame.Rect((BORDER_MARGIN, BORDER_MARGIN,
                                          CELL_SIZE - (BORDER_MARGIN * 2),
                                          CELL_SIZE - (BORDER_MARGIN * 2))),
                             BORDER_WIDTH)

    def get_border_color(self):
        return self._border_color

    def get_fill_color(self):
        return self._fill_color

    def set_border_color(self, new_color):
        self._border_color = new_color
        self._render()

    def set_fill_color(self, new_color):
        self._fill_color = new_color
        self._render()

    def clear_color(self):
        self._fill_color = None
        self._border_color = None
        self._render()

    def get_position(self):
        return Vector(self._origin[0] + self.coords[0] * CELL_SIZE,
                      self._origin[1] + self.coords[1] * CELL_SIZE)

    def get_rect(self):
        return pygame.Rect(self._origin[0] + self.coords[0] * CELL_SIZE,
                           self._origin[1] + self.coords[1] * CELL_SIZE,
                           CELL_SIZE,
                           CELL_SIZE)

    def draw(self, screen: pygame.Surface):
        if self._image:
            screen.blit(self._image, (self.get_rect()[0], self.get_rect()[1]))

    def __str__(self):
        return f'[{self.coords[0]},{self.coords[1]}]'

