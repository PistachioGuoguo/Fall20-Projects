import random
import numpy as np
from random import shuffle


# stats = {'a':1000, 'b':3000, 'c': 100, 'd':3000}
# print(max(stats, key=stats.get))

def shuffle_dict(old_dict : dict):
    keys = list(old_dict.keys())
    shuffle(keys)
    shuffled_dict = {key: old_dict[key] for key in keys}
    return shuffled_dict

dict1 = {'z':3, 'a':3, 'b':3, 'c':3}
new_dict = shuffle_dict(dict1)

print( max(new_dict, key=new_dict.get) )


