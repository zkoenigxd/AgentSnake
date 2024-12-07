from typing import Self
from enum import Enum
import random

class BlockState(Enum):
    Empty = 0
    Snake = 1
    Food = 2
    Obsticle = 3

class InputAction(Enum):
    Left = (-1,0)
    Right = (1, 0)
    Up = (0, -1)
    Down = (0, 1)


class SnakeGame:

    def __init__(self: Self) -> Self:
        self.rows, self.cols = (45,80)
        self.state_arr = [[BlockState.Empty for i in range(self.cols)] for j in range(self.rows)]
        self.set_block_state(self.place_food(self.state_arr), BlockState.Food)
        self.score = 0
        self.is_dead = False
        self.action = InputAction.Right
        self.head_location = (int(self.rows / 2), int(self.cols / 2))


    def place_food(self: Self) -> tuple[int, int]:
        while True:  #DO WHILE IMPLEMENTATION - do place_food while food placed in invalid space
            row = random.randint(0,len(self.rows) - 1)
            column = random.randint(0, len(self.cols[0]) - 1)
            if self.state_arr[row][column] == BlockState.Empty:
                return row, column
            
    def get_grid_size(self: Self) -> tuple[int,int]:
        return self.rows, self.cols
    
    def set_block_state(self: Self, location : tuple[int, int], state : BlockState):
        l_x, l_y = location
        self.state_arr[l_x][l_y] = state

    def set_action(self: Self, action: InputAction):
        self.action = action

    def process_action(self: Self):
        new_head_x, new_head_y = self.head_location + self.action
        if new_head_x < 0 or new_head_x >= self.cols or new_head_y < 0 or new_head_y >= self.rows:
            self.is_dead = True
            return
        if self.state_arr[new_head_x][new_head_y] == BlockState.Snake or self.state_arr[new_head_x][new_head_y] == BlockState.Obsticle:
            self.is_dead = True
            return
        if self.state_arr[new_head_x][new_head_y] == BlockState.Food:
            self.score += 1
            self.set_block_state(self.place_food(self.state_arr), BlockState.Food)
        self.set_block_state((new_head_x,new_head_y), BlockState.Snake)
        
    def get_game_state(self):
        return self.state_arr, self.score, self.isDead