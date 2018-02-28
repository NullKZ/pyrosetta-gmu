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
        mc = exp(diff/-20)
        if diff < 0 or r<mc:
            oldPose.assign(newPose)
        if (tempScore < self.minScore):
            self.minScore = tempScore
            self.minState.assign(newPose)
    def pareto_calc(self, pose):
        #returns tuple (short range hbond, long range hbond, and sum of the other terms of score4_smooth)
        return (self.hbond_sr(pose),self.hbond_lr(pose),self.other(pose))
    def pareto_domination(self, test_pose, base_pose)
        #returns true if the test pose dominates the base pose
        tpc = self.pareto_calc(test_pose)
        bpc = self.pareto_calc(base_pose)
        if tpc[0] < bpc[0] and tpc[1] < bpc[1] and tpc[2] < bpc[2]:
            return True
        return False
    def pareto_count(self, targetpose):
        poses = selection.select(self)
        rank = 0
        for pose in poses:
            if self.pareto_domination(targetpose, pose)
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
        poses = selection.select(self)
        popsize = len(poses)
        tposes = []
        for pose in poses:
            tempPose = Pose()
            tempPose.assign(pose) #copy pose
            variation.perturb(self, tempPose)
            improvement.run(self, tempPose)
            tposes.append(tempPose)
        #poses.sort(key=lambda x: self.score(x))
        #tposesc.sort(key=lambda x: self.score(x))
        merged_population = poses+tposes
        merged_population.sort(key=lambda x: self.score(x))
        self.population = merged_population[:(popsize/2)]