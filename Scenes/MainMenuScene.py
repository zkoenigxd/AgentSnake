from .Scene import Scene
from typing import Self
import pygame
from UI.Button import Button
from Singlton import GAME_MANAGER

class MainMenuScene(Scene):
    def __init__(self):
        self.buttons = []
        self.mouse_down_previous = False
        self.game = self
        self.game_manager = GAME_MANAGER

        # Create "snake game with human agent" button.
        human_agent_button = Button(
            label="Human Agent"
        )
        human_agent_button.subscribe(self.load_snake_game_human_agent)
        self.buttons.append(human_agent_button)

        # Create "snake game with hamiltonian path agent" button.
        hamiltonian_path_button = Button(
            label="Hamiltonian Path Agent"
        )
        hamiltonian_path_button.subscribe(self.load_snake_game_hamiltonian_path_agent)
        self.buttons.append(hamiltonian_path_button)

        # Create "A*" button.
        a_star_button = Button(
            label="A* Path Agent"
        )
        a_star_button.subscribe(self.load_snake_game_a_star_agent)
        self.buttons.append(a_star_button)

        # Create "snake game with reinforcement learning agent" button.
        rl_agent_button = Button(
            label="Reinforcement Learning Agent"
        )
        rl_agent_button.subscribe(self.load_snake_game_rl_agent)
        self.buttons.append(rl_agent_button)


    def load_snake_game_human_agent(self):
        from Scenes import SnakeGameHumanAgentScene as gs
        new_scene = gs.SnakeGameHumanAgentScene()
        self.game_manager.changeScene(new_scene)
    
    def load_snake_game_hamiltonian_path_agent(self):
        from Scenes import SnakeGameHamiltonianPathAgentScene as gs
        new_scene = gs.SnakeGameHamiltonianPathAgentScene()
        self.game_manager.changeScene(new_scene)


    def load_snake_game_a_star_agent(self):
        from Scenes import SnakeGameAStarAgentScene as gs
        new_scene = gs.SnakeGameAStarAgentScene()
        self.game_manager.changeScene(new_scene)

    def load_snake_game_rl_agent(self):
        from Scenes import SnakeGameRLAgent as rl
        new_scene = rl.SnakeGameRLAgent()
        self.game_manager.changeScene(new_scene)

    def update_layout(self, screen):
        """
        Recalculates button positions based on a grid layout with two columns per row.
        If the number of buttons is odd, the extra button is placed on the left.
        """
        import math
        window_width, window_height = screen.get_size()
        num_buttons = len(self.buttons)
        columns = 2
        rows = math.ceil(num_buttons / columns)
        
        # Define a margin (space between buttons and window edges)
        margin = 20
        
        # Compute available width and height for the button grid.
        # Here we assume the grid spans nearly the whole window minus fixed margins.
        available_width = window_width - 2 * margin  # left/right margin
        available_height = window_height - 2 * margin  # top/bottom margin
        
        # Compute each button's width and height.
        # Also include additional horizontal spacing (margin between columns).
        button_width = (available_width - margin * (columns - 1)) // columns
        button_height = min(100, (available_height - margin * (rows - 1)) // rows)
        
        # Position each button in the grid.
        for idx, button in enumerate(self.buttons):
            row_index = idx // columns
            col_index = idx % columns
            x_position = margin + col_index * (button_width + margin)
            y_position = margin + row_index * (button_height + margin)
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