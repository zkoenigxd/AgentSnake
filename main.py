import pygame
from Singlton import GAME_MANAGER
import Scenes.MainMenuScene as startScene

# pygame setup
pygame.init()
pygame.font.init()  # Ensure the font module is initialized
screen_width = 1280
aspect_ratio = 9/16
screen = pygame.display.set_mode((screen_width, screen_width * aspect_ratio), pygame.RESIZABLE)
clock = pygame.time.Clock()

# Initialize the game manager with the main menu scene
GAME_MANAGER.initialize(startScene.MainMenuScene(), screen_width)

running = True
dt = 0

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.VIDEORESIZE:
            screen_width = event.w
            screen = pygame.display.set_mode((screen_width, screen_width * aspect_ratio), pygame.RESIZABLE)
            GAME_MANAGER.scene.set_scale(screen_width)
    
    GAME_MANAGER.scene.collect_input()
    GAME_MANAGER.scene.process_input(dt)
    GAME_MANAGER.scene.render_scene(screen)

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()