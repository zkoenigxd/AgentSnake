from collections import deque
from typing import Self
from enum import Enum
import random
import csv
import os
import time
from Scenes.PlotCSVdata import plot_csv_data  # Import the function directly
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class BlockState(Enum):
    Empty = 0
    Snake = 1
    Food = 2
    Obsticle = 3

class InputAction(Enum):
    Up = (-1, 0)
    Down = (1,0)
    Right = (0, 1)
    Left = (0, -1)


class SnakeGame:

    def __init__(self: Self, save_id: str, rows=26, cols=32) -> Self:
        self.score = 0
        self.save_id = save_id
        self.is_dead = False
        self.action = InputAction.Right
        self.rows, self.cols = (rows,cols)
        self.state_arr = [[BlockState.Empty for i in range(self.cols)] for j in range(self.rows)]
        self.head_location = (int(self.rows / 2), int(self.cols / 2))
        self.tail_locations = deque()
        self.food_location = None
        self.tail_locations.append((self.head_location[0] + self.action.value[0] * -0, self.head_location[1] + self.action.value[1] * -0))
        self.tail_locations.append((self.head_location[0] + self.action.value[0] * -1, self.head_location[1] + self.action.value[1] * -1))
        self.tail_locations.append((self.head_location[0] + self.action.value[0] * -2, self.head_location[1] + self.action.value[1] * -2))
        self.tail_locations.append((self.head_location[0] + self.action.value[0] * -3, self.head_location[1] + self.action.value[1] * -3))
        self.set_block_state(self.head_location, BlockState.Snake)
        self.place_food()
        # Initialize timers
        self.start_time = time.time()
        self.elapsed_time = 0
        self.total_time = 0  # Total time across all attempts
        # Initialize counters
        self.attempts = 0
        self.high_score = 0  # Track highest score achieved

    def place_food(self: Self):
        while True:  #DO WHILE IMPLEMENTATION - do place_food while food placed in invalid space
            x = random.randint(0,self.rows - 1)
            y = random.randint(0, self.cols - 1)
            if self.state_arr[x][y] == BlockState.Empty:
                self.set_block_state((x, y), BlockState.Food)
                self.food_location = (x,y)
                return
    
    def set_block_state(self: Self, location : tuple[int, int], state : BlockState):
        x, y = location
        self.state_arr[x][y] = state

    def set_action(self: Self, action: InputAction):
        self.action = action

    def process_action(self: Self):
        # Skip processing if already dead
        if self.is_dead:
            return
            
        new_head_x, new_head_y = self.head_location[0] + self.action.value[0], self.head_location[1] + self.action.value[1]
        if new_head_x < 0 or new_head_x >= self.rows or new_head_y < 0 or new_head_y >= self.cols:
            self.is_dead = True
            self.save_game(self.save_id, self.attempts, self.score, self.elapsed_time)
            return
        if self.state_arr[new_head_x][new_head_y] == BlockState.Snake or self.state_arr[new_head_x][new_head_y] == BlockState.Obsticle:
            self.is_dead = True
            self.save_game(self.save_id, self.attempts, self.score, self.elapsed_time)
            return
        if self.score == self.rows * self.cols - 5:
            self.is_dead = True
            self.save_game(self.save_id, self.attempts, self.score, self.elapsed_time)
            return
        if self.state_arr[new_head_x][new_head_y] == BlockState.Food:
            self.score += 1
            # Update high score if current score is higher
            if self.score > self.high_score:
                self.high_score = self.score
            self.place_food()
        else:
            self.set_block_state(self.tail_locations.popleft(), BlockState.Empty)
        self.head_location = (new_head_x, new_head_y)
        self.tail_locations.append(self.head_location)
        self.set_block_state(self.head_location, BlockState.Snake)
        # Update elapsed time
        self.elapsed_time = time.time() - self.start_time

    def reset(self: Self):
        
        # Increment attempt counter
        self.attempts += 1
        
        # Reset game state
        self.score = 0
        self.is_dead = False
        self.action = InputAction.Right
        
        # Clear the board
        self.state_arr = [[BlockState.Empty for i in range(self.cols)] for j in range(self.rows)]
        
        # Reset snake position
        self.head_location = (int(self.rows / 2), int(self.cols / 2))
        self.tail_locations = deque()
        self.tail_locations.append((self.head_location[0] + self.action.value[0] * -0, self.head_location[1] + self.action.value[1] * -0))
        self.tail_locations.append((self.head_location[0] + self.action.value[0] * -1, self.head_location[1] + self.action.value[1] * -1))
        self.tail_locations.append((self.head_location[0] + self.action.value[0] * -2, self.head_location[1] + self.action.value[1] * -2))
        self.tail_locations.append((self.head_location[0] + self.action.value[0] * -3, self.head_location[1] + self.action.value[1] * -3))
        self.set_block_state(self.head_location, BlockState.Snake)
        
        # Place new food
        self.place_food()
        
        # Reset timer for new attempt
        self.start_time = time.time()
        self.elapsed_time = 0

    def save_game(self: Self, save_id: str, attempts: int, score: int, elapsed_time: float):
        """
        Save game statistics to a CSV file in the SaveData folder.
                
        Args:
            save_id: Identifier for the save (e.g., 'human', 'hamiltonian')
            attempts: Number of attempts made
            score: Final score achieved
            elapsed_time: Time taken to achieve the score (in seconds)
        """
        # Create SaveData directory if it doesn't exist
        save_dir = "SaveData"
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
            
        filename = os.path.join(save_dir, f"snake_game_scores_{save_id}.csv")
        file_exists = os.path.isfile(filename)
        
        # Format elapsed time as HH:MM:SS.mmm
        hours = int(elapsed_time // 3600)
        minutes = int((elapsed_time % 3600) // 60)
        seconds = int(elapsed_time % 60)
        milliseconds = int((elapsed_time % 1) * 1000)
        time_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}.{milliseconds:03d}"

        # Add current attempt's time to total time
        self.total_time += self.elapsed_time
        
        with open(filename, 'a', newline='') as f:
            writer = csv.writer(f)
            # Write header if file is new
            if not file_exists:
                writer.writerow(['attempt', 'score', 'time'])
            # Write the data row
            writer.writerow([attempts, score, time_str])
        
        # Call plotting function directly and show any errors
        try:
            plot_csv_data(filename)
        except Exception as e:
            print(f"Error plotting data: {str(e)}")  # More detailed error output
            
    def get_elapsed_time(self: Self) -> float:
        """Return the elapsed time in seconds since the game started or was reset"""
        return self.elapsed_time
        
    def get_total_time(self: Self) -> float:
        """Return the total time in seconds across all attempts"""
        return self.total_time
        
    def get_high_score(self: Self) -> int:
        """Return the highest score achieved across all attempts"""
        return self.high_score