import pygame
import game_logic as gl

def get_block_scale(game_instance : gl.SnakeGame):
    return screen_width / game_instance.cols

# pygame setup
pygame.init()
screen_width = 1280
aspect_ratio = 9/16
screen = pygame.display.set_mode((screen_width, screen_width * aspect_ratio), pygame.RESIZABLE)
clock = pygame.time.Clock()
running = True
dt = 0
speed = 10 # input processes per second
last_process = 0

game = gl.SnakeGame()
block_size = get_block_scale(game)

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.VIDEORESIZE:
            screen_width = event.w
            screen = pygame.display.set_mode((screen_width, screen_width * aspect_ratio), pygame.RESIZABLE)
            block_size = get_block_scale(game)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] or keys[pygame.K_UP]:
        game.set_action(gl.InputAction.Up)
    if keys[pygame.K_s] or keys[pygame.K_DOWN]:
        game.set_action(gl.InputAction.Down)
    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        game.set_action(gl.InputAction.Left)
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        game.set_action(gl.InputAction.Right)

    last_process += dt
    if last_process >= 1 / speed:
        game.process_action()
        last_process = 0
    
    # fill the screen with a color to wipe away anything from last frame
    if game.is_dead == True:
        screen.fill("red")
    else:
        screen.fill("black")
        for r_index, row in enumerate(game.state_arr):
            for c_index, element in enumerate(row):
                if element == gl.BlockState.Snake:
                    pygame.draw.rect(screen, "white", pygame.Rect(c_index * block_size, r_index * block_size,block_size,block_size), 0, 3)
                if element == gl.BlockState.Food:
                    pygame.draw.rect(screen, "red", pygame.Rect(c_index * block_size, r_index * block_size,block_size,block_size), 0, 3)
                if element == gl.BlockState.Obsticle:
                    pygame.draw.rect(screen, "green", pygame.Rect(c_index * block_size, r_index * block_size,block_size,block_size), 0, 3)
    


    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()