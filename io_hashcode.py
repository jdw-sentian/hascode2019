def read(filename):
    with open(filename, "r") as f:
        pics = list()
        for ix, line in enumerate(f):
            line = line.split()
            orientation = line[0]
            tags = line[2:]
            pics.append((ix, orientation, tags))
    return pics
