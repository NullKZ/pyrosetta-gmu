from rosetta import *
from pyrosetta import *
from random import randint, random
from configparser import ConfigParser
from time import time
from math import exp, floor, sqrt, fabs
from statistics import median
init()

def seq_from_fasta(filepath):
    fastaFile = open(filepath)
    seq = ""
    for line in fastaFile:
        parsedLine = line.strip()
        if parsedLine.startswith('>'):
            continue
        seq+=parsedLine
    return seq

class ea:
    def __init__(self, cfgpath):
        self.pymol = PyMOLMover()
        #config parser
        self.cfg = ConfigParser()
        self.cfg.optionxform = lambda option: option
        self.cfg.read(cfgpath)
        #initial setup
        initcfg = self.cfg['init']
        self.genN = int(initcfg['nGen'])
        self.pdbid = initcfg['protein']
        path = initcfg['path']
        if initcfg['initState'] == 'line':
            self.sequence = seq_from_fasta(path+"{0}/{0}.fasta".format(self.pdbid))
            self.initialPose = pose_from_sequence(self.sequence)
        elif initcfg['initState'] == 'pdb':
            self.initialPose = pose_from_pdb(path+"{0}/{0}.pdb")
        elif initcfg['initState'] == 'sequence':
            self.sequence = initcfg['sequence']
            self.initialPose = pose_from_sequence(self.sequence)
        else:
            raise Exception("Unrecognized initState!")
            return
        self.seqlen = len(self.initialPose.sequence())
        self.population = []
        for i in range(int(initcfg['population'])):
            temporaryPose = Pose()
            temporaryPose.assign(self.initialPose)
            self.population.append(temporaryPose)
        #evaluation tracking
        self.evalnum = 0
        self.evalbudget = int(initcfg['evalbudget'])
        self.knownNative = pose_from_pdb(path+"{0}/{0}.pdb".format(self.pdbid))
        #variation setup
        varcfg = self.cfg['variation']
        if varcfg['fragReplacement'] == 'True':
            self.fragLength = int(varcfg['fragLength'])
            self.fragments = core.fragment.ConstantLengthFragSet(self.fragLength)
            self.fragments.read_fragment_file(path+"{0}/aat000_0{1}_05.200_v1_3".format(self.pdbid, self.fragLength))
            self.movemap = MoveMap()
            self.movemap.set_bb(True)
            self.movemap.set_chi(True)
            self.movekmer = protocols.simple_moves.ClassicFragmentMover(self.fragments, self.movemap)
        #3mer frag setup
        self.frag3mer = core.fragment.ConstantLengthFragSet(3)
        self.frag3mer.read_fragment_file(path+"{0}/aat000_0{1}_05.200_v1_3".format(self.pdbid, 3))
        self.move3mer = protocols.simple_moves.ClassicFragmentMover(self.frag3mer, self.movemap)
        #9mer frag setup
        self.frag9mer = core.fragment.ConstantLengthFragSet(9)
        self.frag9mer.read_fragment_file(path+"{0}/aat000_0{1}_05.200_v1_3".format(self.pdbid, 9))
        self.move9mer = protocols.simple_moves.ClassicFragmentMover(self.frag3mer, self.movemap)
        #small mover
        movemapmover = MoveMap()
        movemapmover.set_bb(True)
        movemapmover.set_chi(True)
        self.smallmover = protocols.simple_moves.SmallMover(movemapmover, 5.0, 1)
        self.smallmover.angle_max("H", 360)
        self.smallmover.angle_max("E", 360)
        self.smallmover.angle_max("L", 360)
        #improvement setup
        impcfg = self.cfg['improvement']
        try:
            self.score = create_score_function(impcfg['scorefxn'])
        except Exception:
            raise Exception("Unrecognized scorefxn!")
            return
        self.plow = False
        if impcfg['relaxtype'] == 'fast':
            self.relax = protocols.relax.FastRelax()
        elif impcfg['relaxtype'] == 'classic':
            self.relax = protocols.relax.ClassicRelax()
        elif impcfg['relaxtype'] == 'centroid':
            self.relax = protocols.relax.CentroidRelax()
        elif impcfg['relaxtype'] == 'plow':
            self.plow = True
        else:
            raise Exception("Unrecognized relaxtype!")
            return
        self.dE = float(impcfg['dE'])
        if not self.plow:
            self.relax.set_scorefxn(self.score)
        #converters
        self.fa2cen = SwitchResidueTypeSetMover("centroid")
        self.cen2fa = protocols.simple_moves.ReturnSidechainMover(self.initialPose)
        if impcfg['representation'] == 'centroid':
            self.fa2cen.apply(self.initialPose)
            for pose in self.population:
                self.fa2cen.apply(pose)
        #offspring set
        self.oSet = set()
        #mintracker
        self.minScore = 1e9
        self.minState = Pose()
        #intelligent seed
        if int(initcfg['randomseed']):
            self.randomizeBBConformation()
    def randomizeBBConformation(self):
        t1 = time()
        rg_fxn = ScoreFunction()
        rg_fxn.set_weight(core.scoring.rg, 1)
        clash = create_score_function('score3')#ScoreFunction()
        #clash.set_weight(core.scoring.vdw, 1)
        pose = Pose()
        while fabs(rg_fxn(pose)-sqrt(self.seqlen)) > sqrt(self.seqlen)*.6:
            pose.assign(self.population[0])
            while clash(pose) >= 150:
                for i in range(1,self.seqlen+1):
                    pose.set_phi(i,randint(-180,180))
                    pose.set_psi(i,randint(-180,180))
        self.selection().assign(pose)
        print("Randomized Seed in",time()-t1)
    def selection(self):
        if self.cfg['selection']['type'] == 'opo':
            return self.population[0]
    def keepBest(self, pose1, pose2):
        posepair = (pose1,pose2)
        tempScore = self.score(posepair[0])
        diff = tempScore - self.score(posepair[1])
        self.evalnum += 2
        r = random()
        mc = exp(diff/-28.8539008178)
        if diff < 0 or r<mc:
            self.population[0].assign(posepair[0])
        if (tempScore < self.minScore):
            self.minScore = tempScore
            self.minState.assign(posepair[0])
        #self.oSet.add(posepair[0])
    def improvement(self, pose):
        if self.plow:
            self.pyPLOW(pose)
        else:
            self.relax.apply(pose) #relax
    def vary(self, pose):
        if self.plow:
            self.move9mer.apply(pose)
        else:
            self.movekmer.apply(pose)
    def pyPLOW(self, current):
        curScore = self.score(current)
        self.evalnum+=1
        discardnum = 0
        while discardnum < 20:#self.seqlen:
            tempPose = Pose()
            tempPose.assign(current)
            self.vary(tempPose)
            tempScore = self.score(tempPose)
            self.evalnum+=1
            if tempScore < curScore:
                curScore = tempScore
                current.assign(tempPose)
            else:
                discardnum+=1
        del tempPose
        return current
    def run(self):
        i=0
        self.evalnum=0
        self.time = time()
        stagecfg = self.cfg['stages']
        for j in range(1,5):
            if str(j) in stagecfg['skip']:
                continue
            self.score = create_score_function(stagecfg['s'+str(j)+'scorefxn'])
            while (self.evalnum / self.evalbudget) < float(stagecfg['s'+str(j)+'weight']):
                i+=1
                self.iterate(i)
                print("\r > "+str(format(self.evalnum*100/self.evalbudget, ".2f"))+"%\t",end="")
            self.evalnum = 0
        print("-"*20)
        self.time = (time()-self.time)/i
    def iterate(self, i):
        selectedPose = self.selection() #select
        tempPose = Pose()
        tempPose.assign(selectedPose) #copy pose
        self.movekmer.apply(tempPose) #vary
        self.improvement(tempPose)
        self.keepBest(tempPose,selectedPose)
for i in range(100):
    main = ea('cfg.ini')
    main.run()
    with open(main.pdbid+'PLOW_9mer-1Phase.txt', 'a') as f:
        print(core.scoring.CA_rmsd(main.minState,main.knownNative), main.minScore, file=f)
