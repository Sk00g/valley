import pygame
import asset_manager
from vector import Vector


# CONSTANTS
FLOAT_FONT_SIZE = 10
FLOAT_DURATION = 1500  # ms
FLOAT_DISTANCE = 40  # total pixels travelled from origin
DEFAULT_FLOAT_DIR = Vector(1, -1).normalize()  # direction of travel
FLOAT_SPEED = 12  # how far moved per update cycle


class FloatingText:
    text_list = []

    def __init__(self, text, pos, color, direction: Vector=DEFAULT_FLOAT_DIR):
        self._text = text
        self._position = Vector(pos)
        self._distance_travelled = 0
        self._time_alive = 0
        self._direction = Vector(direction).normalize()

        font = asset_manager.load_font('emulogic', FLOAT_FONT_SIZE)
        self._surface = font.render(text, False, color)
        self._shadow = font.render(text, False, (0, 0, 0, 120))

    @staticmethod
    def create_new(text):
        FloatingText.text_list.append(text)
        return text

    @staticmethod
    def update_all(elapsed):
        for text in FloatingText.text_list:
            text._update(elapsed)

    @staticmethod
    def draw_all(screen: pygame.Surface):
        for text in FloatingText.text_list:
            text._draw(screen)

    def _update(self, elapsed):
        if self._distance_travelled < FLOAT_DISTANCE:
            self._position = self._position + (FLOAT_SPEED * self._direction)
            self._distance_travelled += FLOAT_SPEED

        self._time_alive += elapsed
        if self._time_alive > FLOAT_DURATION:
            FloatingText.text_list.remove(self)

    def _draw(self, screen: pygame.Surface):
        screen.blit(self._shadow, self._position + (1, 1))
        screen.blit(self._surface, self._position)






