# Click-able button with text
import pygame
import suie
import asset_manager

# CONSTANTS
DEFAULT_SIZE = 12
DEFAULT_COLOR = (240, 240, 240)
DEFAULT_BTN_RECT = pygame.Rect(16, 125, 281, 56)
HIGHLIGHT_BTN_RECT = pygame.Rect(16, 281, 281, 56)
PRESSED_BTN_RECT = pygame.Rect(16, 203, 281, 56)

BTN_STATE_DEFAULT = 0
BTN_STATE_MOUSEOVER = 1
BTN_STATE_PRESSED = 2


class TextButton(suie.Element):
    def __init__(self, position, text: str, callback):
        suie.Element.__init__(self, position)
        self._text = text
        self._callback = callback
        self._default_surface = pygame.Surface((281, 56), pygame.SRCALPHA, 32)
        self._highlight_surface = pygame.Surface((281, 56), pygame.SRCALPHA, 32)
        self._pressed_surface = pygame.Surface((281, 56), pygame.SRCALPHA, 32)
        self._surface_list = [self._default_surface,
                              self._highlight_surface,
                              self._pressed_surface]
        self._state = BTN_STATE_DEFAULT

        # Initial render
        self._render()

    def _render(self):
        self._default_surface.blit(suie.SOURCE_IMAGE, (0, 0), DEFAULT_BTN_RECT)
        self._highlight_surface.blit(suie.SOURCE_IMAGE, (0, 0), HIGHLIGHT_BTN_RECT)
        self._pressed_surface.blit(suie.SOURCE_IMAGE, (0, 0), PRESSED_BTN_RECT)

        font = asset_manager.load_font(suie.default_font_type, DEFAULT_SIZE)
        font_surface = font.render(self._text, False, DEFAULT_COLOR)
        font_size = font_surface.get_rect()[2:4]

        locx = (281 - font_size[0]) / 2
        locy = (56 - font_size[1]) / 2
        self._default_surface.blit(font_surface, (locx, locy))
        self._highlight_surface.blit(font_surface, (locx, locy))
        self._pressed_surface.blit(font_surface, (locx + 1, locy + 2))

    def get_display_rect(self):
        return pygame.Rect(self._get_final_position() + (281, 56))

    def update(self, event_list):
        # Handle default state
        if self._state == BTN_STATE_DEFAULT:
            if self.get_display_rect().collidepoint(pygame.mouse.get_pos()):
                self._state = BTN_STATE_MOUSEOVER
        # Handle mouse over state
        elif self._state == BTN_STATE_MOUSEOVER:
            if not self.get_display_rect().collidepoint(pygame.mouse.get_pos()):
                self._state = BTN_STATE_DEFAULT
            else:
                for event in event_list:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        self._state = BTN_STATE_PRESSED
        # Handle pressed state
        elif self._state == BTN_STATE_PRESSED:
            if not self.get_display_rect().collidepoint(pygame.mouse.get_pos()):
                self._state = BTN_STATE_DEFAULT
            else:
                for event in event_list:
                    if event.type == pygame.MOUSEBUTTONUP:
                        self._state = BTN_STATE_MOUSEOVER
                        self._callback()

    def draw(self, screen: pygame.Surface):
        # Draw different surface based on button state
        if self._state == BTN_STATE_DEFAULT:
            screen.blit(self._default_surface, self._get_final_position())
        elif self._state == BTN_STATE_MOUSEOVER:
            screen.blit(self._highlight_surface, self._get_final_position())
        elif self._state == BTN_STATE_PRESSED:
            screen.blit(self._pressed_surface, self._get_final_position())

