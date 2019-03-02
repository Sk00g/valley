import sys
from suie.element import Element
from suie.rectangle import Rectangle
from suie.panel import Panel
from suie.label import Label
from suie.image import Image
from suie.border import Border
from suie.text_button import TextButton
from suie.image_button import ImageButton
from suie.progress_bar import *
from suie.avatar_icon import AvatarIcon
from suie.action_icon import ActionIcon

pygame.init()

# CONSTANTS
SOURCE_IMAGE = None
SCREEN_WIDTH = 840
SCREEN_HEIGHT = 600

# Global variables
default_font_type = 'emulogic'
default_font_size = 12


def init(source_image):
    global SOURCE_IMAGE
    SOURCE_IMAGE = source_image

