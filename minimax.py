from othello import Othello, DIM, BLACK, WHITE, DIRECTIONS, EMPTY
from othello import np, deepcopy, opposite, is_inbound, board
from kingOthello import KingOthello, king, BLACK_KING, WHITE_KING
import random


IN_LINE_WITH_ENEMY_KING_PENALTY = 100 # if you put a king in same line with enemy's king, your king is in danger
# to prevent this, we add a penalty to avoid such kind of behaviors
KING_ON_BORDER_BONUS = 75 # if you first put king on a boarder, you have good possibility to control this border
BASIC_KING_SCORE = 10 # A king piece has this basic score, as in pos_score_sum

def shuffle_dict(old_dict : dict):
    # shuffle the dictionary for a different order, or 'max' function will always return the same element
    keys = list(old_dict.keys())
    random.shuffle(keys)
    shuffled_dict = {key: old_dict[key] for key in keys}
    return shuffled_dict


# ------------ Minimax part ---------------

pos_score_map = [120, -20,  20,   5,   5,  20, -20, 120,
     -20, -40,  -5,  -5,  -5,  -5, -40, -20,
      20,  -5,  15,   3,   3,  15,  -5,  20,
      5,  -5,   3,   3,   3,   3,  -5,   5,
      5,  -5,   3,   3,   3,   3,  -5,   5,
      20,  -5,  15,   3,   3,  15,  -5,  20,
     -20, -40,  -5,  -5,  -5,  -5, -40, -20,
     120, -20,  20,   5,   5,  20, -20, 120]

pos_score_map = np.array(pos_score_map).reshape(DIM, DIM)

def pos_score_sum(board):
    # sum of positional score
    # defined as (Σ black - Σ white), black tries to maximize while white minimizes
    sum_black = 0
    sum_white = 0
    for i in range(DIM):
        for j in range(DIM):
            if board[i, j] == BLACK:
                sum_black += pos_score_map[i, j]
            elif board[i, j] == WHITE:
                sum_white += pos_score_map[i, j]
            elif board[i,j] == BLACK_KING:
                sum_black += pos_score_map[i, j] + BASIC_KING_SCORE
            elif board[i,j] == WHITE_KING:
                sum_white += pos_score_map[i, j] + BASIC_KING_SCORE
    return  sum_black - sum_white


def mobility(board):
    # defined number of possible moves : black - white
    g1 = Othello()
    g1.board = board
    g1.current_player = BLACK
    score_black = len(g1.find_all_valid_moves())
    g1.current_player = WHITE
    score_white = len(g1.find_all_valid_moves())
    return score_black - score_white


def pos_plus_mobi(board, multiplier=1):
    return pos_score_sum(board) + multiplier * mobility(board)


def minimax(board, depth, player, alpha=-np.inf, beta=np.inf, eval_func='pos_score', king_version=False):
    if depth == 0:
        if eval_func == 'pos_score':
            return pos_score_sum(board)
        elif eval_func == 'mobi':
            return mobility(board)
        elif eval_func == 'pos_mobi':
            return pos_plus_mobi(board)
        elif eval_func == 'king_pos_score': # this is for King Othello
            return king_pos_score_sum(board)
    if not king_version:
        game = Othello()
    else:
        game = KingOthello()
    game.board = board
    game.current_player = player
    possible_moves = game.find_all_valid_moves()

    if possible_moves:
        if player == BLACK: # maximizing player
            max_eval = - np.inf
            for move in possible_moves:
                game_copy = deepcopy(game)
                game_copy.take_move(move[0], move[1])
                eval = minimax(game_copy.board, depth-1, opposite(player), alpha, beta)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval

        else: # WHITE, minimizing player
            min_eval = np.inf
            for move in possible_moves:
                game_copy = deepcopy(game)
                game_copy.take_move(move[0], move[1])
                eval = minimax(game_copy.board, depth - 1, opposite(player), alpha, beta)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval

    else: # no possible move for current player
        game.switch_turn()
        possible_moves = game.find_all_valid_moves() # check whether opponent has moves
        if possible_moves:
            return minimax(game.board, depth-1, opposite(player), alpha, beta) # hand over to opponent, nothing changed
        else: # the opponent has no moves either, game over
            return pos_score_sum(game.board)



def king_pos_score_sum(board):
    # on the basis of pos_score_sum, add the extra value of king pieces
    # King serves as a protection for connected self pieces, so we add the score of those pieces again
    # a king on border is less easily to be captured so it has a KING_ON_BORDER_BONUS
    # but if a King is online with previous enemy king, it is in danger of being captured by enemy, so it has a IN_LINE_WITH_ENEMY_KING_PENALTY

    score = pos_score_sum(board)

    def get_king_additional_score(i, j, player):
        score = 0
        if i in [0,DIM-1] or j in [0, DIM-1]: # on border
            score += KING_ON_BORDER_BONUS
        for direction in DIRECTIONS:
            new_i, new_j = i + direction[0], j + direction[0]
            while is_inbound(new_i, new_j) and board[new_i, new_j] in [player, king(player)]: # if self's piece
                score += pos_score_map[new_i, new_j] # the king piece serves as a reinforce, so we add again of those pieces that king piece can protect
                new_i, new_j = new_i + direction[0], new_j + direction[0] # proceed with this direction
            # out of bound, met enemy piece, or enemy king
            if is_inbound(new_i, new_j): # if still in bound, means it encountered enemy pieces
                if board[new_i, new_j] == king(opposite(player)):
                    score -= IN_LINE_WITH_ENEMY_KING_PENALTY # avoid right in same line with enemy king (where the first piece after our row of pieces is an enemy king), as you might be turned
            # else: out of bound, just continue
        return score if player==BLACK else -score # black is maximizing player and white is minimizing

    for i in range(DIM):
        for j in range(DIM):
            if board[i,j] == BLACK_KING:
                score += get_king_additional_score(i, j, BLACK)
            elif board[i,j] == WHITE_KING:
                score += get_king_additional_score(i, j, WHITE)

    return score
