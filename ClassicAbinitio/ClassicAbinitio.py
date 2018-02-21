from rosetta import *
from pyrosetta import *
init()
for i in range(100):
    protein = "1ail"
    frag3 = core.fragment.ConstantLengthFragSet(3)
    frag3.read_fragment_file("../../Proteins/"+protein+"/aat000_03_05.200_v1_3")
    frag9 = core.fragment.ConstantLengthFragSet(9)
    frag9.read_fragment_file("../../Proteins/"+protein+"/aat000_09_05.200_v1_3")
    movemap = MoveMap()
    movemap.set_bb(True)
    movemap.set_chi(True)
    ab = protocols.abinitio.ClassicAbinitio(frag3,frag9,movemap)
    pose = pose_from_pdb("../../Proteins/"+protein+"/"+protein+".pdb")
    seq = "MDSNTVSSFQVDCFLWHVRKQVVDQELGDAPFLDRLRRDQKSLRGRGSTLGLNIEAATHVGKQIVEKILKEED"#pose.sequence()
    pose = pose_from_sequence(seq)
    fa2cen = SwitchResidueTypeSetMover('centroid')
    fa2cen.apply(pose)
    ab.bSkipStage5_ = True
    ab.init(pose)
    ab.apply(pose)
    score = create_score_function('score3')
    native = pose_from_pdb("../../Proteins/"+protein+"/"+protein+".pdb")
    fa2cen.apply(native)
    with open(protein+'CA.txt', 'a') as f:
        print(core.scoring.CA_rmsd(pose,native), score(pose), file=f)
