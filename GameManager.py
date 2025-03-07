import Games.SnakeGameLogic as gl
from Scenes import SnakeGameHumanAgentScene as gs
from RenderMode import RenderMode_Human
from typing import Self

class GameManager:

    def __init__(self: Self) -> Self:
        self.scene = gs.SnakeGameHumanAgentScene()
        self.render_mode = RenderMode_Human(1280, self.scene.game)

    def changeScene(self: Self, game, renderMode, scene):
        self.render_mode = renderMode
        self.scene = scene