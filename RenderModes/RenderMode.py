import Games.SnakeGameLogic as gl
from typing import Self
import pygame

class RenderMode:
    def __init__(self):
        raise NotImplementedError
    
    def render_scene(self, screen, context):
        raise NotImplementedError
    
    def set_scale(self, width: float, game: gl.SnakeGame):
        raise NotImplementedError