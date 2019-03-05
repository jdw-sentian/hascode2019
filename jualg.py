import random
from calc_score import score_pair, window


def rand(pics):
    random.shuffle(pics)
    return pics


def change_break(pics):
    current_break = (-1, 0)
    lowest_score = score_pair(pics[-1], pics[0])
    for ix, (a, b) in enumerate(window(pics)):
        score = score_pair(a, b)
        if score < lowest_score:
            current_break = (ix, ix+1)
            lowest_score = score
        if lowest_score == 0:
            break
    pics[current_break[1]:] + pics[:current_break[0]]
    return pics
