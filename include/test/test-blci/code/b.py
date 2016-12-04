import sys
from analysis.c import readcat
from analysis.deep.learning import a

def hello():
    print "hello from b"

def bmeth():
    print "Hitting bmeth"
    readcat()
