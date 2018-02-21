from pyrosetta import *
from rosetta import *
from .utils import getTrueValues

def variation(eaObj, varcfg):
    if int(varcfg['fragReplacement']):
        eaObj.varFragLength = int(varcfg['fragLength'])
        eaObj.varFragments = core.fragment.ConstantLengthFragSet(eaObj.varFragLength)
        eaObj.varFragments.read_fragment_file(eaObj.proteinPath+"{0}/aat000_0{1}_05.200_v1_3".format(eaObj.pdbid, eaObj.varFragLength))
        eaObj.movemap = MoveMap()
        eaObj.movemap.set_bb(int(varcfg['bbAngle'])==1)
        eaObj.movemap.set_chi(int(varcfg['chiAngle'])==1)
        eaObj.varMover = protocols.simple_moves.ClassicFragmentMover(eaObj.varFragments, eaObj.movemap)
