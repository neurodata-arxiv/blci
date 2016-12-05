import os
import b
import numpy as np
import sys
from analysis import c

def hello():
    print "hello from a"

def other():
    b.hello()

def last():
    c.hello()

def sum(a , b):
    return a + b

if __name__ == "__main__":
    mat = np.loadtxt("../otherdata/data.txt")
    np.savetxt("../data/databy2.txt", mat*2, "%.3f")
