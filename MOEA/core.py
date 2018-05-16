from rosetta import *
from pyrosetta import *
from random import randint, random
from math import exp, floor, sqrt, fabs
import itertools
import setup
import variation
import improvement
import selection
init()
s4 = create_score_function("score4_smooth")
class pareto_archive:
    #keeps track of all pareto ranks and counts for population
    def __init__(self, eaObj):
        self.ranks = dict()
        self.counts = dict()
        self.eaObj = eaObj
    def pareto_calc(self, pose):
        #returns tuple (short range hbond, long range hbond, and sum of the other terms of score4_smooth)
        self.eaObj.evalnum+=3
        return (self.eaObj.hbond_sr(pose),self.eaObj.hbond_lr(pose),self.eaObj.other(pose))
    def pareto_domination(self, test_pose, base_pose):
        #returns true if the test pose dominates the base pose
        tpc = self.pareto_calc(test_pose)
        bpc = self.pareto_calc(base_pose)
        if tpc[0] < bpc[0] and tpc[1] < bpc[1] and tpc[2] < bpc[2]:
            return True
        return False
    def pareto_count(self, poses, targetpose):
        #returns number of poses that targetpose dominates
        count = 0
        for pose in poses:
            if self.pareto_domination(targetpose, pose):
                count += 1
        return count
    def pareto_rank(self, poses, targetpose):
        #returns number of poses that dominate targetpose
        rank = 0
        for pose in poses:
            if self.pareto_domination(pose, targetpose):
                rank += 1
        return rank
    def update_ranks(self, poses):
        #finds Pareto ranks for each pose in population
        for base, target in itertools.permutations(poses, 2):
            if self.pareto_domination(base, target):
                if base in self.ranks:
                    self.ranks[base]+=1
                else:
                    self.ranks[base]=1
        #for pose in poses:
        #    self.ranks[pose] = self.pareto_rank(poses, pose)
    def update_counts(self, poses):
        #finds Pareto counts for each pose in population
        for base, target in itertools.permutations(poses, 2):
            if self.pareto_domination(target, base):
                if base in self.counts:
                    self.counts[base]+=1
                else:
                    self.counts[base]=1
        #for pose in poses:
        #    self.counts[pose] = self.pareto_count(poses, pose)

class ea:
    def __init__(self, cfg):
        setup.run(self, cfg)
        self.PA = pareto_archive(self)
        self.rmsdarchive = []
    def run(self):
        self.evalnum=0
        while (self.evalnum < self.evalbudget):
            print(self.evalnum)
            self.iterate()
        self.evalnum = 0
    def iterate(self):
        poses = selection.select(self)
        tposes = []
        for pose in poses:
            tempPose = Pose()
            tempPose.assign(pose) #copy pose
            variation.perturb(self, tempPose)
            improvement.run(self, tempPose)
            tposes.append(tempPose)
        for pose in tposes:
            self.rmsdarchive.append(core.scoring.CA_rmsd(pose,self.knownNative))
        self.population = selection.truncate(self, poses, tposes)
