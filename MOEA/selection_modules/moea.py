from time import time
from pyrosetta import *
from rosetta import *
init()
score4 = create_score_function('score4_smooth')

def moea(eaObj):
    return eaObj.population

def truncate(eaObj, poses, tposes):
    #merged_population = poses+tposes
    #t0 = time()
    #eaObj.PA.update_ranks(merged_population)
    #eaObj.PA.update_counts(merged_population)
    #print("R/C Updated in "+str(time()-t0))
    poses.sort(key=lambda x: score4(x))
    tposes.sort(key=lambda x: score4(x))
    return poses[:25]+tposes[:75]
