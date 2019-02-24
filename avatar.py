import random
from grid import *
from animated_sprite import *
from floating_text import *
from timer import Timer
from vector import Vector
from sfx import SFX


# UNIT STATES
UNIT_STATE_READY = 0
UNIT_STATE_WAIT = 1
UNIT_STATE_DEAD = 2
UNIT_STATE_ACTIVE = 3
UNIT_STATE_RETALIATE = 4

# CONSTANTS
HIT_ANIM_DURATION = 600
UNIT_CELL_OFFSET = (-1, -6)

UNIT_STAT_LIFE = 0
UNIT_STAT_SPEED = 1
UNIT_STAT_ARMOR = 2
UNIT_STAT_POWER = 3

ATTACK_STYLE_CHOP = 0
ATTACK_STYLE_STAB = 1
ATTACK_STYLE_BOW = 2
ATTACK_STYLE_THROW = 3


class Avatar:
    def __init__(self, animated_sprite: AnimatedSprite, cell: Cell, max_life, speed, armor, power):
        self.state = UNIT_STATE_READY
        self.sprite = animated_sprite
        self.armor = armor
        self.power = power
        self.speed = speed

        self.cell = cell
        cell.occupant = self
        self.sprite.set_position(Vector(self.cell.get_position()) + UNIT_CELL_OFFSET)

        self._max_life = max_life
        self._current_life = max_life

        self._blood_sfx = None
        self._move_path = None
        self._weapon_image = None

        self.weapon = None
        self.armor = None
        self.accessory = None
        self.items = [self.weapon, self.armor, self.accessory]

    def get_max_life(self):
        return self._max_life

    def get_current_life(self):
        return self._current_life

    def die(self):
        self._current_life = 0
        Timer.create_new(Timer(HIT_ANIM_DURATION * 2, lambda: self.sprite.set_pose(POSE_DEAD)))
        self.state = UNIT_STATE_DEAD

    # Positive value to heal, negative to deal damage
    # Induces related graphical effects, potential death, etc.
    def alter_life(self, value):
        # Cannot affect the life of dead units
        if self.state == UNIT_STATE_DEAD:
            return

        # Ensure value cannot heal above max life
        if self._current_life + value > self._max_life:
            value = self._max_life - self._current_life

        # Ensure value cannot reduce below 0
        if self._current_life - value < 0:
            value = -self._current_life

        color = (230, 20, 20) if value < 0 else (20, 230, 20)
        direction = Vector(random.random(), -random.random())
        FloatingText.create_new(FloatingText(str(value), self.sprite.get_position(), color, direction))

        self._current_life = self._current_life + value

        # Handle animation
        if value < 0:
            self.sprite.set_pose(POSE_HIT, HIT_ANIM_DURATION)
            self._blood_sfx = self._generate_blood_sfx()
            if self._current_life <= 0:
                self.die()

    # Runs attack animation and actually does damage
    def attack_unit(self, target):
        pass

    # No idea how this will be implemented yet
    def use_ability(self, ability, target):
        pass

    # Reset unit's position to it's cell position
    def reset_position(self):
        self.sprite.set_position(self.cell.get_position() + UNIT_CELL_OFFSET)

    # Moves sprite and updates other values
    def move(self, cell_path):
        self.cell.occupant = None
        self.cell = cell_path[0]
        self.cell.occupant = self
        self.sprite.move(cell_path[len(cell_path) - 1].get_position() + UNIT_CELL_OFFSET)
        self._move_path = cell_path

    def update(self, elapsed):
        # Handle move path
        if self._move_path:
            if len(self._move_path) == 1:
                self._move_path = None
            else:
                pos = Vector(self.sprite.get_position())
                tar = Vector(self._move_path[len(self._move_path) - 1].get_position() + UNIT_CELL_OFFSET)
                dist = math.fabs((pos - tar).norm())
                if dist < 10:
                    self._move_path.pop()
                    self.sprite.move(self._move_path[len(self._move_path) - 1].get_position() + UNIT_CELL_OFFSET*8)

        if self.state != UNIT_STATE_DEAD:
            self.sprite.update(elapsed)
        if self._weapon_image:
            self._weapon_image.update(elapsed)

    def draw(self, screen: pygame.Surface):
        if self._weapon_image:
            self._weapon_image.draw(screen)
        self.sprite.draw(screen)
        if self._blood_sfx:
            self._blood_sfx.draw(screen)

    # ----- PRIVATE FUNCTIONS -----
    def _generate_blood_sfx(self):
        start = random.randrange(4) * 6
        return SFX('./assets/_sfx/bloodSheet.png', (12, 2), (64, 64), self.sprite.get_position(),
                   start, start + 6)







