

def split(pics):
    verts = [pic for pic in pics if pic[1] == "V"]
    horts = [pic for pic in pics if pic[1] == "H"]
    return verts, horts


def naive_union(verts):
    new_verts = list()
    for ix, _ in enumerate(verts[:-1:2]):
        ix *= 2
        print(ix)
        a, b = verts[ix:ix+2]
        idx = (a[0][0], b[0][0])
        orient = a[1]
        tags = a[2] | b[2]
        new_verts.append((idx, orient, tags))
    return new_verts


def max_inter(verts):
    verts = verts.copy()
    new_verts = list()
    while verts:
        a = verts.pop()

        max_i = None
        b = None
        for test_b in verts:
            size_i = len(a[2] & test_b[2])
            if b is None or size_i > max_i:
                b = test_b
                max_i = size_i
        if b is None:
            continue

        verts.remove(b)
        idx = (a[0][0], b[0][0])
        orient = a[1]
        tags = a[2] | b[2]
        new_verts.append((idx, orient, tags))
    return new_verts


def min_inter(verts, cutoff=0):
    verts = verts.copy()
    new_verts = list()
    while verts:
        a = verts.pop()

        b = None
        for test_b in verts:
            size_i = len(a[2] & test_b[2])
            if size_i <= cutoff:
                b = test_b
                break
        else:
            print("Warning!")
            continue

        verts.remove(b)
        idx = (a[0][0], b[0][0])
        orient = a[1]
        tags = a[2] | b[2]
        new_verts.append((idx, orient, tags))
    return new_verts


if __name__ == '__main__':
    from io_hashcode import read
    pics = read("/home/ju/Downloads/2019/a_example (copy).txt")
    verts, horts = split(pics)
    verts_ = naive_union(verts)
    print(verts_)
    verts_ = max_inter(verts)
    print(verts_)
