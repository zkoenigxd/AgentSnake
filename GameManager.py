from typing import Self

default_screen_width = 600

class GameManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(GameManager, cls).__new__(cls)
            cls._instance.scene = None
        return cls._instance

    def initialize(self: Self, initial_scene, width = default_screen_width) -> Self:
        if self.scene is None:  # Only initialize if not already initialized
            self.scene = initial_scene
            self.scene.set_game_manager(self)
            self.scene.set_scale(width)
        return self

    def changeScene(self: Self, scene, width = default_screen_width):
        self.scene = scene
        self.scene.set_game_manager(self)
        self.scene.set_scale(width)
