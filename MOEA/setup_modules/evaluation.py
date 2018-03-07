from pyrosetta import *
from rosetta import *

def evaluation(eaObj, initcfg):
    eaObj.evalnum = 0
    eaObj.evalbudget = int(initcfg['evalbudget'])
    eaObj.knownNative = pose_from_pdb(eaObj.proteinPath+"{0}/{0}.pdb".format(eaObj.pdbid))

    eaObj.hbond_sr = ScoreFunction()
    eaObj.hbond_sr.set_weight(core.scoring.hbond_sr_bb, 1.0)
    eaObj.hbond_lr = ScoreFunction()
    eaObj.hbond_lr.set_weight(core.scoring.hbond_lr_bb, 1.0)
    eaObj.other = create_score_function("score4_smooth")
    eaObj.other.set_weight(core.scoring.hbond_sr_bb, 0)
    eaObj.other.set_weight(core.scoring.hbond_lr_bb, 0)