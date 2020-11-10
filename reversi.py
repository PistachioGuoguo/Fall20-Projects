import numpy as np
import random
from copy import deepcopy

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
        if is_inbound(x,y) and self.board[x,y] == EMPTY:
            for direction in DIRECTIONS:
                new_x, new_y = x + direction[0], y + direction[1]
                if is_inbound(new_x, new_y) and self.board[new_x, new_y] == opposite(self.current_player): # make sure >= 1 opposite
                    while is_inbound(new_x, new_y) and self.board[new_x, new_y] == opposite(self.current_player):
                        new_x, new_y = new_x + direction[0], new_y + direction[1]
                    if is_inbound(new_x, new_y) and self.board[new_x, new_y] == self.current_player:
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
                if is_inbound(new_x, new_y) and self.board[new_x, new_y] == opposite(self.current_player):
                    while is_inbound(new_x, new_y) and self.board[new_x, new_y] == opposite(self.current_player):
                        temp_list.append((new_x, new_y))
                        new_x, new_y = new_x + direction[0], new_y + direction[1]
                    if is_inbound(new_x, new_y) and self.board[new_x, new_y] == self.current_player: # valid direction
                        pieces_to_reverse.extend(temp_list) # move to final container
            for coord in pieces_to_reverse:
                self.board[coord[0], coord[1]] = self.current_player
        else:
            print("Invalid move.")


    def switch_turn(self):
        self.current_player = opposite(self.current_player)


    def find_all_valid_moves(self):
        valid_moves = []
        for i in range(DIM):
            for j in range(DIM):
                if self.is_valid_move(i,j):
                    valid_moves.append((i,j))
        return valid_moves


    def is_game_end(self):
        if not self.find_all_valid_moves(): # make sure 1st player has no valid moves
            game_copy = deepcopy(self)
            game_copy.switch_turn() # check whether the other player also has valid moves
            return True if not game_copy.find_all_valid_moves() else False
        else:
            return False


    def random_move(self):
        valid_moves = self.find_all_valid_moves() # a list of current valid moves
        if valid_moves:
            return random.choice(self.find_all_valid_moves())
        else:
            return None

    def finish_count(self):
        num_black = np.count_nonzero(self.board == BLACK)
        num_white = np.count_nonzero(self.board == WHITE)
        if num_black != num_white:
            which_player = 'BLACK' if num_black > num_white else 'WHITE' # 32-32 is omitted for simplicity
            comment = "GAME END -- Black: {} White: {}. -- {} wins!".format(num_black, num_white, which_player)
        else:
            comment = "GAME END -- Black: {} White: {}. -- Draw!".format(num_black, num_white)
        # print(comment)
        return comment


    def get_move(self, player):
        players_dict = {}
        if self.mode['mode'] == 'man-machine':
            if self.mode['human_first']:
                players_dict = {BLACK: 'HUMAN', WHITE: 'AI'}
            else:
                players_dict = {BLACK: 'AI', WHITE: 'HUMAN'}
        elif self.mode['mode'] == 'machine-machine':
            players_dict = {BLACK: 'AI', WHITE: 'AI'}

        if players_dict[player] == 'HUMAN':
            move = get_input()
        elif players_dict[player] == 'AI':
            if self.mode['ai'] == 'random':
                move = self.random_move()
        return move


    def main_flow(self, game_mode='man-machine', human_first=True, ai_strategy='random'):
        self.mode = {'mode' : game_mode, 'human_first' : human_first, 'ai' : ai_strategy}

        while not self.is_game_end():
            if self.find_all_valid_moves(): # if have valid moves for current player
                while True:
                    new_move = self.get_move(self.current_player) # request new move
                    if self.is_valid_move(new_move[0], new_move[1]): # if entered a valid move
                        self.take_move(new_move[0], new_move[1])
                        self.switch_turn()
                        self.print_board() # print the game situation when a valid move is taken
                        break
                    else:
                        print('Invalid move. Please try again.')
            else: # no valid moves for current player
                self.switch_turn()

        self.finish_count()



    def print_board(self):
        EMPTY_PIECE = '+'
        BLACK_PIECE = '⚫'
        WHITE_PIECE = '⚪'
        icon = {EMPTY:EMPTY_PIECE, WHITE : WHITE_PIECE, BLACK : BLACK_PIECE}
        print('================================================')
        for row in self.board:
            for i in range(len(row)):
                print(icon[row[i]], end='     ')
            print('\n')
        print('================================================')


def get_input():
    move = input('Please enter your move in form x,y: ')
    x, y = move.split(',')
    return (int(x), int(y)) # all moves takes the form of tuple


if __name__ == '__main__':
    g1 = Game()
    g1.main_flow(game_mode='machine-machine', human_first=True)





# board = np.full((DIM, DIM), BLACK)
# board[4,4] = WHITE
# board[0,0] = EMPTY; board[7,7] = EMPTY; board[0,7] = EMPTY; board[7,0] = EMPTY
# s1.board = board
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




