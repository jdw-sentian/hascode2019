import sys
import os
sys.path.insert(1, os.path.join(sys.path[0], '..'))

import numpy as np
import matplotlib.pyplot as plt

from itertools import product

import io_hashcode
from orientation import split, min_inter, max_inter

def num_tags(pics):
    tags = set()
    for pic in pics:
        for tag in pic[-1]:
        #print(pic[-1])
            tags.add(tag)
        #tags.update(pic[-1])

    return len(tags)

def hist_tags(pics, name):
    pic2num_tags = [len(pic[-1]) for pic in pics]
    plt.hist(pic2num_tags)

    plt.title(name)
    plt.show()

def intersect_score(pic1, pic2):
    return len(pic1[-1] & pic2[-1])

def complement_score(pic1, pic2):
    return len(pic1[-1] - pic2[-1])

def pairwise_score(pic1, pic2):
    return min(complement_score(pic1, pic2),
                complement_score(pic2, pic1),
                intersect_score(pic1, pic2)
            )

def hist_pairwise(pics, name):
    pair2left = []
    pair2right = []
    pair2intersect = []
    pair2total = []

    num_samples = 1000000
    set1 = np.random.randint(0, len(pics), [num_samples])
    set2 = np.random.randint(0, len(pics), [num_samples])
    for idx1, idx2 in zip(set1, set2):
        pic1 = pics[idx1]
        pic2 = pics[idx2]

        pair2left.append(complement_score(pic1, pic2))
        pair2right.append(complement_score(pic2, pic1))
        pair2intersect.append(intersect_score(pic1, pic2))
        pair2total.append(pairwise_score(pic1, pic2))

    print(sum(pair2total))

    fig, (ax_left, ax_right, ax_intersect, ax_total) = plt.subplots(ncols=4)

    ax_left.hist(pair2left, bins=range(35))
    ax_right.hist(pair2right, bins=range(35))
    ax_intersect.hist(pair2intersect, bins=range(35))
    ax_total.hist(pair2total, bins=range(35))

    ax_left.set_title("left")
    ax_right.set_title("right")
    ax_intersect.set_title("intersect")
    ax_total.set_title("total")

    ax_left.set_ylabel(name)
    plt.show()



def main():
    examples = {"a": "/home/jdw/Documents/2019/a_example.txt",
                "b": "/home/jdw/Documents/2019/b_lovely_landscapes.txt",
                "c": "/home/jdw/Documents/2019/c_memorable_moments.txt",
                "d": "/home/jdw/Documents/2019/d_pet_pictures.txt",
                "e": "/home/jdw/Documents/2019/e_shiny_selfies.txt"}
    name = "d"
    pics = io_hashcode.read(examples[name])
    if 1:
        verts, horzs = split(pics)
        verts = min_inter(verts, cutoff=0)
        pics = verts + horzs

    #print(pics)

    #print(num_tags(pics))
    #hist_tags(pics, name)
    hist_pairwise(pics, name)

if __name__ == '__main__':
    main()