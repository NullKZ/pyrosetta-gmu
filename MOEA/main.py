from core import ea
from rosetta import *
from pyrosetta import *
import sys
array_id = sys.argv[1]
score4 = create_score_function('score4_smooth')
for i in range(10):
    main = ea('cfg.ini')
    main.run()
    with open(main.pdbid+'-'+array_id+'-MOEA_100.txt', 'a') as f:
        for pose in main.population:
            s = str(core.scoring.CA_rmsd(pose,main.knownNative))+" "+str(score4(pose))+"\n"
            f.write(s)