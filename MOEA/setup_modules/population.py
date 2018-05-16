from pyrosetta import *
from rosetta import *
from math import fabs, sqrt, exp
from random import randint, random

def population(eaObj, initcfg):
    eaObj.population = []
    eaObj.randomSeed = False
    if initcfg['randomseed'] == '1':
        eaObj.randomSeed = True
    for i in range(int(initcfg['population'])):
        temporaryPose = Pose()
        temporaryPose.assign(eaObj.initialPose)
        if eaObj.cfg['improvement']['representation'] == 'centroid':
            eaObj.fa2cen.apply(temporaryPose)
        if eaObj.randomSeed:
            randomSeed(eaObj, temporaryPose)
        eaObj.population.append(temporaryPose)
    if len(eaObj.population) < 1:
        return
    eaObj.score0 = create_score_function('score0')
    eaObj.score1 = create_score_function('score1')
    setupfrag = core.fragment.ConstantLengthFragSet(9)
    setupfrag.read_fragment_file(eaObj.proteinPath+"{0}/aat000_0{1}_05.200_v1_3".format(eaObj.pdbid, 9))
    setupmm = MoveMap()
    setupmm.set_bb(True)
    setupmm.set_chi(True)
    eaObj.setupMover = protocols.simple_moves.ClassicFragmentMover(setupfrag, setupmm)
    for pose in eaObj.population:
        pose.assign(randomizeConformation(eaObj, pose))

def mc(eaObj, newPose, oldPose, score):
        diff = score(newPose) - score(oldPose)
        r = random()
        tmp = eaObj.evalnum*14/eaObj.evalbudget
        mc = exp(diff/(-14-tmp))
        if diff < 0 or r<mc:
            oldPose.assign(newPose)
            return True
        return False

def randomizeConformation(eaObj, ipose):
    base = Pose()
    base.assign(ipose)
    for x in range(200):
        tempPose = Pose()
        tempPose.assign(base)
        eaObj.setupMover.apply(tempPose)
        mc(eaObj, tempPose, base, eaObj.score0)
    discardnum = 0
    while discardnum < eaObj.seqlen:
        tempPose = Pose()
        tempPose.assign(base)
        eaObj.setupMover.apply(tempPose)
        if mc(eaObj, tempPose, base, eaObj.score1):
            continue
        else:
            discardnum+=1
    return base
def randomSeed(eaObj, ipose):
    rg_fxn = ScoreFunction()
    rg_fxn.set_weight(core.scoring.rg, 1)
    pose = Pose()
    pose.assign(ipose)
    clash = create_score_function('score3')
    while fabs(rg_fxn(pose)-sqrt(eaObj.seqlen)) > sqrt(eaObj.seqlen)*.6 and clash(pose) >= 150:
        pose.assign(ipose)
        randomizeBB(eaObj, pose)
    ipose.assign(pose)

def randomizeBB(eaObj, pose):
    for i in range(1,eaObj.seqlen+1):
        pose.set_phi(i,randint(-180,180))
        pose.set_psi(i,randint(-180,180))
