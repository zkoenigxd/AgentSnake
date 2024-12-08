import SnakeGameLogic as gl
from typing import Self
import pygame


class RenderMode_Human:

    def __init__(self: Self, width: float, game: gl.SnakeGame) -> Self:
        self.width = width
        self.set_scale(width, game)

    def render_scene(self: Self, screen: pygame.Surface, game : gl.SnakeGame):
        if game.is_dead == True:
            screen.fill("red")
        else:
            screen.fill("black")
            for x, row in enumerate(game.state_arr):
                for y, block in enumerate(row):
                    if block == gl.BlockState.Snake:
                        pygame.draw.rect(screen, "white", pygame.Rect(y * block_size, x * block_size,block_size,block_size), 0, 3)
                    if block == gl.BlockState.Food:
                        pygame.draw.rect(screen, "red", pygame.Rect(y * block_size, x * block_size,block_size,block_size), 0, 3)
                    if block == gl.BlockState.Obsticle:
                        pygame.draw.rect(screen, "green", pygame.Rect(y * block_size, x * block_size,block_size,block_size), 0, 3)

    def set_scale(self: Self, width : int, game : gl.SnakeGame):
        global block_size 
        block_size = width / game.cols