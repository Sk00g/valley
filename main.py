import sys
import pygame
from timer import Timer
from pygame.locals import QUIT, KEYDOWN, K_ESCAPE

# Initialize display so we can start creating surfaces on import
pygame.init()
pygame.display.set_caption('Valley')
screen = pygame.display.set_mode((840, 600))
clock = pygame.time.Clock()

# Initialize UI engine so scenes don't have to
import asset_manager
import suie
from scenes import *
suie.init(asset_manager.load_image('ui/suiSource.png'))

# Initialize game by creating our first game scene
first_scene = BattleScene()

while True:
    event_list = pygame.event.get()
    for event in event_list:
        if event.type == QUIT or \
                (event.type == KEYDOWN and event.key == K_ESCAPE):
            sys.exit()

    # Run update logic based on input
    elapsed_ms = clock.get_time()
    Timer.update(elapsed_ms)
    GameScene.update_current(event_list, elapsed_ms)

    # Draw loop
    screen.fill((0, 0, 0))
    GameScene.draw_current(screen)

    pygame.display.flip()

    # Set frame rate
    clock.tick(60)
