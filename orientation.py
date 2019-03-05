

def split(pics):
    verts = [pic for pic in pics if pic[1] == "V"]
    horts = [pic for pic in pics if pic[1] == "H"]
    return verts, horts
