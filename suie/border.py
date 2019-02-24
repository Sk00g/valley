# A border using custom images, surrounding a colored background
import pygame
import suie

# CONSTANTS
BORDER_TYPE_NONE = 0
BORDER_TYPE_SINGLE = 1
BORDER_TYPE_DOUBLE = 2

SINGLE_BORDER_SIZE = 6  # Including shadow
SINGLE_RECTS = [
    pygame.Rect(867, 400, 17, 17),  # tl
    pygame.Rect(951, 400, 20, 8),   # he
    pygame.Rect(982, 400, 17, 17),  # tr
    pygame.Rect(867, 428, 8, 20),   # ve
    pygame.Rect(982, 498, 17, 17),  # br
    pygame.Rect(867, 498, 17, 17)   # bl
]


class Border(suie.Element):
    # Size parameter defines the size INSIDE the border
    def __init__(self, position, size, bgnd_color=(0, 0, 0), border_type=BORDER_TYPE_SINGLE):
        suie.Element.__init__(self, position)
        self._size = size
        # Including border pixels
        self._full_size = (size[0] + SINGLE_BORDER_SIZE, size[1] + SINGLE_BORDER_SIZE)
        self._background_color = bgnd_color
        self._border_type = border_type
        # Surface list starts from top left and works clockwise to left (bottom left)
        self._surface_list = list()
        self._populate_surface_list()
        # Generate our surfaces
        self._render()

    def _populate_surface_list(self):
        for rect in SINGLE_RECTS:
            surf = pygame.Surface(size=rect[2:4])
            surf.blit(suie.SOURCE_IMAGE, (0, 0), rect)
            self._surface_list.append(surf)

    def _render(self):
        self._image = pygame.Surface(size=self._full_size)
        # First fill the background
        self._image.fill(self._background_color,
                         pygame.Rect(SINGLE_BORDER_SIZE,
                                     SINGLE_BORDER_SIZE,
                                     self._image.get_rect()[2] - SINGLE_BORDER_SIZE * 2,
                                     self._image.get_rect()[3] - SINGLE_BORDER_SIZE * 2))

        # Then the corner borders
        self._image.blit(self._surface_list[0], (0, 0), special_flags=pygame.BLEND_ADD)
        self._image.blit(self._surface_list[2],
                         (self._full_size[0] - 17, 0),
                         special_flags=pygame.BLEND_ADD)
        self._image.blit(self._surface_list[4],
                         (self._full_size[0] - 17, self._full_size[1] - 17),
                         special_flags=pygame.BLEND_ADD)
        self._image.blit(self._surface_list[5],
                         (0, self._full_size[1] - 17),
                         special_flags=pygame.BLEND_ADD)

        # Horizontal edges
        curx = 17
        while curx < self._full_size[0] - 17 - 20:
            self._image.blit(self._surface_list[1], (curx, 0), special_flags=pygame.BLEND_ADD)
            self._image.blit(self._surface_list[1],
                             (curx, self._full_size[1] - 8),
                             special_flags=pygame.BLEND_ADD)
            curx = curx + 20
        distance_left = (self._full_size[0] - 17) - curx
        self._image.blit(self._surface_list[1],
                         (curx, 0),
                         (0, 0, distance_left, 8),
                         special_flags=pygame.BLEND_ADD)
        self._image.blit(self._surface_list[1],
                         (curx, self._full_size[1] - 8),
                         (0, 0, distance_left, 8),
                         special_flags=pygame.BLEND_ADD)
        # Vertical edges
        cury = 17
        while cury < self._full_size[1] - 17 - 20:
            self._image.blit(self._surface_list[3], (0, cury), special_flags=pygame.BLEND_ADD)
            self._image.blit(self._surface_list[3],
                             (self._full_size[0] - 8, cury),
                             special_flags=pygame.BLEND_ADD)
            cury = cury + 20
        distance_left = (self._full_size[1] - 17) - cury
        self._image.blit(self._surface_list[3],
                         (0, cury),
                         (0, 0, 8, distance_left),
                         special_flags=pygame.BLEND_ADD)
        self._image.blit(self._surface_list[3],
                         (self._full_size[0] - 8, cury),
                         (0, 0, 8, distance_left),
                         special_flags=pygame.BLEND_ADD)

    def get_display_rect(self):
        return pygame.Rect(self._position + self._size)

    def set_size(self, new_size):
        self._size = new_size
        self._full_size = (self._size[0] + SINGLE_BORDER_SIZE,
                           self._size[1] + SINGLE_BORDER_SIZE)
        self._render()

    def draw(self, screen: pygame.Surface):
        screen.blit(self._image, self._get_final_position())


