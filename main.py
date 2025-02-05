import sys
import os
sys.path.insert(1, os.path.join(sys.path[0], '..'))

import time
import numpy as np
import matplotlib.pyplot as plt

from itertools import product

import io_hashcode
from orientation import split, min_inter, max_inter
from calc_score import calc_score

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

def pairing_score(seq1, seq2):
    first1 = seq1[0]
    last1 = seq1[-1]
    first2 = seq2[0]
    last2 = seq2[-1]

    scores = [pairwise_score(first1, first2),
              pairwise_score(first1, last2),
              pairwise_score(last1, first2),
              pairwise_score(last1, last2)
            ]

    return max(scores), np.argmax(scores)

def solve_max_combine(pics, init_cutoff=1):
    cutoff = init_cutoff
    sequences = [[pic] for pic in pics]

    t0 = time.time()

    iter_since_join = 0
    while len(sequences) > 1:
        if time.time() - t0 > 5:
            print("Cutoff:", cutoff)
            print("Num sequences:", len(sequences))
            print("Total score:", sum([total_score(seq) for seq in sequences]))
            print()
            t0 = time.time()
        if iter_since_join >= 5000:
            cutoff -= 1 # to guarantee termination
            cutoff = max(cutoff, 10)

        idx1 = np.random.randint(0, len(sequences))
        idx2 = np.random.randint(0, len(sequences))

        if idx1 == idx2:
            continue

        seq1 = sequences[idx1]
        seq2 = sequences[idx2]

        s, argmax = pairing_score(seq1, seq2)
        if s >= cutoff:
            if argmax == 0:
                seq = list(reversed(seq2)) + seq1
            elif argmax == 1:
                seq = seq2 + seq1
            elif argmax == 2:
                seq = seq1 + seq2
            elif argmax == 3:
                seq = seq1 + list(reversed(seq2))

            try:
                sequences.remove(seq1)
                sequences.remove(seq2)
            except Exception:
                print(seq1)
                print(seq2)
                raise
            sequences.append(seq)
            iter_since_join = 0
        else:
            iter_since_join += 1

    return sequences[0]

def total_score(sequence):
    return sum([pairwise_score(pic1, pic2) for pic1, pic2 in zip(sequence[:-1], sequence[1:])])

def main():
    examples = {"a": "/home/jdw/Documents/2019/a_example.txt",
                "b": "/home/jdw/Documents/2019/b_lovely_landscapes.txt",
                "c": "/home/jdw/Documents/2019/c_memorable_moments.txt",
                "d": "/home/jdw/Documents/2019/d_pet_pictures.txt",
                "e": "/home/jdw/Documents/2019/e_shiny_selfies.txt"}
    name = "e"
    pics = io_hashcode.read(examples[name])
    if 1:
        verts, horzs = split(pics)
        verts = min_inter(verts, cutoff=0)
        pics = verts + horzs

    #print(pics)

    #print(num_tags(pics))
    #hist_tags(pics, name)
    #hist_pairwise(pics, name)

    seq = solve_max_combine(pics, init_cutoff=20)
    #print(seq)
    #print(calc_score(seq))
    print(total_score(seq))

if __name__ == '__main__':
    main()