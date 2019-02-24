import pygame
from suie.element import Element
from suie.panel import Panel
from suie.label import Label
from suie.image import Image
from suie.border import Border
from suie.text_button import TextButton
from suie.image_button import ImageButton
from suie.progress_bar import *

pygame.init()

# CONSTANTS
SOURCE_IMAGE = None

# Global variables
default_font_type = 'emulogic'
default_font_size = 12


def init(source_image):
    global SOURCE_IMAGE
    SOURCE_IMAGE = source_image

