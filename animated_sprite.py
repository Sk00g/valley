import pygame
import pyganim
from timer import Timer
from vector import Vector


class Animation:
    WALK = "WALK"
    ATTACK = "ATTACK"
    DEATH = "DEATH"
    DEATH2 = "DEATH2"

class Facing:
    LEFT = 0
    RIGHT = 1

WALK_SPEED = 0.15
WALK_ANIM_INTERVAL = 200  # ms
MIN_MOVE_DISTANCE = 4
SPRITE_SCALE = 1.3

"""
animations: {
    Animation.WALK: [{"index": ..., "duration": ...}, {"index": ..., "duration": ...}, etc...],
    Animation.ATTACK: {...}
}
"""

class AnimatedSprite:
    def __init__(self, source_file, **kwargs):
        self.attack_hit_timeout = kwargs['attack_hit_timeout']
        self.death_timeout = kwargs['death_timeout']
        self.dead_index = kwargs['dead_index']
        self.dead_index2 = kwargs['dead_index2']

        self._position = Vector(0, 0)
        self._target_position = Vector(0, 0)
        self._facing = Facing.LEFT
        self._original_source_images = pyganim.getImagesFromSpriteSheet(source_file, rows=kwargs['rows'], cols=kwargs['cols'])
        self._source_image_count = kwargs['rows'] * kwargs['cols']
        self._animations = kwargs['animations']
        self._current_animation = None
        self._default_index = kwargs['default_index']
        self._static_index = self._default_index
        self.reset()

        # Setup source image array
        self._source_images = []
        width, height = self._original_source_images[0].get_size()
        for i in range(self._source_image_count):
            self._source_images.append(pygame.Surface((width * SPRITE_SCALE, height * SPRITE_SCALE), pygame.SRCALPHA))
        self._render()

        # For animation
        self._animation_timer = 0
        self._animation_step = 0
        self._animation_looping = False

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
        for i in range(self._source_image_count):
            self._source_images[i] = pygame.transform.scale(self._original_source_images[i], self._source_images[i].get_size())
            if self._facing == Facing.LEFT:
                self._source_images[i] = pygame.transform.flip(self._source_images[i], True, False)

    # ----- PUBLIC -----
    def reset(self):
        self.set_static_index(self._default_index)

    def start_animation(self, anim_type, looping=False):
        if not anim_type in self._animations:
            raise ValueError("This sprite doesn't support animation '%s'" % anim_type)

        self._animation_timer = 0
        self._animation_step = 0
        self._animation_looping = looping
        self._current_animation = anim_type
        self._static_index = None

        if anim_type == Animation.DEATH:
            Timer.create_new(Timer(self.death_timeout, lambda: self.set_static_index(self.dead_index)))


    def move(self, target_pos):
        self._target_position = Vector(target_pos)
        self.set_facing(Facing.LEFT if target_pos[0] < self._position[0] else Facing.RIGHT)
        if self._current_animation != Animation.WALK:
            self.start_animation(Animation.WALK, True)

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

    def get_animation(self):
        return self._current_animation

    def set_static_index(self, index):
        self._static_index = index

        if self._current_animation:
            self._current_animation = None

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
        # Update animation
        if self._current_animation:
            anim = self._animations[self._current_animation]
            self._animation_timer += elapsed_ms
            if self._animation_timer >= anim[self._animation_step]['duration']:
                self._animation_timer = 0
                self._animation_step += 1

                if self._animation_step >= len(anim):
                    if self._animation_looping:
                        self._animation_step = 0
                    else:
                        self.reset()

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

        if self._target_position != self._position:
            # Move the sprite
            if (self._target_position - self._position).norm() < MIN_MOVE_DISTANCE:
                self._position = self._target_position
                self.reset()
            else:
                dist = elapsed_ms * WALK_SPEED
                dir = (self._target_position - self._position).normalize()
                self._position += dir * dist

    def draw(self, screen: pygame.Surface):
        if self._static_index:
            screen.blit(self._source_images[self._static_index], self.get_position())
        else:
            source_index = self._animations[self._current_animation][self._animation_step]['index']
            screen.blit(self._source_images[source_index], self.get_position())




