import random
from grid import *
from animated_sprite import *
from floating_text import *
from timer import Timer
from vector import Vector
from sfx import SFX


# CONSTANTS
DEFEND_BONUS = 0.50
UNIT_CELL_OFFSET = (0, 0)

class AvatarState:
    READY = "READY"
    DEFEND = "DEFEND"


class Avatar:
    def __init__(self, animated_sprite: AnimatedSprite, cell: Cell, stack_count, life, speed, armor, power, accuracy):
        self.state = AvatarState.READY
        self.sprite = animated_sprite
        self.armor = armor
        self.power = power
        self.speed = speed
        self.max_life = life * stack_count
        self.accuracy = accuracy

        self.cell = cell
        cell.occupant = self
        self.sprite.set_position(Vector(self.cell.get_position()) + UNIT_CELL_OFFSET)

        self._current_life = self.max_life
        self._stack_life = life

        self._blood_sfx = None

    def get_stack_count(self):
        return self._current_life // self._stack_life

    def die(self):
        self._current_life = 0
        # sprite.start_animation(death)
        # Timer.create_new(Timer(HIT_ANIM_DURATION * 2, lambda: self.sprite.set_dead()))

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

        color = (230, 20, 20) if value < 0 else (20, 230, 20)
        direction = Vector(random.random(), -random.random())
        FloatingText.create_new(FloatingText(str(value), self.sprite.get_position(), color, direction))

        self._current_life += value

        # Handle animation
        if value < 0:
            self._blood_sfx = self._generate_blood_sfx()
            if self._current_life <= 0:
                self.die()

    # Runs attack animation and actually does damage
    def attack_unit(self, target):
        damage = int(random.randrange(self.power - int(self.power * (1 - self.accuracy)),
                                      self.power + int(self.power * (1 - self.accuracy))))

        # Cut by armor
        damage -= target.armor

        # Cut by defend bonus
        if target.state == AvatarState.DEFEND:
            damage *= DEFEND_BONUS

        # Damage must be at least 1
        if damage < 1:
            damage = 1

        # sprite.start_animation(Animation.ATTACK)
        # Timer.create_new(Timer(sprite.attack_hit_timeout, lambda: target.alter_life(-damage)))

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
        if self._current_life > 0:
            self.sprite.update(elapsed)

    def draw(self, screen: pygame.Surface):
        self.sprite.draw(screen)
        if self._blood_sfx:
            self._blood_sfx.draw(screen)

    # ----- PRIVATE FUNCTIONS -----
    def _generate_blood_sfx(self):
        start = random.randrange(4) * 6
        return SFX('./assets/_sfx/bloodSheet.png', (12, 2), (64, 64), self.sprite.get_position(),
                   start, start + 6)







