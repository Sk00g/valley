import pygame
import suie


class Rectangle(suie.Element):
    def __init__(self, position, size, fill_color=(0, 0, 0, 255), border_color=None, border_thickness=1):
        suie.Element.__init__(self, position)

        self._size = size
        self._fill_color = fill_color
        self._border_color = border_color
        self._border_thickness = border_thickness

        self._render()

    def _render(self):
        thick, size = self._border_thickness, self._size

        self._image = pygame.Surface(size, pygame.SRCALPHA, 32)
        if self._fill_color:
            self._image.fill(self._fill_color,
                             (thick, thick, size[0] - thick * 2, size[1] - thick * 2))

        if self._border_thickness > 0 and self._border_color:
            self._image.fill(self._border_color, (0, 0, size[0], thick))
            self._image.fill(self._border_color, (0, 0, thick, size[1]))
            self._image.fill(self._border_color, (0, size[1] - thick, size[0], thick))
            self._image.fill(self._border_color, (size[0] - thick, 0, thick, size[1]))

    def get_display_rect(self):
        return pygame.Rect(self._position + self._size)

    def set_color(self, color):
        self._fill_color = color
        self._render()

    def set_border(self, color, thickness):
        self._border_color = color
        self._border_thickness = thickness
        self._render()

    def resize(self, new_size):
        self._size = new_size
        self._render()

    def draw(self, screen: pygame.Surface):
        screen.blit(self._image, self._get_final_position())


