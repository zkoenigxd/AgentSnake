import pygame
import SnakeGameLogic as gl
import SnakeGameHumanAgentScene as gs
from RenderMode import RenderMode_Human

# pygame setup
pygame.init()
screen_width = 1280
aspect_ratio = 9/16
screen = pygame.display.set_mode((screen_width, screen_width * aspect_ratio), pygame.RESIZABLE)
clock = pygame.time.Clock()
running = True
dt = 0

game = gl.SnakeGame()
render_mode = RenderMode_Human(1280, game)
scene = gs.SnakeGameHumanAgentScene()

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.VIDEORESIZE:
            screen_width = event.w
            screen = pygame.display.set_mode((screen_width, screen_width * aspect_ratio), pygame.RESIZABLE)
            render_mode.set_scale(screen_width)
    
    scene.collect_input(game)
    scene.process_input(dt, game)
    render_mode.render_scene(screen, game)

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()