import random
from calc_score import score_pair, window
from orientation import split, _min_inter


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


def next_is_best(pics, max_score=2**20):
    pics = pics.copy()
    verts, _ = split(pics)
    pic = pics[0]
    new_pics = []
    flag = True

    while pics:
        new_pics.append(pic)
        try:
            pics.remove(pic)
        except ValueError:
            pass
        if flag and pic[1] == "V":
            flag = False
            verts.remove(pic)
            if not verts:
                new_pics.pop()
                break
            other = _min_inter(pic, verts)
            verts.remove(other)
            pics.remove(other)
            idx = (pic[0][0], other[0][0])
            orient = pic[1]
            tags = pic[2] | other[2]
            pic = (idx, orient, tags)
            if new_pics:
                new_pics.pop()
        else:
            flag = True
            score = 0
            best_other = None
            for other in pics:
                tmp_score = score_pair(pic, other)
                if best_other is None or tmp_score > score:
                    score = tmp_score
                    best_other = other
                if score >= max_score:
                    break
            pic = best_other

    return new_pics


if __name__ == "__main__":
    from io_hashcode import read
    from calc_score import score_pics
    from time import time
    picss = [
        read("../2019/a_example.txt"),
        read("../2019/b_lovely_landscapes.txt"),
        read("../2019/c_memorable_moments.txt"),
        read("../2019/d_pet_pictures.txt"),
        read("../2019/e_shiny_selfies.txt"),
    ]
    start = time()
    sum_score = 0
    for pics in picss:
        im = time()
        pics = next_is_best(pics)
        pics = change_break(pics)
        score = score_pics(pics)
        sum_score += score
        print(score)
        print(time() - im)
        print('-'*80)
    print(sum_score)
    print(time()-start)

