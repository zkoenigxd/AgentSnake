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
        self.speed = .5  # input processes per second
        self.last_input_process = 0
        rows = 9
        cols = 16
        self.game = SnakeGameLogic.SnakeGame("hamiltonian", rows, cols)
        self.restart_button = None
        self.mouse_down_previous = False
        
        # Initialize the Hamiltonian path
        self.hamiltonian_path = None
        self.current_path_index = 0
        self.food_position = None
        self.graph = None
        
        # Initialize the graph and path
        self.graph = gh.array_to_graph(self.game.state_arr)
        self.hamiltonian_path = ham.find_hamiltonian_cycle_in_grid(rows, cols)
    
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
        if self.game != None:
            if self.game.is_dead == True:
                self.end_game(screen)
            else:
                screen.fill("black")
                # Draw the game grid
                for x, row in enumerate(self.game.state_arr):
                    for y, block in enumerate(row):
                        if block == BlockState.Snake:
                            pygame.draw.rect(screen, "white", pygame.Rect(y * block_size, x * block_size,block_size,block_size), 0, 3)
                        if block == BlockState.Food:
                            pygame.draw.rect(screen, "red", pygame.Rect(y * block_size, x * block_size,block_size,block_size), 0, 3)
                        if block == BlockState.Obsticle:
                            pygame.draw.rect(screen, "green", pygame.Rect(y * block_size, x * block_size,block_size,block_size), 0, 3)
                
                # Optionally visualize the Hamiltonian path
                self.visualize_path(screen)
                
                # Display game stats
                font = pygame.font.SysFont("Arial", 24)
                score_text = font.render(f"Score: {self.game.score}", True, (255, 255, 255))
                time_text = font.render(f"Time: {self.game.get_elapsed_time():.1f}s", True, (255, 255, 255))
                high_score_text = font.render(f"High Score: {self.game.get_high_score()}", True, (255, 255, 255))
                
                # Position stats in top-left corner with 10px padding
                screen.blit(score_text, (10, 10))
                screen.blit(time_text, (10, 40))
                screen.blit(high_score_text, (10, 70))

    def visualize_path(self, screen):
        """
        Visualize the Hamiltonian path on the screen.
        """
        if not self.hamiltonian_path:
            return
            
        # Draw the path with a semi-transparent line
        for i in range(len(self.hamiltonian_path) - 1):
            start_pos = self.hamiltonian_path[i]
            end_pos = self.hamiltonian_path[i + 1]
            
            # Convert grid positions to screen coordinates
            start_x = start_pos[1] * block_size + block_size // 2
            start_y = start_pos[0] * block_size + block_size // 2
            end_x = end_pos[1] * block_size + block_size // 2
            end_y = end_pos[0] * block_size + block_size // 2
            
            # Draw a line between the points
            pygame.draw.line(screen, (0, 255, 0, 128), (start_x, start_y), (end_x, end_y), 2)

    def end_game(self: Self, screen: pygame.Surface):
        screen.fill("red")
        
        # Display game over text and stats
        font = pygame.font.SysFont("Arial", 48)
        game_over_text = font.render("Game Over", True, (255, 255, 255))
        score_text = font.render(f"Score: {self.game.score}", True, (255, 255, 255))
        time_text = font.render(f"Time: {self.game.get_elapsed_time():.1f}s", True, (255, 255, 255))
        high_score_text = font.render(f"High Score: {self.game.get_high_score()}", True, (255, 255, 255))
        total_time_text = font.render(f"Total Time: {self.game.get_total_time():.1f}s", True, (255, 255, 255))
        
        screen_width, screen_height = screen.get_size()
        game_over_rect = game_over_text.get_rect(center=(screen_width // 2, screen_height // 2 - 150))
        score_rect = score_text.get_rect(center=(screen_width // 2, screen_height // 2 - 50))
        time_rect = time_text.get_rect(center=(screen_width // 2, screen_height // 2))
        high_score_rect = high_score_text.get_rect(center=(screen_width // 2, screen_height // 2 + 50))
        total_time_rect = total_time_text.get_rect(center=(screen_width // 2, screen_height // 2 + 100))
        
        screen.blit(game_over_text, game_over_rect)
        screen.blit(score_text, score_rect)
        screen.blit(time_text, time_rect)
        screen.blit(high_score_text, high_score_rect)
        screen.blit(total_time_text, total_time_rect)
        
        # Create restart button if it doesn't exist
        if self.restart_button is None:
            self.restart_button = Button(
                label="Restart Game",
                callback=self.restart_game
            )
            
            # Position the button in the center of the screen
            button_width = 200
            button_height = 50
            x_position = (screen_width - button_width) // 2
            y_position = screen_height // 2 + 200  # Moved down to accommodate new stats
            self.restart_button.rect = pygame.Rect(x_position, y_position, button_width, button_height)
        
        # Draw the restart button
        self.restart_button.draw(screen)
        
        # Check for button clicks
        mouse_pressed = pygame.mouse.get_pressed()[0]
        if mouse_pressed and not self.mouse_down_previous:
            mouse_pos = pygame.mouse.get_pos()
            if self.restart_button.rect.collidepoint(mouse_pos):
                self.restart_button.on_click()
        self.mouse_down_previous = mouse_pressed

    def restart_game(self):
        """Reset the game when the restart button is clicked"""
        self.game.reset()
        self.last_input_process = 0
        # Recreate the Hamiltonian path for the new game state
        self.initialize_graph_and_path()

    def set_scale(self: Self, width : int):
        global block_size 
        block_size = width / self.game.cols
        