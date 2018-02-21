from pyrosetta import *
from rosetta import *
from .utils import getTrueValues

def improvement(eaObj, impcfg):
    eaObj.relaxtype = impcfg['relaxtype']
    if eaObj.relaxtype == 'fast':
        eaObj.relax = protocols.relax.FastRelax()
    elif eaObj.relaxtype == 'classic':
        eaObj.relax = protocols.relax.ClassicRelax()
    elif eaObj.relaxtype == 'centroid':
        eaObj.relax = protocols.relax.CentroidRelax()
    elif eaObj.relaxtype == 'plow':
        pass
    else:
        raise Exception("Unrecognized relaxtype!")
        return
    eaObj.dE = float(impcfg['dE'])
    eaObj.impScoreFxn = create_score_function(impcfg['scorefxn'])
    if not eaObj.relaxtype == 'plow':
        eaObj.relax.set_scorefxn(eaObj.impScoreFxn)
    eaObj.impFragLength = int(impcfg['fragLength'])
    eaObj.impFragments = core.fragment.ConstantLengthFragSet(eaObj.impFragLength)
    eaObj.impFragments.read_fragment_file(eaObj.proteinPath+"{0}/aat000_0{1}_05.200_v1_3".format(eaObj.pdbid, eaObj.impFragLength))
    eaObj.movemap = MoveMap()
    eaObj.movemap.set_bb(True)
    eaObj.movemap.set_chi(True)
    eaObj.impMover = protocols.simple_moves.ClassicFragmentMover(eaObj.impFragments, eaObj.movemap)
