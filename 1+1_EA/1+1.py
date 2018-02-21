from rosetta import *
from pyrosetta import *
from random import randint, random
from configparser import ConfigParser

config = ConfigParser()
config.read('cfg.ini')
init()

path = "../../Proteins/"
protein = "1ail"
cmd = int(sys.argv[1])

def cprint(color, obj):
    if cmd:
        cmdclist = {'p':'\033[95m','b':'\033[94m','g':'\033[92m','y':'\033[93m','r':'\033[91m','end':'\033[0m','c':'\033[96m'}
        print(cmdclist[color]+str(obj)+'\033[0m')
    else:
        print(obj)

def seq_from_fasta(filepath):
    fastaFile = open(filepath)
    seq = ""
    for line in fastaFile:
        parsedLine = line.strip()
        if parsedLine.startswith('>'):
            continue
        seq+=parsedLine
    return seq

class opo:
    def __init__(self, sequence, frags, deltaE):
        #pose and ΔE
        self.initialPose = pose_from_sequence(seq)
        self.seqlen = len(seq)
        self.dE = deltaE
        #population of 1
        self.current = Pose()
        self.current.assign(self.initialPose)
        #fragments, movemap, and mover
        self.fragments = frags
        self.movemap = MoveMap()
        self.movemap.set_bb(True)
        self.movemap.set_chi(True)
        self.movekmer = protocols.simple_moves.ClassicFragmentMover(self.fragments, self.movemap)
        #score12
        self.score12 = create_score_function('score12_full')
        self.curScore = self.score12(self.current)
        #relaxer
        self.relax = protocols.relax.FastRelax()
        self.relax.set_scorefxn(self.score12)
        #converters
        self.fa2cen = SwitchResidueTypeSetMover("centroid")
        self.cen2fa = protocols.simple_moves.ReturnSidechainMover(self.initialPose)
        #offspring set
        self.oSet = set()
    def runN(self, n):
        for i in range(n):
            cprint('c', "="*100)
            cprint('y', (str(i)+" ")*25)
            cprint('c', "="*100)
            print(self.score12(self.current))
            self.run(i)
    def run(self, it):
        #modify mover range randomly
        tempRangeStart = randint(1,self.seqlen)
        self.movemap.set_bb_true_range(tempRangeStart, tempRangeStart+8)
        self.movemap.set_chi_true_range(tempRangeStart, tempRangeStart+8)
        tempPose = Pose() #select and copy
        tempPose.assign(self.current)
        self.fa2cen.apply(tempPose) #convert to centroid
        self.movekmer.apply(tempPose) #vary with K-mer
        self.cen2fa.apply(tempPose) #revert to fullatom
        self.relax.apply(tempPose) #relax
        tempScore = self.score12(tempPose)
        diff = tempScore - self.curScore
        if diff < 0 or (diff < self.dE and random()>.5):
            self.curScore = tempScore
            self.current.assign(tempPose)
        self.oSet.add(tempPose)
"""
#fragments
fragments = core.fragment.ConstantLengthFragSet(9)
fragments.read_fragment_file(path+"{0}/aat000_09_05.200_v1_3".format(protein))
#sequences
seq = seq_from_fasta(path+"{0}/{0}.fasta".format(protein))
#ea obj
opo_ea = opo(seq, fragments, 3)
opo_ea.runN(5)
opo_ea.current.dump_pdb("Iterations/relaxFinal.pdb")
cprint("c", "Final Score:"+ str(opo_ea.curScore))
"""


