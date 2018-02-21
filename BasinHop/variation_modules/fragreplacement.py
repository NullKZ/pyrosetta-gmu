from rosetta import *
from pyrosetta import *

def fragReplace(eaObj, pose):
    eaObj.varMover.apply(pose)
