

def get_move(self, player: int):  # get_move(white)
    players_dict = {}
    if self.game.mode['mode'] == 'man-machine':
        if self.game.mode['human_first']:
            players_dict = {BLACK: 'HUMAN', WHITE: 'AI'}
        else:
            players_dict = {BLACK: 'AI', WHITE: 'HUMAN'}
    elif self.game.mode['mode'] == 'machine-machine':
        players_dict = {BLACK: 'AI', WHITE: 'AI'}

    if players_dict[player] == 'HUMAN':
        move = self.clicked_pos
    elif players_dict[player] == 'AI':
        if self.game.mode['ai'] == 'random':
            move = self.game.random_move()
    return move


def main_flow(self, game_mode='man-machine', human_first=True, ai_strategy='random'):
    self.game.mode = {'mode': game_mode, 'human_first': human_first, 'ai': ai_strategy}

    while not self.game.is_game_end():
        if self.game.find_all_valid_moves():  # if have valid moves for current player
            while True:
                time.sleep(1)
                new_move = self.get_move(self.game.current_player)  # request new move
                if self.game.is_valid_move(new_move[0], new_move[1]):  # if entered a valid move
                    self.game.take_move(new_move[0], new_move[1])
                    self.game.switch_turn()
                    self.draw_board()  # print the game situation when a valid move is taken
                    break
                else:
                    print('Invalid move. Please try again.')
        else:  # no valid moves for current player
            self.game.switch_turn()

    self.game.finish_count()