import numpy as np
from deep.learning.a import hello

def hello():
    print "hello from c"

def readcat():
    mat = np.read("../../../test-blci/data/test.txt")
    print mat
