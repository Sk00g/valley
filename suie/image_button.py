# Clickable image, use outline to show mouse, shift and lines to show click
import pygame
import suie

# CONSTANTS
HIGHLIGHT_COLOR = (50, 220, 255, 255)
PRESSED_COLOR = (200, 85, 50, 255)

BTN_STATE_DEFAULT = 0
BTN_STATE_MOUSEOVER = 1
BTN_STATE_PRESSED = 2


class ImageButton(suie.Element):
    def __init__(self, image: pygame.Surface, callback, position, size=None, source_rect=None):
        suie.Element.__init__(self, position)
        self.icon = suie.Image(image, position, size, source_rect)
        self._callback = callback
        self._state = BTN_STATE_DEFAULT
        self._highlight_surface = pygame.Surface(size, pygame.SRCALPHA, 32)
        self._pressed_surface = pygame.Surface(size, pygame.SRCALPHA, 32)

        # Setup three surfaces
        self._render()

    def _render(self):
        # Only have to generate the outlines
        pygame.draw.rect(self._highlight_surface,
                         HIGHLIGHT_COLOR,
                         pygame.Rect((0, 0) + self.icon._size))
        pygame.draw.rect(self._pressed_surface,
                         PRESSED_COLOR,
                         pygame.Rect((0, 0) + self.icon._size),
                         2)

    def add_panel(self, new_host):
        new_host.add_child(self)
        new_host.add_child(self.icon)

    def set_position(self, new_position):
        super().set_position(new_position)
        self.icon.set_position(new_position)

    def get_display_rect(self):
        return self.icon.get_display_rect()

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
        if self._state == BTN_STATE_DEFAULT:
            pass
        elif self._state == BTN_STATE_MOUSEOVER:
            screen.blit(self._highlight_surface, self._get_final_position())
        elif self._state == BTN_STATE_PRESSED:
            self.icon.set_position((self.icon.get_position()[0] + 1,
                                   self.icon.get_position()[1] + 2))
            self.icon.set_position((self.icon.get_position()[0] - 1,
                                   self.icon.get_position()[1] - 2))
            screen.blit(self._pressed_surface, self._get_final_position())

