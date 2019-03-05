from itertools import islice

def load_pics():
    pics = {}
    with open("a_example.txt") as f:
        for i, line in enumerate(f):
            if i != 0:
                line = line[:-1]
                line = line.split()
                pics[i - 1] = (line[0], set(line[2:]))
    return pics


def calc_score(solution):
    pics = load_pics()
    used = set()
    last = set()
    score = 0
    for slide in solution:
        if len(slide) == 1:
            pic = pics[slide[0]]
            if pic[0] != "H" or slide[0] in used:
                print(pic)
                raise
            used.add(slide[0])
            l1 = len(last)
            l2 = len(pic[1])
            l3 = len(last & pic[1])
            score += min(l1 - l3, l2 - l3, l3)
            last = pic[1]
        else:
            pic1 = pics[slide[0]]
            pic2 = pics[slide[1]]
            if pic1[0] != "V" or pic2[0] != "V" or slide[0] in used or slide[1] in used:
                raise
            used.add(slide[0])
            used.add(slide[1])
            tags = pic1[1] | pic2[1]
            l1 = len(last)
            l2 = len(tags)
            l3 = len(last & tags)
            score += min(l1 - l3, l2 - l3, l3)
            last = tags
        print(score)


def window(seq, n=2):
    "Returns a sliding window (of width n) over data from the iterable"
    "   s -> (s0,s1,...s[n-1]), (s1,s2,...,sn), ...                   "
    it = iter(seq)
    result = tuple(islice(it, n))
    if len(result) == n:
        yield result
    for elem in it:
        result = result[1:] + (elem,)
        yield result


def score_pair(a, b):
    a_not_b = len(a[2] - b[2])
    a_and_b = len(a[2] & b[2])
    b_not_a = len(b[2] - a[2])
    return min(a_not_b, a_and_b, b_not_a)


def score_pics(pics):
    score = 0
    for a, b in window(pics):
        score += score_pair(a, b)
    return score


if __name__ == "__main__":
    # calc_score([[0], [3], [1, 2]])
    from io_hashcode import read
    from orientation import split, max_inter, min_inter
    from jualg import rand

    pics = read("/home/ju/Downloads/2019/c_memorable_moments.txt")
    verts, horts = split(pics)
    verts = min_inter(verts)
    pics = verts + horts
    scores = set()
    for _ in range(1000):
        pics = rand(pics)
        score = score_pics(pics)
        scores.add(score)
    print(max(scores))