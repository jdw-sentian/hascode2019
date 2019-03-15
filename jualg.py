import random
from calc_score import score_pair, window
from orientation import split, _min_inter, min_inter
from brute_slice import brute_window_random
from multiprocessing import Pool, Process, Value, Pipe, cpu_count
from itertools import repeat

cpus = cpu_count()

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
    pics = pics[current_break[1]:] + pics[:current_break[0]+1]
    return pics


def _max_score(pics):
    return len(sorted(pics, key=lambda pic: len(pic[2]))[-1])


def best_match(pic, pics, *, max_score=2**10):
    score = 0
    best_other = None
    tag_len = len(pic[2])
    for other in pics:
        tmp_score = score_pair(pic, other)
        if best_other is None or tmp_score > score:
            score = tmp_score
            best_other = other
        if score >= max_score or score >= tag_len/2:
            break
    return score, best_other


def next_is_best(pics, max_score=None, multiprocess=False):
    if max_score is None:
        max_score = _max_score(pics)

    verts, _ = split(pics)
    pics = pics.copy()
    pic = pics[0]
    new_pics = []
    pool = Pool(cpus)
    while pics:
        tag_len = len(pic[2])
        new_pics.append(pic)
        try:
            pics.remove(pic)
        except ValueError:
            pass
        if not pics:
            break
        if pic[1] == "V" and len(pic[0]) == 1:
            verts.remove(pic)
            if not verts:
                new_pics.pop()
                break
            other = _min_inter(pic, verts)
            verts.remove(other)
            pics.remove(other)
            idx = (pic[0][0], other[0][0])
            orient = "VV"
            tags = pic[2] | other[2]
            pic = (idx, orient, tags)
            if new_pics:
                new_pics.pop()
        else:
            # !! this method also sucks !!
            no_pics = len(pics)
            no_slices = min(cpus, no_pics/5000)
            if multiprocess and no_slices > 1:
                length = no_pics//no_slices
                slices = [pics[ix*length:(ix+1)*length] for ix in range(no_slices+1)]
                pic_repeat = [pic]*no_slices

                res = pool.starmap(best_match, zip(pic_repeat, slices))
                _, best_other = max(res, key=lambda x: x[0])
            else:
                _, best_other = best_match(pic, pics, max_score=max_score)

            pic = best_other
    pool.close()
    return change_break(new_pics)


if __name__ == "__main__":
    from io_hashcode import read
    from calc_score import score_pics
    from time import time
    filenames = [
        "data/a_example.txt",
        "data/b_lovely_landscapes.txt",
        "data/c_memorable_moments.txt",
        "data/d_pet_pictures.txt",
        # "data/d_pet_pictures (copy).txt",
        "data/e_shiny_selfies.txt",
    ]
    start = time()
    sum_score = 0
    for filename in filenames:
        scores = list()
        im = time()
        pics = read(filename)
        print(f"{filename}")
        # print(pics)
        score = score_pics(pics, validate=False)
        print(f"read: {score}")
        pics = sorted(pics, key=lambda pic: len(pic[2]), reverse=False)
        pics = next_is_best(pics, multiprocess=False)
        score = score_pics(pics)
        scores.append(score)
        # print(pics)
        print(f"next_is_best: {score}")

        pics = sorted(pics, key=lambda pic: len(pic[2]), reverse=False)
        pics = next_is_best(pics, multiprocess=False)
        score = score_pics(pics)
        scores.append(score)
        # print(pics)
        print(f"next_is_best: {score}")
        # times = 500
        # for _ in range(times):
        #     pics = brute_window_random(pics, 3)
        # score = score_pics(pics)
        # print(f"{times} brute_window: {score}")
        # pics = change_break(pics)
        # score = score_pics(pics)
        # print(f"change_break: {score}")
        score = max(scores)
        sum_score += score
        print(time() - im)
        print('*'*80)
    print("total:")
    print(sum_score)
    print(time()-start)
