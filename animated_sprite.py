import pygame
import pyganim
from vector import Vector


# CONSTANTS
POSE_PRE_PUNCH = 0
POSE_PUNCH = 1
POSE_CROUCH = 2
POSE_DEAD = 3
POSE_HIT = 4
POSE_SPELL = 5
POSE_STAND = 6
POSE_WALK1 = 7
POSE_WALK2 = 8

FACING_LEFT = 0
FACING_RIGHT = 1

WALK_SPEED = 0.15
WALK_ANIM_INTERVAL = 200  # ms
MIN_MOVE_DISTANCE = 4


class AnimatedSprite:
    def __init__(self, source_file):
        self._position = Vector(0, 0)
        self._target_position = Vector(0, 0)
        self._facing = FACING_LEFT
        self._original_pose_images = pyganim.getImagesFromSpriteSheet(source_file, rows=2, cols=5)[0:9]
        self._pose_images = [pygame.Surface((50, 50), pygame.SRCALPHA, 32)] * 9
        self._current_pose = POSE_STAND
        self._render()

        # For walking
        self._time_since_walk_anim = 0
        self._temp_anim_start = None
        self._temp_anim_duration = 0

        # For auto-slide
        self._slide_target = None
        self._slide_distance = None
        self._slide_duration = 0
        self._slide_elapsed = 0

        # For fixed-slide
        self._slide_list = None
        self._slide_interval = 0
        self._slide_time_since_last = 0

    # ----- PRIVATE -----
    def _render(self):
        for i in range(9):
            self._pose_images[i] = pygame.transform.scale2x(self._original_pose_images[i])
            if self._facing == FACING_RIGHT:
                self._pose_images[i] = pygame.transform.flip(self._pose_images[i], True, False)

    # ----- PUBLIC -----
    def move(self, target_pos):
        self._target_position = Vector(target_pos)
        self.set_facing(FACING_LEFT if target_pos[0] < self._position[0] else FACING_RIGHT)
        if self._current_pose != POSE_WALK2 and self._current_pose != POSE_WALK2:
            self.set_pose(POSE_WALK1)
            self._time_since_walk_anim = 0

    def slide(self, vector: Vector, duration_ms):
        if self._target_position != self._position:
            raise Exception("Cannot slide while walking...")

        self._slide_target = self._position + vector
        self._slide_distance = Vector(vector)
        self._slide_duration = duration_ms
        self._slide_elapsed = 0

    def slide_fixed(self, vector_list, interval_ms: int):
        self._slide_list = [Vector(vec) for vec in vector_list]
        self._slide_interval = interval_ms
        self._slide_time_since_last = 0

    def get_pose(self):
        return self._current_pose

    def set_pose(self, new_pose, duration=None):
        self._current_pose = new_pose
        self._temp_anim_start = pygame.time.get_ticks() if duration else None
        self._temp_anim_duration = duration

    def get_facing(self):
        return self._facing

    def set_facing(self, new_facing):
        if self._facing != new_facing:
            self._facing = new_facing
            self._render()

    def get_position(self):
        return self._position

    def get_center(self):
        return Vector(self._position) + (25, 25)

    def set_position(self, new_position):
        self._position = Vector(new_position)
        self._target_position = self._position

    def update(self, elapsed_ms):
        # Handle sliding
        if self._slide_target:
            pct_time = elapsed_ms / self._slide_duration
            distance_increment = self._slide_distance * pct_time
            self.set_position(self._position + distance_increment)
            self._slide_elapsed += elapsed_ms

            if self._slide_elapsed >= self._slide_duration:
                self.set_position(self._slide_target)
                self._slide_target = None
        elif self._slide_list:
            self._slide_time_since_last += elapsed_ms
            if self._slide_time_since_last >= self._slide_interval:
                self.set_position(self._position + self._slide_list[0])
                self._slide_list.remove(self._slide_list[0])
                self._slide_time_since_last = 0
                if len(self._slide_list) == 0:
                    self._slide_list = None

        # Handled timed animation
        if self._temp_anim_start:
            if pygame.time.get_ticks() - self._temp_anim_start > self._temp_anim_duration:
                self.set_pose(POSE_STAND)

        if self._target_position != self._position:
            # Handle walk animation
            self._time_since_walk_anim += elapsed_ms
            if self._time_since_walk_anim > WALK_ANIM_INTERVAL:
                self.set_pose(POSE_WALK2 if self.get_pose() == POSE_WALK1 else POSE_WALK1)
                self._time_since_walk_anim = 0

            # Move the sprite
            if (self._target_position - self._position).norm() < MIN_MOVE_DISTANCE:
                self._position = self._target_position
                self.set_pose(POSE_STAND)
            else:
                dist = elapsed_ms * WALK_SPEED
                dir = (self._target_position - self._position).normalize()
                self._position += dir * dist

    def draw(self, screen: pygame.Surface):
        screen.blit(self._pose_images[self._current_pose], self.get_position())




