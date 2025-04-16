from .Scene import Scene
from typing import Self
import pygame
from Games import SnakeGameLogic
from Games.SnakeGameLogic import BlockState, InputAction
from Singlton import GAME_MANAGER
from UI.Button import Button
import GraphHelperFunctions.ArrayToGraph as gh
import GraphHelperFunctions.Hamiltonian as ham

class SnakeGameHamiltonianPathAgentScene(Scene):

    def __init__(self):
        self.speed = 10  # input processes per second
        self.last_input_process = 0
        self.rows = 26
        self.cols = 32
        self.game = SnakeGameLogic.SnakeGame("hamiltonian", self.rows, self.cols)
        self.restart_button = None
        self.main_menu_button = None
        self.speed_increase_button = None
        self.speed_decrease_button = None
        self.mouse_down_previous = False
        self.game_manager = GAME_MANAGER
        
        # Initialize the Hamiltonian path
        self.hamiltonian_path = None
        self.current_path_index = 0
        self.graph = None
        
        # Initialize the graph and path
        self.graph = gh.array_to_graph(self.game.state_arr)
        self.hamiltonian_path = ham.find_hamiltonian_cycle(self.rows, self.cols)

    def initialize_graph_and_path(self):
        self.last_input_process = 0
        self.restart_button = None
        self.mouse_down_previous = False
        
        # Initialize the Hamiltonian path
        self.current_path_index = 0
        
        # Initialize the graph and path
        self.graph = gh.array_to_graph(self.game.state_arr)
        self.hamiltonian_path = ham.find_hamiltonian_cycle(self.rows, self.cols)
    
    def get_next_action(self):
        """
        Determine the next action based on the current position and the Hamiltonian cycle.
        """
        current_pos = self.game.head_location

        # Ensure that we have a valid cycle.
        if not self.hamiltonian_path or len(self.hamiltonian_path) == 0:
            return None

        # Wrap-around indexing since it's a cycle:
        next_index = (self.current_path_index + 1) % len(self.hamiltonian_path)
        next_pos = self.hamiltonian_path[next_index]
        
        # Calculate the differences in row and column between the current and next positions.
        row_diff = next_pos[0] - current_pos[0]
        col_diff = next_pos[1] - current_pos[1]
        
        # Map the directional differences to an action.
        if row_diff == -1 and col_diff == 0:
            return InputAction.Up
        elif row_diff == 1 and col_diff == 0:
            return InputAction.Down
        elif row_diff == 0 and col_diff == 1:
            return InputAction.Right
        elif row_diff == 0 and col_diff == -1:
            return InputAction.Left
        else:
            return None    
    
    def is_valid_move(self, pos):
        """
        Check if a move to the given position is valid.
        """
        # Check if the position is within bounds
        if (pos[0] < 0 or pos[0] >= self.game.rows or 
            pos[1] < 0 or pos[1] >= self.game.cols):
            return False
        
        # Check if the position is empty or contains food
        state = self.game.state_arr[pos[0]][pos[1]]
        return state == BlockState.Empty or state == BlockState.Food
    
    def collect_input(self: Self):
        # No need to collect input as the agent controls the snake
        pass
    
    def process_input(self: Self, dt: float):
        # Skip processing if already dead
        if self.game.is_dead:
            return
        
        # Process input at the specified speed
        if dt == 0:
            self.process_game_step()
            return
            
        self.last_input_process += dt
        if self.last_input_process >= 1 / self.speed:
            self.last_input_process = 0
            self.process_game_step()

        # Check for button clicks.
        mouse_pressed = pygame.mouse.get_pressed()[0]
        if mouse_pressed and not self.mouse_down_previous:
            mouse_pos = pygame.mouse.get_pos()
            if self.main_menu_button is not None and self.main_menu_button.rect.collidepoint(mouse_pos):
                self.main_menu_button.on_click()
            if self.speed_decrease_button is not None and self.speed_decrease_button.rect.collidepoint(mouse_pos):
                self.speed_decrease_button.on_click()
            if self.speed_increase_button is not None and self.speed_increase_button.rect.collidepoint(mouse_pos):
                self.speed_increase_button.on_click()
        self.mouse_down_previous = mouse_pressed
    
    def process_game_step(self):
        """
        Process one step of the game, updating the snake's position and the graph.
        """
        # Ensure the graph is initialized.
        if self.graph is None:
            self.initialize_graph_and_path()
        
        # Get the next action from the Hamiltonian cycle.
        next_action = self.get_next_action()
        if next_action is not None:
            self.game.set_action(next_action)
        else:
            # You might decide what to do here if no valid action is found.
            print("No valid next action found!")
        
        # Process the action.
        self.game.process_action()
        
        # Update the current path index:
        # Try to match the snake's head position with a node in the Hamiltonian cycle.
        if self.hamiltonian_path:
            for i, pos in enumerate(self.hamiltonian_path):
                if pos == self.game.head_location:
                    self.current_path_index = i
                    break
    
    def render_scene(self: Self, screen: pygame.Surface):
        if self.game is not None:
            if self.game.is_dead:
                self.end_game(screen)
            else:
                # Fill the background.
                screen.fill("black")
                
                # --- Define the grid drawing area ---
                # These offsets ensure that the grid is not drawn at the very edge,
                # leaving room for a border and score readouts.
                game_offset_x = 10
                game_offset_y = 10
                game_width = self.game.cols * block_size
                game_height = self.game.rows * block_size
                
                # --- Draw the grid blocks ---
                # Adjust each block's position based on the game area offsets.
                for x, row in enumerate(self.game.state_arr):
                    for y, block in enumerate(row):
                        rect = pygame.Rect(
                            game_offset_x + y * block_size,
                            game_offset_y + x * block_size,
                            block_size,
                            block_size
                        )
                        if block == BlockState.Snake:
                            pygame.draw.rect(screen, "white", rect, 0, 3)
                        elif block == BlockState.Food:
                            pygame.draw.rect(screen, "red", rect, 0, 3)
                        elif block == BlockState.Obsticle:
                            pygame.draw.rect(screen, "green", rect, 0, 3)

                self.visualize_path(screen)
                
                # --- Draw a border around the grid ---
                # The border is drawn with a padding so it doesn't overlap the grid blocks.
                border_padding = 5  # adjust as needed
                border_rect = pygame.Rect(
                    game_offset_x - border_padding,
                    game_offset_y - border_padding,
                    game_width + 2 * border_padding,
                    game_height + 2 * border_padding
                )
                pygame.draw.rect(screen, "white", border_rect, 3)
                
                # --- Draw the score readouts outside the grid ---
                # Here, we choose to render the score information below the grid.
                stats_offset_y = game_offset_y + game_height + 10
                font = pygame.font.SysFont("Arial", 24)
                score_text = font.render(f"Score: {self.game.score}", True, (255, 255, 255))
                time_text = font.render(f"Time: {self.game.get_elapsed_time():.1f}s", True, (255, 255, 255))
                high_score_text = font.render(f"High Score: {self.game.get_high_score()}", True, (255, 255, 255))
                
                screen.blit(score_text, (game_offset_x, stats_offset_y))
                screen.blit(time_text, (game_offset_x, stats_offset_y + 30))
                screen.blit(high_score_text, (game_offset_x, stats_offset_y + 60))

                button_width = 200
                button_height = 50
                menu_x = game_offset_x + game_width - button_width
                menu_y = game_offset_y + game_height + 10
                menu_y = stats_offset_y
                if self.main_menu_button is None:
                    self.main_menu_button = Button(
                        label="Main Menu",
                        callback=self.load_main_menu
                    )
                #self.main_menu_button.rect = pygame.Rect(game_width - game_offset_x, menu_y, button_width, button_height)
                self.main_menu_button.rect = pygame.Rect(menu_x, menu_y, button_width, button_height)
                self.main_menu_button.draw(screen)

                # --- Place the Speed Control Buttons Below the Main Menu Button ---
            # Define a small gap between rows.
            vertical_gap = 10
            speed_buttons_y = menu_y + button_height + vertical_gap
            
            # We'll arrange two buttons in a single row. Their total width equals the Main Menu button's width.
            speed_button_margin = 10  # gap between the two speed buttons
            speed_button_width = (button_width - speed_button_margin) // 2
            speed_button_height = button_height
            
            # Left button: decrease speed ("Slow")
            if self.speed_decrease_button is None:
                self.speed_decrease_button = Button(
                    label="Slow",
                    callback=self.decrease_speed
                )
            speed_decrease_x = menu_x  # left column of the two-speed buttons
            self.speed_decrease_button.rect = pygame.Rect(speed_decrease_x, speed_buttons_y, speed_button_width, speed_button_height)
            self.speed_decrease_button.draw(screen)
            
            # Right button: increase speed ("Fast")
            if self.speed_increase_button is None:
                self.speed_increase_button = Button(
                    label="Fast",
                    callback=self.increase_speed
                )
            speed_increase_x = menu_x + speed_button_width + speed_button_margin
            self.speed_increase_button.rect = pygame.Rect(speed_increase_x, speed_buttons_y, speed_button_width, speed_button_height)
            self.speed_increase_button.draw(screen)
            
    def decrease_speed(self):
        """
        Decrease the game speed, but do not let it go below a minimum value.
        """
        # Decrease speed by 5 (or any step you choose), ensuring a minimum of 5.
        self.speed = max(1, self.speed - 5)
        print(f"Speed decreased to {self.speed}")

    def increase_speed(self):
        """
        Increase the game speed.
        """
        # Increase speed by 5.
        self.speed = min(200, self.speed + 5)
        print(f"Speed increased to {self.speed}")

    def visualize_path(self, screen):
        """
        Visualize the Hamiltonian path on the screen,
        drawing it centered relative to the grid.
        """
        if not self.hamiltonian_path:
            return

        # Use the same offsets as in render_scene.
        game_offset_x = 10
        game_offset_y = 10

        # Draw the path with a green line.
        for i in range(len(self.hamiltonian_path) - 1):
            start_pos = self.hamiltonian_path[i]
            end_pos = self.hamiltonian_path[i + 1]

            # Convert grid positions to screen coordinates, adding the offsets.
            start_x = game_offset_x + start_pos[1] * block_size + block_size // 2
            start_y = game_offset_y + start_pos[0] * block_size + block_size // 2
            end_x = game_offset_x + end_pos[1] * block_size + block_size // 2
            end_y = game_offset_y + end_pos[0] * block_size + block_size // 2

            pygame.draw.line(screen, (0, 255, 0), (start_x, start_y), (end_x, end_y), 2)

    def end_game(self: Self, screen: pygame.Surface):
        # Fill the background with a solid color.
        screen.fill("red")
        
        # Obtain screen dimensions.
        screen_width, screen_height = screen.get_size()
        
        # Display game over text and stats in the upper half of the screen.
        font = pygame.font.SysFont("Arial", 48)
        game_over_text = font.render("Game Over", True, (255, 255, 255))
        font_small = pygame.font.SysFont("Arial", 24)
        score_text = font_small.render(f"Score: {self.game.score}", True, (255, 255, 255))
        time_text = font_small.render(f"Time: {self.game.get_elapsed_time():.1f}s", True, (255, 255, 255))
        high_score_text = font_small.render(f"High Score: {self.game.get_high_score()}", True, (255, 255, 255))
        total_time_text = font_small.render(f"Total Time: {self.game.get_total_time():.1f}s", True, (255, 255, 255))
        
        # Center the game over text near the top half.
        game_over_rect = game_over_text.get_rect(center=(screen_width // 2, screen_height // 2 - 150))
        screen.blit(game_over_text, game_over_rect)
        
        # Place the stats below the "Game Over" text but away from the game area.
        stats_y = game_over_rect.bottom + 10
        screen.blit(score_text, (screen_width // 2 - score_text.get_width() // 2, stats_y))
        screen.blit(time_text, (screen_width // 2 - time_text.get_width() // 2, stats_y + 40))
        screen.blit(high_score_text, (screen_width // 2 - high_score_text.get_width() // 2, stats_y + 80))
        screen.blit(total_time_text, (screen_width // 2 - total_time_text.get_width() // 2, stats_y + 120))

        # --- Create/reset buttons with updated positions ---
        # Restart Button:
        button_width = 200
        button_height = 50
        window_width, window_height = screen.get_size()
        y_position = window_height // 1.5 - button_height // 2
        restart_x = (screen_width - button_width) // 2
        # Position the restart button below the stats.
        restart_y = y_position
        if self.restart_button is None:
            self.restart_button = Button(
                label="Restart Game",
                callback=self.restart_game
            )
        self.restart_button.rect = pygame.Rect(restart_x, restart_y, button_width, button_height)
        
        # Main Menu Button:
        menu_y = restart_y + button_height + 10  # position below the restart button
        if self.main_menu_button is None:
            self.main_menu_button = Button(
                label="Main Menu",
                callback=self.load_main_menu
            )
        self.main_menu_button.rect = pygame.Rect(restart_x, menu_y, button_width, button_height)
        
        # Draw the buttons.
        self.restart_button.draw(screen)
        self.main_menu_button.draw(screen)
        
        # Check for button clicks.
        mouse_pressed = pygame.mouse.get_pressed()[0]
        if mouse_pressed and not self.mouse_down_previous:
            mouse_pos = pygame.mouse.get_pos()
            if self.restart_button.rect.collidepoint(mouse_pos):
                self.restart_button.on_click()
            if self.main_menu_button.rect.collidepoint(mouse_pos):
                self.main_menu_button.on_click()
        self.mouse_down_previous = mouse_pressed

    def restart_game(self):
        """Reset the game when the restart button is clicked"""
        self.game.reset()
        self.last_input_process = 0
        # Recreate the Hamiltonian path for the new game state
        self.initialize_graph_and_path()

    def load_main_menu(self):
        from Scenes import MainMenuScene as mm
        new_scene = mm.MainMenuScene()
        self.game_manager.changeScene(new_scene)

    def set_scale(self: Self, width : int):
        global block_size 
        block_size = (width - 20) / self.game.cols
        