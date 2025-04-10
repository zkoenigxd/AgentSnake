from RenderMode import RenderMode_Human
from typing import Self

class GameManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(GameManager, cls).__new__(cls)
            cls._instance.scene = None
            cls._instance.render_mode = None
        return cls._instance

    def initialize(self: Self, initial_scene) -> Self:
        if self.scene is None:  # Only initialize if not already initialized
            self.scene = initial_scene
            self.render_mode = RenderMode_Human(1280, self.scene.game)
            self.scene.set_game_manager()
        return self

    def changeScene(self: Self, game, renderMode, scene):
        self.render_mode = renderMode
        self.scene = scene