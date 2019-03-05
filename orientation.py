

def split(pics):
    verts = [pic for pic in pics if pic[1] == "V"]
    horts = [pic for pic in pics if pic[1] == "H"]
    return verts, horts


def naive_union(verts):
    new_verts = list()
    for ix, _ in enumerate(verts[:-1:2]):
        a, b = verts[ix:ix+2]
        idx = (a[0][0], b[0][0])
        orient = a[1]
        tags = a[2] | b[2]
        new_verts.append((idx, orient, tags))
    return new_verts
    # return [((a[0], b[0]), a[1], a[2] | b[2]) for a, b in verts[::2]]


def min_union(verts):
    pass


# from io_hashcode import read
# pics = read("/home/ju/Downloads/2019/a_example (copy).txt")
# verts, horts = split(pics)
# verts = naive_union(verts)
# print(verts)
