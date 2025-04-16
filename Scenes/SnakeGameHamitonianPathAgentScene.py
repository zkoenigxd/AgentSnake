from .Scene import Scene
from typing import Self
import pygame
from Games import SnakeGameLogic
from Games.SnakeGameLogic import SnakeGame, InputAction

class SnakeGameHumanAgentScene(Scene):

    def __init__(self):
        self.game = SnakeGameLogic.SnakeGame()
        self.path = createHamiltonianPath(self.game)
    
    def collect_input(self: Self, context: SnakeGame):
        nextState = self.path[location]
        context.set_action(nextState)
    
    def process_input(self: Self, dt: float, context):
        if dt == 0:
            context.process_action()
            return
        self.last_input_process += dt
        if self.last_input_process >= 1 / self.speed:
            self.last_input_process = 0
            context.process_action()
    
    def createHamiltonianPath(stateArr):
        path = stateArr
        #TODO: create a path that doesn't cross itself
        return path
        