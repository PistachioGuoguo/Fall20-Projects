
from minimax import Othello
from minimax import EMPTY, BLACK, WHITE, DIRECTIONS, DIM
from minimax import opposite, is_inbound, deepcopy
import minimax as mm

import numpy as np

BLACK_KING = 3
WHITE_KING = 4

NUM_INITIAL_KING = 5
PLACE_KING_THRESHOLD = 20 # there needs to be a threshold to place king, only exceed this threshold
KING_THRES_INCREMENT = 5 # for each king place, the threshold rise up, to not waste king pieces

def king(player: int):
    if player == BLACK:
        return BLACK_KING
    elif player == WHITE:
        return WHITE_KING


class KingOthello(Othello):

    def __init__(self):
        super(KingOthello, self).__init__()
        self.black_king_remain = self.white_king_remain = NUM_INITIAL_KING # provide each player with NUM_INITIAL_KING
        self.black_king_thres = self.white_king_thres = PLACE_KING_THRESHOLD

    def is_valid_move(self, x, y, is_king=False):
        # if is_king=True, decide whether the move is valid for a king piece, else calculate only for a normal piece
        if is_inbound(x, y) and self.board[x, y] == EMPTY:
            if not is_king: # only valid
                for direction in DIRECTIONS:
                    new_x, new_y = x + direction[0], y + direction[1]
                    if is_inbound(new_x, new_y) and self.board[new_x, new_y] == opposite(
                            self.current_player):  # make sure >= 1 opposite
                        while is_inbound(new_x, new_y) and self.board[new_x, new_y] == opposite(self.current_player):
                            new_x, new_y = new_x + direction[0], new_y + direction[1]
                        if is_inbound(new_x, new_y) and self.board[new_x, new_y] in [self.current_player, king(self.current_player)]:
                            return True  # find one valid is enough
                return False
            else: # this is a king piece
                if self.current_player == BLACK:
                    if self.black_king_remain == 0:
                        return False # not more king pieces
                else: # current_player is WHITE
                    if self.white_king_remain == 0:
                        return False
                opp_king = king(opposite(self.current_player))
                for direction in DIRECTIONS:
                    met_opponent_king = False # whether has enemy king in middle, if so, the two end must be self's two kings to reverse
                    new_x, new_y = x + direction[0], y + direction[1]
                    if is_inbound(new_x, new_y) and self.board[new_x, new_y] in \
                            [opposite(self.current_player), opp_king]:
                        if self.board[new_x, new_y] == opp_king:
                            met_opponent_king = True
                        while is_inbound(new_x, new_y) and self.board[new_x, new_y] in \
                            [opposite(self.current_player), opp_king]:
                            if self.board[new_x, new_y] == opp_king:
                                met_opponent_king = True
                            new_x, new_y = new_x + direction[0], new_y + direction[1]
                        if is_inbound(new_x, new_y) and self.board[new_x, new_y] in [self.current_player,
                                                                                     king(self.current_player)]:
                            if not met_opponent_king:
                                return True  # find one valid is enough
                            else: # have opponent's king in middle
                                if self.board[new_x, new_y] == king(self.current_player):
                                    return True
                return False

        else: # occupied or out of bound
            return False

    def take_move(self, x, y, is_king=False):
        if self.is_valid_move(x, y, is_king=is_king):
            if not is_king:
                self.board[x, y] = self.current_player
            else:
                self.board[x, y] = king(self.current_player) # place king piece
                if self.current_player == BLACK:
                    self.black_king_remain -= 1 # minus one from balance
                    self.black_king_thres += KING_THRES_INCREMENT
                else:
                    self.white_king_remain -= 1
                    self.white_king_thres += KING_THRES_INCREMENT

            pieces_to_reverse = []
            for direction in DIRECTIONS:
                new_x, new_y = x + direction[0], y + direction[1]
                temp_list = [] # temp storage for each direction
                if not is_king:
                    if is_inbound(new_x, new_y) and self.board[new_x, new_y] == opposite(self.current_player):
                        while is_inbound(new_x, new_y) and self.board[new_x, new_y] == opposite(self.current_player):
                            temp_list.append((new_x, new_y))
                            new_x, new_y = new_x + direction[0], new_y + direction[1]
                        if is_inbound(new_x, new_y) and self.board[new_x, new_y] in [self.current_player, king(self.current_player)]: # valid direction
                            pieces_to_reverse.extend(temp_list) # move to final container
                else: # king
                    met_opponent_king = False
                    if is_inbound(new_x, new_y) and self.board[new_x, new_y] in [opposite(self.current_player), king(opposite(self.current_player))]:
                        if self.board[new_x, new_y] == king(opposite(self.current_player)):
                            met_opponent_king = True
                        while is_inbound(new_x, new_y) and self.board[new_x, new_y] in [opposite(self.current_player), king(opposite(self.current_player))]:
                            if self.board[new_x, new_y] == king(opposite(self.current_player)):
                                met_opponent_king = True
                            temp_list.append((new_x, new_y))
                            new_x, new_y = new_x + direction[0], new_y + direction[1]
                        if is_inbound(new_x, new_y) and self.board[new_x, new_y] in [self.current_player, king(
                                self.current_player)]:  # valid direction
                            if not met_opponent_king:
                                pieces_to_reverse.extend(temp_list)  # move to final container
                            else: # has opponent king in middle, only reverse if two ends of this line are both self's king
                                if self.board[new_x, new_y] == king(self.current_player):
                                    pieces_to_reverse.extend(temp_list)

            for coord in pieces_to_reverse: # all pieces in the middle, no matter king or not, will be turned to normal enemy pieces
                self.board[coord[0], coord[1]] = self.current_player
        else:
            print("Invalid move.")

    def is_game_end(self):
        if not self.find_all_valid_moves(): # make sure 1st player has no valid moves
            game_copy = deepcopy(self)
            game_copy.switch_turn() # check whether the other player also has valid moves
            return True if not game_copy.find_all_valid_moves() else False
        else:
            return False


    def test_flow(self, print_board=True, print_each_game_final=True):

        while not self.is_game_end():
            if self.find_all_valid_moves(): # if have valid moves for current player
                while True:
                    new_move = self.minimax_move() # both black and white are minimax ai
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


    def find_all_valid_moves(self):
        # find all possible moves, return in form of: a list of tuples
        valid_moves = []
        for i in range(DIM):
            for j in range(DIM):
                for is_king in [True, False]: # check for king and common pieces
                    if self.is_valid_move(i, j, is_king):
                        valid_moves.append((i, j, is_king))
        return valid_moves

    def best_move(self, move_eval_dict : dict):
        # choose a best move from move_eval_dict, for current player
        king_move = {}
        common_move = {}
        for move in move_eval_dict: # separate into two dicts, and find max or min for each one
            if move[2] == True: # if king move
                king_move[move] = move_eval_dict[move]
            else:
                common_move[move] = move_eval_dict[move]

        if self.current_player == BLACK:
            m1 = max(king_move, key=king_move.get)
            m2 = max(common_move, key=common_move.get)
            if move_eval_dict[m1] - move_eval_dict[m2] > self.black_king_thres:
                return m1
            else:
                return m2
        else:
            m1 = min(king_move, key=king_move.get)
            m2 = min(common_move, key=common_move.get)
            if move_eval_dict[m1] - move_eval_dict[m2] < -self.white_king_thres:
                return m1
            else:
                return m2



    def minimax_move(self, depth=1, eval_func='king_pos_score'):
        # return the move with max minimax score
        # minimax(board, depth, player, alpha, beta) -> int:
        move_eval_dict = {}
        possible_moves = self.find_all_valid_moves()
        if possible_moves:
            for move in possible_moves: # format of move: (i, j, is_king=True/False)
                game_copy = deepcopy(self)
                game_copy.take_move(move[0], move[1], move[2])
                move_eval_dict[move] = mm.minimax(game_copy.board, depth=depth, player=opposite(self.current_player),
                                                  eval_func=eval_func, king_version=True)

            move_eval_dict = mm.shuffle_dict(move_eval_dict)  # shuffle the dict, or always choose the same move

            return self.best_move(move_eval_dict)
        else:
            return None


    def print_board(self):
        # ♔♚♕♛
        # print board in command line, added icons for king pieces for each side
        EMPTY_PIECE = '+'
        BLACK_PIECE = '⚫'
        BLACK_KING_PIECE = '♚'
        WHITE_PIECE = '⚪'
        WHITE_KING_PIECE = '♔'
        icon = {EMPTY:EMPTY_PIECE, WHITE : WHITE_PIECE, BLACK : BLACK_PIECE,
                BLACK_KING : BLACK_KING_PIECE, WHITE_KING : WHITE_KING_PIECE}
        print('================================================')
        for row in self.board:
            for i in range(len(row)):
                print(icon[row[i]], end='     ')
            print('\n')
        print('================================================')


    def finish_count(self, return_option='net', print_each_game_final=True):
        """
        :param return_option: 'net' : returns num_black - num_white, 'summary': returns num_black and num_white in a string
        """
        num_black = np.count_nonzero(self.board == BLACK) + np.count_nonzero(self.board == BLACK_KING)
        num_white = np.count_nonzero(self.board == WHITE) + np.count_nonzero(self.board == WHITE_KING)
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


if __name__ == '__main__':
    g1 = KingOthello()
    for i in range(10):
        g1.test_flow(print_board=False)


