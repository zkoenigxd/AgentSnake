from .Scene import Scene
from typing import List, Tuple, Dict, Set, Self
from queue import PriorityQueue
import pygame
from Games import SnakeGameLogic
from Games.SnakeGameLogic import SnakeGame, InputAction, BlockState
from UI.Button import Button  # Add this import

class SnakeGameAStarAgentScene(Scene):
    def __init__(self):
        self.grid_size = 20  # Default grid size
        self.game = SnakeGameLogic.SnakeGame(save_id="a_star_agent")
        self.path = []
        self.tail_position = None
        self.last_input_process = 0
        self.speed = 10
        self.mouse_down_previous = False
        self.main_menu_button = None
        self.speed_increase_button = None
        self.speed_decrease_button = None
        self.restart_button = None
        # Initialize for the first path
        self.create_path()
    
    def collect_input(self):
        """Determines next move and sets the action based on the current path"""
        # Always try to create a new path
        self.create_path()  # Remove the if not self.path condition to recalculate path every time
        
        # If we have a path, follow it
        if self.path:
            head = self.game.head_location
            current_pos = head
            for i, next_pos in enumerate(self.path[1:], 1):
                if current_pos == self.path[i-1]:
                    dx = next_pos[0] - current_pos[0]
                    dy = next_pos[1] - current_pos[1]
                    
                    if dx == 1:
                        self.game.set_action(InputAction.Down)
                    elif dx == -1:
                        self.game.set_action(InputAction.Up)
                    elif dy == 1:
                        self.game.set_action(InputAction.Right)
                    elif dy == -1:
                        self.game.set_action(InputAction.Left)
                    break

    def process_input(self, dt: float):
        if dt == 0:
            self.game.process_action()
            return
        self.last_input_process += dt
        if self.last_input_process >= 1 / self.speed:
            self.last_input_process = 0
            self.game.process_action()
            # Update tail position if we don't have one yet
            if self.tail_position is None:
                self.tail_position = self.game.tail_locations[0]
        
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

    def create_path(self) -> List[Tuple[int, int]]:
        """Creates a path using A* pathfinding"""
        head_pos = self.game.head_location
        food_pos = self.find_food_position()
        
        if not food_pos:
            return []
            
        path = self.find_path_to_food(head_pos, food_pos)
        if not path:
            # If no path to food, find a path to tail
            path = self.find_path_to_tail(head_pos)
            if not path:
                # If no safe path exists, just keep going!
                return []
        
        self.path = path
        return path

    def find_path_to_food(self, start: Tuple[int, int], goal: Tuple[int, int]) -> List[Tuple[int, int]]:
        """A* pathfinding to food"""
        frontier = PriorityQueue()
        frontier.put((0, start))
        came_from = {start: None}
        cost_so_far = {start: 0}

        while not frontier.empty():
            current = frontier.get()[1]
            if current == goal:
                break

            for next_pos in self.get_valid_neighbors(current):
                new_cost = cost_so_far[current] + 1
                if next_pos not in cost_so_far or new_cost < cost_so_far[next_pos]:
                    cost_so_far[next_pos] = new_cost
                    priority = new_cost + self.manhattan_distance(next_pos, goal)
                    frontier.put((priority, next_pos))
                    came_from[next_pos] = current

        return self.reconstruct_path(came_from, start, goal)

    def find_path_to_tail(self, start: Tuple[int, int]) -> List[Tuple[int, int]]:
        """Find path to the snake's tail"""
        tail_pos = self.game.tail_locations[0] if self.game.tail_locations else None
        if not tail_pos:
            return []
        return self.find_path_to_food(start, tail_pos)  # Reuse A* but with tail as goal

    def get_valid_neighbors(self, pos: Tuple[int, int]) -> List[Tuple[int, int]]:
        """Get valid neighboring positions"""
        neighbors = []
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:  # right, down, left, up
            new_x, new_y = pos[0] + dx, pos[1] + dy
            
            # Check boundaries
            if new_x < 0 or new_x >= self.game.rows or new_y < 0 or new_y >= self.game.cols:
                continue
            
            # Check collisions with snake or obstacles
            # Don't count tail piece as collision since it will move
            if self.game.state_arr[new_x][new_y] == BlockState.Snake:
                # If this is the tail and we're not eating food, we can move here
                if (new_x, new_y) == self.game.tail_locations[0] and not self.path:
                    neighbors.append((new_x, new_y))
            elif self.game.state_arr[new_x][new_y] != BlockState.Obsticle:
                neighbors.append((new_x, new_y))
                
        return neighbors

    def manhattan_distance(self, pos1: Tuple[int, int], pos2: Tuple[int, int]) -> int:
        """Calculate Manhattan distance between two points"""
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

    def reconstruct_path(self, came_from: Dict, start: Tuple[int, int], goal: Tuple[int, int]) -> List[Tuple[int, int]]:
        """Reconstruct path from came_from dictionary"""
        if goal not in came_from:
            return []
            
        current = goal
        path = []
        while current is not None:
            path.append(current)
            current = came_from.get(current)  # Use get to handle when current is not in came_from
        path.reverse()
        return path

    def find_food_position(self) -> Tuple[int, int]:
        """Find food position by scanning game state array"""
        for row in range(self.game.rows):
            for col in range(self.game.cols):
                if self.game.state_arr[row][col] == BlockState.Food:
                    return (row, col)
        return None

    def set_scale(self, width: int):
        global block_size
        block_size = (width - 20) / self.game.cols

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
        if not self.path:
            return

        # Use the same offsets as in render_scene.
        game_offset_x = 10
        game_offset_y = 10

        # Draw the path with a green line.
        for i in range(len(self.path) - 1):
            start_pos = self.path[i]
            end_pos = self.path[i + 1]

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

    def load_main_menu(self):
        from Scenes import MainMenuScene as mm
        new_scene = mm.MainMenuScene()
        self.game_manager.changeScene(new_scene)

    def restart_game(self):
        """Reset the game when the restart button is clicked"""
        self.game.reset()
        self.path = []
        self.last_input_process = 0
        self.tail_position = None