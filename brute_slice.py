from itertools import permutations
from calc_score import score_pics
from io_hashcode import read
from pprint import pprint
import random

def brute_window(data, left_tags=set(), right_tags=set()):
    perms = permutations(data, len(data))
    best_score = score_pics([(0, "H", left_tags)] + data + [(1, "H", right_tags)])
    best_perm = data
    for perm in map(list, perms):
        new_score = score_pics([(0, "H", left_tags)] + perm + [(1, "H", right_tags)])
        if new_score > best_score:
            best_score = new_score
            best_perm = perm
    return best_perm

def update_window(data, window, window_index, window_size):
    return data[:window_index] + window + data[window_index + window_size:]

def brute_window_random(data, window_size=2):
    print(0, len(data), window_size, len(data) - window_size)
    idx = random.randint(0, len(data) - window_size)
    print("brute_window_random", idx, idx + window_size)
    
    if idx - 1 < 0:
        left_tags = set()
    else:
        left_tags = data[idx - 1][2]
    
    if idx + window_size >= len(data) or idx + window_size < idx:
        right_tags = set()
    else:
        right_tags = data[idx + window_size][2]

    new_window = brute_window(data[idx: idx + window_size], left_tags, right_tags)
    return update_window(data, new_window, idx, window_size)
