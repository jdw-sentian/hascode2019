import sys
import os
sys.path.insert(1, os.path.join(sys.path[0], '..'))

import io_hashcode

def main():
    pics = io_hashcode.read("/home/jdw/Documents/2019/a_example.txt")

    print(pics)

if __name__ == '__main__':
    main()