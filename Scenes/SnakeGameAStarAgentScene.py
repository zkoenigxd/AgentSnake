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
        """Sets the scale/size of the game based on window width."""
        global block_size  # Add this line
        block_size = width / self.game.cols  # Match human agent scene's scaling
        self.grid_size = block_size

    def render_scene(self, screen):
        if self.game is not None:
            if self.game.is_dead:
                self.end_game(screen)
            else:
                screen.fill("black")
                # Draw based on state array
                for x, row in enumerate(self.game.state_arr):
                    for y, block in enumerate(row):
                        if block == BlockState.Snake:
                            pygame.draw.rect(screen, "white", pygame.Rect(y * block_size, x * block_size, block_size, block_size), 0, 3)
                        if block == BlockState.Food:
                            pygame.draw.rect(screen, "red", pygame.Rect(y * block_size, x * block_size, block_size, block_size), 0, 3)
                        if block == BlockState.Obsticle:
                            pygame.draw.rect(screen, "green", pygame.Rect(y * block_size, x * block_size, block_size, block_size), 0, 3)

                # Display game stats like the human agent scene
                font = pygame.font.SysFont("Arial", 24)
                score_text = font.render(f"Score: {self.game.score}", True, (255, 255, 255))
                time_text = font.render(f"Time: {self.game.get_elapsed_time():.1f}s", True, (255, 255, 255))
                high_score_text = font.render(f"High Score: {self.game.get_high_score()}", True, (255, 255, 255))
                
                screen.blit(score_text, (10, 10))
                screen.blit(time_text, (10, 40))
                screen.blit(high_score_text, (10, 70))

    def end_game(self, screen):
        """Handle game over state"""
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
        
        # Create restart button if needed
        if not hasattr(self, 'restart_button'):
            self.restart_button = Button(
                label="Restart Game",
                callback=self.restart_game
            )
            button_width = 200
            button_height = 50
            x_position = (screen_width - button_width) // 2
            y_position = screen_height // 2 + 200
            self.restart_button.rect = pygame.Rect(x_position, y_position, button_width, button_height)
        
        self.restart_button.draw(screen)
        
        # Handle button clicks
        mouse_pressed = pygame.mouse.get_pressed()[0]
        if not hasattr(self, 'mouse_down_previous'):
            self.mouse_down_previous = False
        if mouse_pressed and not self.mouse_down_previous:
            mouse_pos = pygame.mouse.get_pos()
            if self.restart_button.rect.collidepoint(mouse_pos):
                self.restart_button.on_click()
        self.mouse_down_previous = mouse_pressed

    def restart_game(self):
        """Reset the game when the restart button is clicked"""
        self.game.reset()
        self.path = []
        self.last_input_process = 0
        self.tail_position = None