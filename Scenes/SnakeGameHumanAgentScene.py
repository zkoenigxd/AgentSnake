from .Scene import Scene
from typing import Self
import pygame
from Games import SnakeGameLogic
from Games.SnakeGameLogic import BlockState, InputAction
from Singlton import GAME_MANAGER

class SnakeGameHumanAgentScene(Scene):

    def __init__(self):
        self.speed = 10 # input processes per second
        self.last_input_process = 0
        self.game = SnakeGameLogic.SnakeGame()
    
    def collect_input(self: Self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.game.set_action(InputAction.Up)
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.game.set_action(InputAction.Down)
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.game.set_action(InputAction.Left)
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.game.set_action(InputAction.Right)
    
    def process_input(self: Self, dt: float):
        # dt is delta time in seconds since last frame, used for framerate-independent input processing.
        if dt == 0:
            self.game.process_action()
            return
        self.last_input_process += dt
        if self.last_input_process >= 1 / self.speed:
            self.last_input_process = 0
            self.game.process_action()


    def set_input_pause(context = GAME_MANAGER.scene.game):
        if pygame.MOUSEBUTTONUP:
            mouse_press_location = pygame.mouse.get_pos()
        return mouse_press_location
    
    def render_scene(self: Self, screen: pygame.Surface):
        if self.game != None:
            if self.game.is_dead == True:
                screen.fill("red")
            else:
                screen.fill("black")
                for x, row in enumerate(self.game.state_arr):
                    for y, block in enumerate(row):
                        if block == BlockState.Snake:
                            pygame.draw.rect(screen, "white", pygame.Rect(y * block_size, x * block_size,block_size,block_size), 0, 3)
                        if block == BlockState.Food:
                            pygame.draw.rect(screen, "red", pygame.Rect(y * block_size, x * block_size,block_size,block_size), 0, 3)
                        if block == BlockState.Obsticle:
                            pygame.draw.rect(screen, "green", pygame.Rect(y * block_size, x * block_size,block_size,block_size), 0, 3)

    def set_scale(self: Self, width : int):
        global block_size 
        block_size = width / self.game.cols