from pyrosetta import *
from rosetta import *

def local(eaObj, pose):
    curScore = eaObj.impScoreFxn(pose)
    eaObj.evalnum+=1
    discardnum = 0
    while discardnum < eaObj.seqlen:
        tempPose = Pose()
        tempPose.assign(pose)
        eaObj.impMover.apply(tempPose)
        tempScore = eaObj.impScoreFxn(tempPose)
        eaObj.evalnum+=1
        if tempScore < curScore:
            curScore = tempScore
            pose.assign(tempPose)
        else:
            discardnum+=1
    del tempPose
    return pose
