from pyrosetta import *
from rosetta import *

def evaluation(eaObj, initcfg):
    eaObj.evalnum = 0
    eaObj.evalbudget = int(initcfg['evalbudget'])
    eaObj.knownNative = pose_from_pdb(eaObj.proteinPath+"{0}/{0}.pdb".format(eaObj.pdbid))

