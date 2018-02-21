from pyrosetta import *
from rosetta import *

def converter(eaObj):
    eaObj.fa2cen = SwitchResidueTypeSetMover("centroid")
    eaObj.cen2fa = protocols.simple_moves.ReturnSidechainMover(eaObj.initialPose)
