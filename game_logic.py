from enum import Enum
import random

class BlockState(Enum):
    Empty = 0
    Snake = 1
    Food = 2
    Obsticle = 3

def place_food(spaces):
    while True:  #DO WHILE placed in invalid space
        row = random.randint(0,len(spaces) - 1)
        column = random.randint(0, len(spaces[0]) - 1)
        if spaces[row][column] == BlockState.Empty:
            return row, column
        
