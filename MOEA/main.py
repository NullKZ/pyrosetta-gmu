from core import ea
from rosetta import *
from pyrosetta import *
import sys
array_id = sys.argv[1]
filename = sys.argv[2]
score4 = create_score_function('score4_smooth')
for i in range(1):
    main = ea(filename)
    main.run()
    with open("/scratch/kzou/"+main.pdbid+'-'+array_id+'-MOEA.txt', 'a') as f:
        for score in main.rmsdarchive:
            f.write(str(score)+"\n")
        #f.write(str(min(main.energyarchive))+"\n")
        #for pose in main.population:
        #    s = str(core.scoring.CA_rmsd(pose,main.knownNative))+" "+str(score4(pose))+"\n"
        #    f.write(s)
