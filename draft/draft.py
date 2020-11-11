
def pos_score_sum(board, player):
    # Define pos_score_sum as sum of self minus sum of opponent, try to maximize in minimax
    self_score = 0
    opponent_score = 0
    for i in range(DIM):
        for j in range(DIM):
            if board[i, j] == player:
                self_score += pos_score_map[i, j]
            elif board[i, j] == opposite(player):
                opponent_score += pos_score_map[i, j]
    return self_score - opponent_score



# A self written minimax algorithm, which successfully works
def minimax(board, depth, player, eval_func=pos_score_sum) -> int:
    if depth == 0:
        return eval_func(board, player) # just count
    else:
        game = Game()
        game.board = board
        game.current_player = player
        possible_moves = game.find_all_valid_moves()
        scores = []
        if possible_moves:
            for move in possible_moves:
                game_copy = deepcopy(game)
                game_copy.take_move(move[0], move[1])
                scores.append(-minimax(game_copy.board, depth - 1, opposite(player), eval_func))
            return max(scores)
        else: # current player has no valid moves
            game.switch_turn() # hand over to opponent
            opponent_moves = game.find_all_valid_moves()
            if opponent_moves: # opponent has move
                for move in opponent_moves:
                    scores.append(-minimax(game.board, depth - 1, opposite(player), eval_func))
                return max(scores)
            else: # enemy also has no moves, that's it end of game
                return eval_func(board, player)