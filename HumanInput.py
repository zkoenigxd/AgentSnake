import pygame
from SnakeGameLogic import SnakeGame, InputAction

class HumanInput_SnakeGame:
    
    def get_input(context: SnakeGame):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            context.set_action(InputAction.Up)
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            context.set_action(InputAction.Down)
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            context.set_action(InputAction.Left)
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            context.set_action(InputAction.Right)

class HumanInput_PauseMenu:

    def get_input(context: None):
        if pygame.MOUSEBUTTONUP:
            mouse_press_location = pygame.mouse.get_pos()
        return mouse_press_location