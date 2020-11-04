import numpy as np
import random

EMPTY = 0
BLACK = 1
WHITE = 2
DIRECTIONS = [(-1,0),(-1,1),(-1,-1),(0,1),(0,-1),(1,0),(1,1),(1,-1)]

DIM = 8 # 8x8 is normal Reversi

# board = np.random.choice((BLACK,WHITE),(DIM, DIM)) # create a 8x8 array of 1s and 2s (blacks and whites)


# print(board)
def opposite(player: int):
    return BLACK if player == WHITE else WHITE

def is_inbound(x, y):
    return 0 <= x < DIM and 0 <= y < DIM

class Game:
    def __init__(self):
        self.board = np.full((DIM, DIM), EMPTY) # initialize board
        self.current_player = BLACK
        self.board[3,3] = BLACK; self.board[4,4] = BLACK
        self.board[3,4] = WHITE; self.board[4,3] = WHITE

    def is_valid_move(self, x, y):
        if self.board[x,y] == EMPTY:
            for direction in DIRECTIONS:
                new_x, new_y = x + direction[0], y + direction[1]
                if is_inbound(new_x, new_y):
                    if self.board[new_x, new_y] == opposite(self.current_player):
                        while self.board[new_x, new_y] == opposite(self.current_player):
                            new_x, new_y = new_x + direction[0], new_y + direction[1]
                        if self.board[new_x, new_y] == self.current_player:
                            return True # find one valid is enough
            return False
        else:
            return False

    def take_move(self, x, y):
        if self.is_valid_move(x,y):
            self.board[x, y] = self.current_player
            pieces_to_reverse = []
            for direction in DIRECTIONS:
                new_x, new_y = x + direction[0], y + direction[1]
                temp_list = [] # temp storage for each direction
                if is_inbound(new_x, new_y):
                    if self.board[new_x, new_y] == opposite(self.current_player):
                        while self.board[new_x, new_y] == opposite(self.current_player):
                            temp_list.append((new_x, new_y))
                            new_x, new_y = new_x + direction[0], new_y + direction[1]
                        if self.board[new_x, new_y] == self.current_player: # valid direction
                            pieces_to_reverse.extend(temp_list) # move to final container
            for coord in pieces_to_reverse:
                self.board[coord[0], coord[1]] = self.current_player
        else:
            print("Invalid move.")

    def switch_turn(self):
        self.current_player = opposite(self.current_player)

    def print_board(self):
        EMPTY_PIECE = '+'
        BLACK_PIECE = '⚫'
        WHITE_PIECE = '⚪'
        icon = {EMPTY:EMPTY_PIECE, WHITE : WHITE_PIECE, BLACK : BLACK_PIECE}
        for row in self.board:
            for i in range(len(row)):
                print(icon[row[i]], end='     ')
            print('\n')

s1 = Game()

board = np.full((DIM, DIM), BLACK)
board[4,4] = WHITE
board[0,0] = EMPTY; board[7,7] = EMPTY; board[0,7] = EMPTY; board[7,0] = EMPTY
s1.board = board
# s1.current_player = WHITE
# s1.take_move(0,0)
# s1.take_move(0,7)
# s1.take_move(7,0)
# s1.take_move(7,7)
# board = s1.board


# s1 = Game()
# s1.take_move(3,5)
#
# s1.switch_turn()
# s1.take_move(2,5)
#
# s1.switch_turn()
# s1.take_move(2,4)
#
# s1.switch_turn()
# s1.take_move(4,5)
#
# s1.print_board()
# print(s1.is_valid_move(4,3))




