import Games.SnakeGameLogic as gl
from Scenes import SnakeGameHumanAgentScene as gs
from RenderMode import RenderMode_Human
from typing import Self

class GameManager:

    def __init__(self: Self) -> Self:
        self.game = gl.SnakeGame()
        self.render_mode = RenderMode_Human(1280, self.game)
        self.scene = gs.SnakeGameHumanAgentScene()