from collections import deque
from typing import Self
from enum import Enum
import random

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

    def __init__(self: Self) -> Self:
        self.score = 0
        self.is_dead = False
        self.action = InputAction.Right
        self.rows, self.cols = (45,80)
        self.state_arr = [[BlockState.Empty for i in range(self.cols)] for j in range(self.rows)]
        self.head_location = (int(self.rows / 2), int(self.cols / 2))
        self.tail_locations = deque()
        self.tail_locations.append((self.head_location[0] + self.action.value[0] * -0, self.head_location[1] + self.action.value[1] * -0))
        self.tail_locations.append((self.head_location[0] + self.action.value[0] * -1, self.head_location[1] + self.action.value[1] * -1))
        self.tail_locations.append((self.head_location[0] + self.action.value[0] * -2, self.head_location[1] + self.action.value[1] * -2))
        self.tail_locations.append((self.head_location[0] + self.action.value[0] * -3, self.head_location[1] + self.action.value[1] * -3))
        self.set_block_state(self.head_location, BlockState.Snake)
        self.place_food()


    def place_food(self: Self):
        while True:  #DO WHILE IMPLEMENTATION - do place_food while food placed in invalid space
            x = random.randint(0,self.rows - 1)
            y = random.randint(0, self.cols - 1)
            if self.state_arr[x][y] == BlockState.Empty:
                self.set_block_state((x, y), BlockState.Food)
                return
            
    def get_grid_size(self: Self) -> tuple[int,int]:
        return self.rows, self.cols
    
    def set_block_state(self: Self, location : tuple[int, int], state : BlockState):
        x, y = location
        self.state_arr[x][y] = state

    def set_action(self: Self, action: InputAction):
        self.action = action

    def process_action(self: Self):
        new_head_x, new_head_y = self.head_location[0] + self.action.value[0], self.head_location[1] + self.action.value[1]
        if new_head_x < 0 or new_head_x >= self.rows or new_head_y < 0 or new_head_y >= self.cols:
            self.is_dead = True
            return
        if self.state_arr[new_head_x][new_head_y] == BlockState.Snake or self.state_arr[new_head_x][new_head_y] == BlockState.Obsticle:
            self.is_dead = True
            return
        if self.state_arr[new_head_x][new_head_y] == BlockState.Food:
            self.score += 1
            self.place_food()
        else:
            self.set_block_state(self.tail_locations.popleft(), BlockState.Empty)
        self.head_location = (new_head_x, new_head_y)
        self.tail_locations.append(self.head_location)
        self.set_block_state(self.head_location, BlockState.Snake)
        
    def get_game_state(self):
        return self.state_arr, self.score, self.is_dead