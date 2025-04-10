from typing import Self

class GameManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(GameManager, cls).__new__(cls)
            cls._instance.scene = None
        return cls._instance

    def initialize(self: Self, initial_scene, width = 1280) -> Self:
        if self.scene is None:  # Only initialize if not already initialized
            self.scene = initial_scene
            self.scene.set_game_manager(self)
            self.scene.set_scale(width)
        return self

    def changeScene(self: Self, scene, width = 1280):
        self.scene = scene
        self.scene.set_game_manager(self)
        self.scene.set_scale(width)
