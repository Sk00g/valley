# Read-only, non-focusable image for GUI
import pygame
import suie


class Image(suie.Element):
    def __init__(self, image: pygame.Surface, position, size=None, source_rect=None):
        suie.Element.__init__(self, position)

        self._size = size if size else image.get_rect()[2:4]
        self._flipx = False
        self._flipy = False

        # Grab only the subsection we need
        if source_rect:
            self._original_image = pygame.Surface(size=source_rect[2:4])
            self._original_image.blit(image, (0, 0), source_rect)
        else:
            self._original_image = image

        self._image = None

        # Generate our initial surface
        self._render()

    def _render(self):
        self._image = pygame.transform.flip(self._original_image, self._flipx, self._flipy)
        self._image = pygame.transform.scale(self._image, self._size)

    def get_display_rect(self):
        return pygame.Rect(self._get_final_position() + self._size)

    def resize(self, new_size):
        self._size = new_size
        self._render()

    def set_flip(self, horizontal: bool, vertical: bool):
        self._flipx = horizontal
        self._flipy = vertical
        self._render()

    def get_flip(self):
        return self._flipx, self._flipy

    def draw(self, screen: pygame.Surface):
        screen.blit(self._image, self._get_final_position())


