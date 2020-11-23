import numpy as np
import random
from copy import deepcopy
import minimax as mm


EMPTY = 0
BLACK = 1
WHITE = 2
DIRECTIONS = [(-1,0),(-1,1),(-1,-1),(0,1),(0,-1),(1,0),(1,1),(1,-1)]

DIM = 8 # 8x8 is normal Reversi

def opposite(player: int):
    return BLACK if player == WHITE else WHITE

def is_inbound(x, y):
    # decide whether a tuple in inside the board
    return 0 <= x < DIM and 0 <= y < DIM

class Othello:
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
        # find all possible moves, return in form of: a list of tuples
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

    def finish_count(self, return_option='net', print_each_game_final=True):
        """
        :param return_option: 'net' : returns num_black - num_white, 'summary': returns num_black and num_white in a string
        """
        num_black = np.count_nonzero(self.board == BLACK)
        num_white = np.count_nonzero(self.board == WHITE)
        if num_black != num_white:
            which_player = 'BLACK' if num_black > num_white else 'WHITE'  # 32-32 is omitted for simplicity
            comment = "GAME END -- Black: {} White: {}. -- {} wins!".format(num_black, num_white, which_player)
        else:
            comment = "GAME END -- Black: {} White: {}. -- Draw!".format(num_black, num_white)
        if print_each_game_final:
            print(comment)
        if return_option == 'net':
            return num_black - num_white
        elif return_option == 'summary':
            return comment  # used for normal reversi GUI


    def get_move(self, player):
        # Check for game settings and decide whether it's AI or human player's turn
        players_dict = {}

        # Mode1: Man vs Machine
        if self.mode['mode'] == 'man-machine':
            if self.mode['human_first']:
                players_dict = {BLACK: 'HUMAN', WHITE: 'AI'}
            else:
                players_dict = {BLACK: 'AI', WHITE: 'HUMAN'}

            if players_dict[player] == 'HUMAN':
                move = get_input()
            elif players_dict[player] == 'AI':
                if self.mode['ai'] == 'random':
                    move = self.random_move()
                elif self.mode['ai'] == 'minimax':
                    move = self.minimax_move()

        # Mode2: AI vs AI
        elif self.mode['mode'] == 'machine-machine':
            players_dict = {BLACK: self.mode['black_strat'], WHITE: self.mode['white_strat']}
            if players_dict[player] == 'random':
                move = self.random_move()
            elif players_dict[player].find('minimax') != -1: # if contains 'minimax', then it's minimax family
                # format: 'minimax|3|pos_score'  means depth=3, eval_func=pos_score
                params = players_dict[player].split('|')
                if len(params) == 3:
                    depth = int(params[1])
                    eval_func = params[2]
                    move = self.minimax_move(depth=depth, eval_func=eval_func )
                else: # use default
                    move = self.minimax_move()
        return move


    def random_move(self):
        valid_moves = self.find_all_valid_moves() # a list of current valid moves
        if valid_moves:
            return random.choice(self.find_all_valid_moves())
        else:
            return None


    def minimax_move(self, depth=1, eval_func='pos_score'):
        # return the move with max minimax score
        # minimax(board, depth, player, alpha, beta) -> int:
        move_eval_dict = {}
        possible_moves = self.find_all_valid_moves()
        if possible_moves:
            for move in possible_moves:
                game_copy = deepcopy(self)
                game_copy.take_move(move[0], move[1])
                move_eval_dict[move] = mm.minimax(game_copy.board, depth=depth, player=opposite(self.current_player), eval_func=eval_func)

            move_eval_dict = mm.shuffle_dict(move_eval_dict) # shuffle the dict, or always choose the same move
            if self.current_player == BLACK:
                return max(move_eval_dict, key=move_eval_dict.get) # return the move with max minimax score
            else: # White is the minimizing player, the less the better.
                return min(move_eval_dict, key=move_eval_dict.get)
                # Initially when I adapted from Sebestian's Youtube code, I forgot the above two lines
                # and Black wins 95% even white uses minimax and black uses 'random'
        else:
            return None


    # main game flow
    def main_flow(self, game_mode='man-machine', human_first=True, ai_strategy='random',
                  black_strat='random', white_strat='random', print_board=True, print_each_game_final=True):
        self.mode = {'mode' : game_mode, 'human_first' : human_first, 'ai' : ai_strategy,'black_strat': black_strat, 'white_strat' : white_strat}

        while not self.is_game_end():
            if self.find_all_valid_moves(): # if have valid moves for current player
                while True:
                    new_move = self.get_move(self.current_player) # request new move
                    if self.is_valid_move(new_move[0], new_move[1]): # if entered a valid move
                        self.take_move(new_move[0], new_move[1])
                        self.switch_turn()
                        if print_board:
                            self.print_board() # print the game situation when a valid move is taken
                        break
                    else:
                        print('Invalid move. Please try again.')
            else: # no valid moves for current player
                self.switch_turn()

        return self.finish_count(print_each_game_final= print_each_game_final) # num_black - num_white


    def print_board(self):
        # print board in command line
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


