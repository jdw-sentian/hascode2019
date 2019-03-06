from itertools import permutations
from calc_score import score_pics
from io_hashcode import read
# from pprint import pprint
import random
from orientation import split, min_inter


def brute_window(data, left=[], right=[]):
    perms = permutations(data, len(data))
    best_score = score_pics(left + data + right)
    best_perm = data
    for perm in map(list, perms):
        new_score = score_pics(left + perm + right)
        if new_score > best_score:
            best_score = new_score
            best_perm = perm
    return best_perm


def update_window(data, window, window_index, window_size):
    return data[:window_index] + window + data[window_index + window_size:]


def brute_window_random(data, window_size=2):
    window_size = min(window_size, len(data))
    # print(0, len(data), window_size, len(data) - window_size)
    idx = random.randint(0, len(data) - window_size)
    # print("brute_window_random", idx, idx + window_size)

    if idx - 1 < 0:
        left = []
    else:
        left = [data[idx - 1]]

    if idx + window_size >= len(data) or idx + window_size < idx:
        right = []
    else:
        right = [data[idx + window_size]]

    new_window = brute_window(data[idx: idx + window_size], left, right)
    return update_window(data, new_window, idx, window_size)


if __name__ == "__main__":
    from jualg import rand
    pics = read("data/c_memorable_moments.txt")
    verts, herts = split(pics)
    verts = min_inter(verts)
    pics = verts + herts
    pics = rand(pics)
    score = score_pics(pics)
    print(score)
    for i in range(7):
        _pics = pics
        for _ in range(500):
            _pics = brute_window_random(_pics, i)
        _score = score_pics(_pics)
        print(i, _score)