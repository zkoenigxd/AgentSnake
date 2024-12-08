from typing import Self
import pygame
from SnakeGameLogic import SnakeGame, InputAction

class SnakeGameHumanAgentScene:

    def __init__(self):
        self.speed = 10 # input processes per second
        self.last_input_process = 0
    
    def collect_input(self: Self, context: SnakeGame):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            context.set_action(InputAction.Up)
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            context.set_action(InputAction.Down)
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            context.set_action(InputAction.Left)
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            context.set_action(InputAction.Right)
    
    def process_input(self: Self, dt: float, context):
        if dt == 0:
            context.process_action()
            return
        self.last_input_process += dt
        if self.last_input_process >= 1 / self.speed:
            self.last_input_process = 0
            context.process_action()


    def set_input_pause(context: None):
        if pygame.MOUSEBUTTONUP:
            mouse_press_location = pygame.mouse.get_pos()
        return mouse_press_location