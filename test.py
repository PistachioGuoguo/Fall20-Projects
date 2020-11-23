import random
import numpy as np
from random import shuffle


# stats = {'a':1000, 'b':3000, 'c': 100, 'd':3000}
# print(max(stats, key=stats.get))

a = [1,1,1,2,2]

a = np.array(a)


print(np.count_nonzero(a==1) + np.count_nonzero(a==2))

# def shuffle_dict(old_dict : dict):
#     keys = list(old_dict.keys())
#     shuffle(keys)
#     shuffled_dict = {key: old_dict[key] for key in keys}
#     return shuffled_dict
#
# dict1 = {'z':3, 'a':3, 'b':3, 'c':3}
# new_dict = shuffle_dict(dict1)
#
# print( max(new_dict, key=new_dict.get) )
#

class Othello:
    def main_flow(self):
        while not self.is_game_end():
            if self.find_all_valid_moves(): # if have valid moves for current player
                while True:
                    new_move = self.get_move(self.current_player) # request new move
                    if self.is_valid_move(new_move[0], new_move[1]): # if entered a valid move
                        self.take_move(new_move[0], new_move[1])
                        self.switch_turn()
                        break
                    else:
                        print('Invalid move.')
            else: # no valid moves for current player
                self.switch_turn()
