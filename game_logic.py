from typing import Self
from enum import Enum
import random

class BlockState(Enum):
    Empty = 0
    Snake = 1
    Food = 2
    Obsticle = 3

class SnakeGame:

    def __init__(self: Self) -> Self:
        self.rows, self.cols = (45,80)
        self.state_arr = [[BlockState.Empty for i in range(self.cols)] for j in range(self.rows)]
        self.food_collected = False
        self.set_state(self.place_food(self.state_arr), BlockState.Food)

    def place_food(self: Self) -> tuple[int, int]:
        while True:  #DO WHILE IMPLEMENTATION - do place_food while food placed in invalid space
            row = random.randint(0,len(self.rows) - 1)
            column = random.randint(0, len(self.cols[0]) - 1)
            if self.state_arr[row][column] == BlockState.Empty:
                return row, column
            
    def get_grid_size(self: Self) -> tuple[int,int]:
        return self.rows, self.cols
    
    def set_block_state(self : Self, location : tuple[int, int], state : BlockState):
        l_x, l_y = location
        self.state_arr[l_x][l_y] = state
        
