import random
import numpy as np

stats = {'a':1000, 'b':3000, 'c': 100, 'd':3000}


print(max(stats, key=stats.get))