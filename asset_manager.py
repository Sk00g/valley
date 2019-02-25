# Handles assets for all other systems. Uses lazy loading
import os
import pygame
import json


# CONSTANTS

# Hold all images that have been loaded, key is file path
__image_dict = {}
__font_dict = {}

def load_image(file_path: str, color_key=None):
    if file_path in __image_dict:
        return __image_dict[file_path]

    fullname = os.path.join('./assets', file_path)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image:', fullname)
        raise message
    image = image.convert_alpha()

    if color_key is not None:
        if color_key is -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key, pygame.RLEACCEL)

    __image_dict[file_path] = image
    return image

def load_font(font_name: str, size: int):
    if (font_name, size) in __font_dict:
        return __font_dict[(font_name, size)]

    try:
        font = pygame.font.SysFont(font_name, size)
    except pygame.error as msg:
        print("Cannot load font:", font_name)
        raise msg

    __font_dict[(font_name, size)] = font
    return font