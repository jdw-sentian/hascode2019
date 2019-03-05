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


if __name__ == "__main__":
    calc_score([[0], [3], [1, 2]])
