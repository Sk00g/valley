import random
import suie
from grid import *
from animated_sprite import *
from floating_text import *
from timer import Timer
from vector import Vector
from sfx import SFX


# CONSTANTS
DEFEND_BONUS = 0.50
UNIT_CELL_OFFSET = (-25, -25)
STACK_TEXT_OFFSET = (57, 56)
BLOOD_OFFSET = (4, 0)

class AvatarState:
    READY = "READY"
    DEFEND = "DEFEND"


class Avatar:
    def __init__(self, animated_sprite: AnimatedSprite, cell: Cell, stack_count, **kwargs):
        self.state = AvatarState.READY
        self.sprite = animated_sprite
        self.armor = kwargs['armor']
        self.power = kwargs['power']
        self.speed = kwargs['speed']
        self.max_life = kwargs['life'] * stack_count
        self.accuracy = kwargs['accuracy']

        self.cell = cell
        cell.occupant = self
        self.sprite.set_position(Vector(self.cell.get_position()) + UNIT_CELL_OFFSET)

        self._current_life = self.max_life
        self._stack_life = kwargs['life']

        self._blood_sfx = None

        border = suie.Border((0, 0), (24, 24))
        border.visible = False
        self._stack_shadow = suie.Label((2, 2), str(stack_count), 18, color=(0, 0, 0, 100))
        self._stack_number = suie.Label((0, 0), str(stack_count), 18, color=(120, 255, 120, 255))
        self._stack_panel = suie.Panel(self.sprite.get_position() + STACK_TEXT_OFFSET, (24, 24),
                                       [border, self._stack_shadow, self._stack_number])

    def get_stack_count(self):
        return (self._current_life + 1) // self._stack_life + 1

    def die(self):
        self._current_life = 0
        self.sprite.start_animation(Animation.DEATH)

    # Positive value to heal, negative to deal damage
    # Induces related graphical effects, potential death, etc.
    def alter_life(self, value):
        # Cannot affect the life of dead units
        if self._current_life == 0:
            return

        # Ensure value cannot heal above max life
        if self._current_life + value > self.max_life:
            value = self.max_life - self._current_life

        # Ensure value cannot reduce below 0
        if self._current_life + value < 0:
            value = -self._current_life

        color = (230, 40, 40) if value < 0 else (50, 230, 50)
        direction = Vector(random.random(), -random.random())
        FloatingText.create_new(FloatingText(str(value), self.sprite.get_center(), color, direction))

        self._current_life += value

        # Handle animation
        if value < 0:
            self._stack_number.set_text(str(self.get_stack_count()))
            self._stack_shadow.set_text(str(self.get_stack_count()))

            self._blood_sfx = self._generate_blood_sfx()
            if self._current_life <= 0:
                self.die()

    # Runs attack animation and actually does damage
    def attack_unit(self, target):
        if self.cell.coords[0] < target.cell.coords[0] and self.sprite.get_facing() == Facing.LEFT:
            self.sprite.set_facing(Facing.RIGHT)
        elif self.cell.coords[0] > target.cell.coords[0] and self.sprite.get_facing() == Facing.RIGHT:
            self.sprite.set_facing(Facing.LEFT)

        damage = int(random.randrange(self.power - int(self.power * (1 - self.accuracy)),
                                      self.power + int(self.power * (1 - self.accuracy))))
        damage *= self.get_stack_count()

        # Cut by armor
        damage -= target.armor

        # Cut by defend bonus
        if target.state == AvatarState.DEFEND:
            damage *= DEFEND_BONUS

        # Damage must be at least 1
        if damage < 1:
            damage = 1

        self.sprite.start_animation(Animation.ATTACK)
        Timer.create_new(Timer(self.sprite.attack_hit_timeout, lambda: target.alter_life(-damage)))

    # No idea how this will be implemented yet
    def use_ability(self, ability, target):
        pass

    # Moves sprite and updates other values
    def move(self, target):
        self.cell.occupant = None
        self.cell = target
        self.cell.occupant = self
        self.sprite.move(target.get_position() + UNIT_CELL_OFFSET)

    def update(self, elapsed):
        self._stack_panel.set_position(self.sprite.get_position() + STACK_TEXT_OFFSET)
        self.sprite.update(elapsed)

    def draw(self, screen: pygame.Surface):
        self.sprite.draw(screen)
        if self._blood_sfx:
            self._blood_sfx.draw(screen)
        if self._current_life > 0:
            self._stack_panel.draw(screen)

    # ----- PRIVATE FUNCTIONS -----
    def _generate_blood_sfx(self):
        start = random.randrange(4) * 6
        angle = random.randrange(0, 180)
        return SFX('assets/sfx/bloodSheet.png', (12, 2), (64, 64),
                   self.sprite.get_position() + BLOOD_OFFSET,
                   start, start + 6, rotation=angle)







