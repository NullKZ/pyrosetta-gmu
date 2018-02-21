from .utils import seq_from_fasta
from pyrosetta import *
from rosetta import *

def bh(eaObj, initcfg):
    eaObj.genN = int(initcfg['nGen'])
    eaObj.pdbid = initcfg['protein']
    eaObj.proteinPath = initcfg['path']
    if initcfg['initState'] == 'extended':
        eaObj.sequence = seq_from_fasta(eaObj.proteinPath+"{0}/{0}.fasta".format(eaObj.pdbid))
        eaObj.initialPose = pose_from_sequence(eaObj.sequence)
    elif initcfg['initState'] == 'pdb':
        eaObj.initialPose = pose_from_pdb(eaObj.proteinPath+"{0}/{0}.pdb")
    elif initcfg['initState'] == 'sequence':
        eaObj.sequence = initcfg['sequence']
        eaObj.initialPose = pose_from_sequence(eaObj.sequence)
    else:
        raise Exception("Unrecognized initState!")
        return
    eaObj.seqlen = len(eaObj.initialPose.sequence())
    #include stuff for random seed here?
    #either that or somwhere more visibil
    #jk put it in the population setup
