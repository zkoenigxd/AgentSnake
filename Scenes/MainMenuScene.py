from .Scene import Scene
from typing import Self
import pygame
from UI.Button import Button
from Singlton import GAME_MANAGER

class MainMenuScene(Scene):
    def __init__(self):
        self.buttons = []
        self.mouse_down_previous = False
        # For rendering, "self.game" is set to self so that RenderMode_Human.render_scene(screen, self.game) calls our draw method.
        self.game = self  
        # Global GameManager should be set via set_game_manager (or be accessed via a global import).
        self.game_manager = GAME_MANAGER

        # Create 4 buttons.
        # Each button is given a broadcast value that could indicate which scene to switch to.
        for i in range(4):
            broadcast_value = f"Scene{i+1}"
            # Here we don’t specify a direct callback; instead we subscribe with a handler.
            button = Button(
                label=f"Sample Button {i+1}",
                broadcast_value=broadcast_value
            )
            # Subscribe MainMenuScene's event handler to the button.
            button.subscribe(self.handle_button_event)
            self.buttons.append(button)

    def handle_button_event(self, event_data):
        """
        Handles button events. The event_data (broadcast by the button) can be used
        to decide which scene to transition to.
        In this demo, if the event_data is "Scene1", we change to the Snake game scene.
        """
        print(f"Button event received with data: {event_data}")
        if self.game_manager is not None:
            # For demonstration, we are only reacting to "Scene1". You may extend this logic.
            if event_data == "Scene1":
                from Scenes import SnakeGameHumanAgentScene as gs
                new_scene = gs.SnakeGameHumanAgentScene()
                self.game_manager.changeScene(new_scene)
            else:
                print("No associated scene for event:", event_data)
        else:
            print("GameManager reference not set in MainMenuScene.")

    def update_layout(self, screen):
        """
        Recalculates button positions and sizes based on the current window dimensions.
        Buttons are arranged in a row with a constant margin.
        """
        window_width, window_height = screen.get_size()
        num_buttons = len(self.buttons)
        margin = 20  # Margin between buttons and edges.
        total_margin = margin * (num_buttons + 1)
        available_width = window_width - total_margin
        button_width = available_width // num_buttons if num_buttons > 0 else 0
        # Use 1/10 of the window height for the button height.
        button_height = window_height // 10
        y_position = window_height // 2 - button_height // 2

        for idx, button in enumerate(self.buttons):
            x_position = margin + idx * (button_width + margin)
            button.rect = pygame.Rect(x_position, y_position, button_width, button_height)

    def render_scene(self, screen):
        """Draws the main menu including background and buttons."""
        screen.fill((0, 0, 0))  # Clear screen with black.
        self.update_layout(screen)
        for button in self.buttons:
            button.draw(screen)

    def collect_input(self, context = GAME_MANAGER.scene):
        """Polls input: upon a fresh left mouse click, checks buttons for a hit and calls on_click()."""
        mouse_pressed = pygame.mouse.get_pressed()[0]
        if mouse_pressed and not self.mouse_down_previous:
            mouse_pos = pygame.mouse.get_pos()
            for button in self.buttons:
                if button.rect.collidepoint(mouse_pos):
                    button.on_click()  # Trigger the button's event.
        self.mouse_down_previous = mouse_pressed

    def process_input(self, dt: float, context = GAME_MANAGER.scene):
        """No time-dependent processing is needed for the main menu."""
        pass

    def set_scale(self: Self, width : int):
        pass