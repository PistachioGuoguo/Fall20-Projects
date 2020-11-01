import numpy as np
import random

EMPTY = 0
BLACK = 1
WHITE = 2

DIM = 8 # 8x8 is normal Reversi

board = np.random.choice((BLACK,WHITE),(DIM, DIM)) # create a 8x8 array of 1s and 2s (blacks and whites)

# print(board)



