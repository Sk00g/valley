import pygame
import pyganim
import asset_manager
from vector import Vector


class SFXStatic:
    def __init__(self, source_file, source_rect, size, pos, rotation, shadow=False):
        source_image = asset_manager.load_image(source_file)
        self._original_image = pygame.Surface(source_rect[2:4], pygame.SRCALPHA, 32)
        self._original_image.blit(source_image, (0, 0), source_rect)
        self._image = None
        self._rotation = rotation
        self._size = size
        self._flipx = False
        self._flipy = False

        self.shadow = shadow
        self.position = Vector(pos)

        self._render()

        # For auto-slide
        self._slide_target = None
        self._slide_distance = None
        self._slide_duration = 0
        self._slide_elapsed = 0

        # For fixed-slide
        self._slide_list = None
        self._slide_interval = 0
        self._slide_time_since_last = 0

    def _render(self):
        self._image = pygame.transform.scale(self._original_image, self._size)
        self._image = pygame.transform.rotate(self._image, self._rotation)
        self._image = pygame.transform.flip(self._image, self._flipx, self._flipy)

    def slide(self, vector: Vector, duration_ms):
        self._slide_target = self.position + vector
        self._slide_distance = Vector(vector)
        self._slide_duration = duration_ms
        self._slide_elapsed = 0

    def slide_fixed(self, vector_list, interval_ms: int):
        self._slide_list = [Vector(vec) for vec in vector_list]
        self._slide_interval = interval_ms
        self._slide_time_since_last = 0

    def set_flip(self, horizontal: bool, vertical: bool):
        self._flipx = horizontal
        self._flipy = vertical
        self._render()

    def get_rotation(self):
        return self._rotation

    def set_rotation(self, new_rotation):
        self._rotation = new_rotation
        self._render()

    def get_size(self):
        return self._size

    def set_size(self, new_size):
        self._size = new_size
        self._render()

    def update(self, elapsed_ms):
        # Handle sliding
        if self._slide_target:
            pct_time = elapsed_ms / self._slide_duration
            distance_increment = self._slide_distance * pct_time
            self.position += distance_increment
            self._slide_elapsed += elapsed_ms

            if self._slide_elapsed >= self._slide_duration:
                self.position = self._slide_target
                self._slide_target = None
        elif self._slide_list:
            self._slide_time_since_last += elapsed_ms
            if self._slide_time_since_last >= self._slide_interval:
                self.position += self._slide_list[0]
                self._slide_list.remove(self._slide_list[0])
                self._slide_time_since_last = 0
                if len(self._slide_list) == 0:
                    self._slide_list = None

    def draw(self, screen: pygame.Surface):
        screen.blit(self._image, self.position)


class SFX:
    def __init__(self, source_file, source_grid, size, pos, frame_start, frame_finish,
                 loop=False, rotation=0, shadow=False, frame_speed=80):
        image_list = pyganim.getImagesFromSpriteSheet(source_file,
                                                      cols=source_grid[0],
                                                      rows=source_grid[1])[frame_start:frame_finish]
        frame_count = frame_finish - frame_start
        self.animation = pyganim.PygAnimation(list(zip(image_list, [frame_speed] * frame_count)), loop)
        self.animation.scale(size)
        self.animation.rotate(rotation)
        self.animation.convert_alpha()
        self.animation.play()

        self.position = pos
        self._rotation = rotation
        self._size = size
        self._shadow = shadow

    def is_finished(self):
        return self.animation.isFinished()

    def get_size(self):
        return self._size

    def get_rotation(self):
        return self._rotation

    def set_size(self, new_size):
        self._size = new_size
        self.animation.scale(new_size)

    def set_rotation(self, new_rotation):
        self._rotation = new_rotation
        self.animation.rotate(new_rotation)

    def draw(self, screen: pygame.Surface):
        self.animation.blit(screen, self.position)




