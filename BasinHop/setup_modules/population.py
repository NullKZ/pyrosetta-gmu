from pyrosetta import *
from rosetta import *
from math import fabs, sqrt
from random import randint

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
