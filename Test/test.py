#cmd color
cmd = True
def cprint(color, obj):
    if cmd:
        cmdclist = {'p':'\033[95m','b':'\033[94m','g':'\033[92m','y':'\033[93m','r':'\033[91m','end':'\033[0m','c':'\033[96m'}
        print(cmdclist[color]+str(obj)+'\033[0m')
    else:
        print(obj)
from rosetta import *
from pyrosetta import *
from pyrosetta.toolbox import cleanATOM
init()
protein = "1ail"
#Clean PDB, output as *.clean.pdb
cleanATOM("../../Proteins/1ail/"+protein+".pdb")
#load molecule * as fullatom default, create backup of initial
#pose = pose_from_pdb(protein+".clean.pdb")
pose = pose_from_sequence("MDSNTVSSFQVDCFLWHVRKQVVDQELGDAPFLDRLRRDQKSLRGRGSTLGLNIEAATHVGKQIVEKILKEED")
poseInitial = Pose()
poseInitial.assign(pose)
#score functions
score3 = create_score_function('score3')
#pose converter fa -> cen
fullatom2centroid = SwitchResidueTypeSetMover("centroid")
#display pose
cprint('c', '---------------- FullAtom Pose ----------------')
cprint('y', str(pose))
#convert pose to centroid
fullatom2centroid.apply(pose)
#show weights
cprint('c', '--------- score3 weights ----------')
score3.show(pose)
#run scoring using scorefunction score3
cprint('c', '------ score3 evaluation ----------')
cprint('y', str(score3(pose)))
#create fragment set
fragments = core.fragment.ConstantLengthFragSet(9)
fragments.read_fragment_file("../../Proteins/1ail/aat000_09_05.200_v1_3")
#make movemap
movemap = MoveMap()
movemap.set_bb(True)
movemap.set_chi(True)
#mover function using fragments and movemap
move9mer = protocols.simple_moves.ClassicFragmentMover(fragments, movemap)
#re-evaluate until < a
move9mer.apply(pose)
minimum = 1e9
while minimum>80:
    move9mer.apply(pose)
    s = score3(pose)
    if s<minimum:
        minimum = s
    print('\r'+str(s), end="")
print()
score3.show(pose)
