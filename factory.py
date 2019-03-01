import json
import os
import asset_manager
import suie
from pygame import Rect
from animated_sprite import AnimatedSprite
from grid import Cell
from avatar import Avatar


def generate_wc_icon(index, size):
    source = asset_manager.load_image('ui/wc2Icons.png')
    width, height = 46, 38
    x, y = (index % 10) * (width + 3), index // 10 * (height + 3)
    return suie.Image(source, (0, 0), size, source_rect=Rect(x, y, width, height))

def generate_wc_button_icon(index, size, action):
    source = asset_manager.load_image('ui/wc2Icons.png')
    width, height = 46, 38
    x, y = (index % 10) * (width + 3), index // 10 * (height + 3)
    return suie.ImageButton(source, action, (0, 0), size, source_rect=Rect(x, y, width, height))

def generate_avatar(unit_type: str, stack_count, cell: Cell=None):
    with open('pdata/wcAnimations.json', 'r') as file:
        sheet_data = json.load(file)
        sprite = AnimatedSprite(os.path.join('assets', 'unit', unit_type) + '.png', **sheet_data[unit_type])

    with open('pdata/wcUnits.json', 'r') as file:
        unit_data = json.load(file)
        avatar = Avatar(sprite, stack_count, cell, **unit_data[unit_type])

    return avatar