def man_vs_AI(human_first=True, ai_strategy='minimax'):
    # a high-level integration function for man_vs AI
    g1 = Othello()
    g1.main_flow(game_mode='man-machine', human_first=human_first, ai_strategy=ai_strategy)


def AI_vs_AI(num_game=100, black_strat='random', white_strat='random', print_each_game_final=True, print_game_summary=True):
    # used for convenience in comparing the strength of different AIs for a specific number of game
    black_wins = 0
    white_wins = 0

    for i in range(num_game):
        g1 = Othello()
        res = g1.main_flow(game_mode='machine-machine', black_strat=black_strat, white_strat=white_strat,
                           print_board=False, print_each_game_final=print_each_game_final)
        if res > 0:
            black_wins += 1
        elif res < 0:
            white_wins += 1

    black_winrate = black_wins / (black_wins + white_wins)
    if print_game_summary:
        print("Black - White : {} - {}".format(black_wins, white_wins))
        print("Black winrate: %.2f" % black_winrate)
    return black_winrate

def AI_compete_matrix():
    AI_list = ['random', 'minimax|0|pos_score', 'minimax|0|mobi', 'minimax|0|pos_mobi',
               'minimax|1|pos_score', 'minimax|1|mobi', 'minimax|1|pos_mobi',
               'minimax|2|pos_score', 'minimax|2|pos_mobi']
    for ai1 in AI_list:
        for ai2 in AI_list:
            wr = AI_vs_AI(100, ai1, ai2, print_each_game_final=False, print_game_summary=False)
            print('%s - %s : %.2f' % (ai1, ai2, wr))

# if __name__ == '__main__':
#
#     random.seed(1)

    # strategies for AI: 'random', 'minimax'
    # minimax strats: 'minimax|depth|eval_func', where depth=1,2,3,... eval_func = 'pos_score', 'mobi', 'pos_mobi'
    # e.g:  black_strat='minimax|1|pos_mobi'

    # AI_vs_AI(num_game=100, black_strat='minimax|0|pos_score', white_strat='minimax|0|pos_mobi' )
    # AI_vs_AI(num_game=100, black_strat='random', white_strat='minimax|0|pos_score')
    # man_vs_AI(human_first=True, ai_strategy='minimax')

    # this function is extremely time-costing
    # AI_compete_matrix()

    # g1 = Othello()
    # # g1.main_flow(game_mode='machine-machine', human_first=True)
    # # g1.main_flow(game_mode='machine-machine', ai_strategy='minimax')
    # g1.main_flow(game_mode='machine-machine', black_strat='minimax', white_strat='random')


s1 = Othello()
board = np.full((DIM, DIM), BLACK)
board[4,4] = WHITE
board[0,0] = EMPTY; board[7,7] = EMPTY; board[0,7] = EMPTY; board[7,0] = EMPTY
s1.board = board
s1.current_player = WHITE
s1.take_move(0,0)
s1.take_move(0,7)
s1.take_move(7,0)
s1.take_move(7,7)
board = s1.board


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




