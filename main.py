import pygame

# pygame setup
pygame.init()
screen_width = 1280
aspect_ratio = 9/16

screen = pygame.display.set_mode((screen_width, screen_width * aspect_ratio), pygame.RESIZABLE)
clock = pygame.time.Clock()
running = True
dt = 0

rows, cols = (45,80)
arr = [[0 for i in range(cols)] for j in range(rows)]

arr[23][40] = 1

def scale_blocks():
    return screen_width / cols

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
block_size = scale_blocks()

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.VIDEORESIZE:
            screen_width = event.w
            screen = pygame.display.set_mode((screen_width, screen_width * aspect_ratio), pygame.RESIZABLE)
            block_size = scale_blocks()

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")
    for r_index, row in enumerate(arr):
        for c_index, element in enumerate(row):
            if element == 1:
                pygame.draw.rect(screen, "white", pygame.Rect(c_index * block_size, r_index * block_size,block_size,block_size), 0, 3)

    #pygame.draw.circle(screen, "red", player_pos, 40)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player_pos.y -= 300 * dt
    if keys[pygame.K_s]:
        player_pos.y += 300 * dt
    if keys[pygame.K_a]:
        player_pos.x -= 300 * dt
    if keys[pygame.K_d]:
        player_pos.x += 300 * dt

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()