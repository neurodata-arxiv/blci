import sys
import numpy as np
from deep.learning.a import hello

def hello():
    print "hello from c"

def read_mat(fn="../../../test-blci/data/data.txt"):
    return np.loadtxt(fn)

def readcat(fn):
    print read_mat(fn)

def read_modify_write(infn, val, outfn):
    mat = read_mat(infn)
    np.savetxt(outfn, val*mat, "%.3f")

if __name__ == "__main__":
    read_modify_write(sys.argv[1], float(sys.argv[2]), sys.argv[3])
