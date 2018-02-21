from rosetta import *
from pyrosetta import *
from random import randint, random
from math import exp, floor, sqrt, fabs

import setup
import variation
import improvement
import selection
init()
class ea:
    def __init__(self, cfg):
        setup.run(self, cfg)
    #metropolis criterion
    def mc(self, newPose, oldPose):
        tempScore = self.score(newPose)
        diff = tempScore - self.score(oldPose)
        self.evalnum += 2
        r = random()
        mc = exp(diff/-28.8539008178)
        if diff < 0 or r<mc:
            oldPose.assign(newPose)
        if (tempScore < self.minScore):
            self.minScore = tempScore
            self.minState.assign(newPose)
    def run(self):
        self.evalnum=0
        stagecfg = self.cfg['stages']
        for j in range(1,5):
            if str(j) in stagecfg['skip']:
                continue
            self.score = create_score_function(stagecfg['s'+str(j)+'scorefxn'])
            while (self.evalnum / self.evalbudget) < float(stagecfg['s'+str(j)+'weight']):
                self.iterate()
            self.evalnum = 0
    def iterate(self):
        pose = selection.select(self)
        tempPose = Pose()
        tempPose.assign(pose) #copy pose
        variation.perturb(self, tempPose)
        improvement.run(self, tempPose)
        self.mc(tempPose,pose)
