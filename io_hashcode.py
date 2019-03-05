import pickle


def read(filename):
    with open(filename, "r") as f:
        pics = list()
        f.readline()
        for ix, line in enumerate(f):
            line = line.split()
            orientation = line[0]
            tags = set(line[2:])
            pics.append(((ix,), orientation, tags))
    return pics


def write(pics, filename):
    with open(filename, "w") as f:
        f.write(str(len(pics)) + "\n")
        for pic in pics:
            f.write(" ".join(map(str, pic[0])) + "\n")


def dump(pics, filename):
    with open(filename, "wb") as f:
        pickle.dump(pics, f)


def load(filename):
    with open(filename, "rb") as f:
        return pickle.load(f)


if __name__ == "__main__":
    pics = read("/home/ju/Downloads/2019/a_example.txt")
    dump(pics, "pics.pickle")
    pics2 = load("pics.pickle")
    print(pics == pics2)
    write(pics, "sol.txt")
