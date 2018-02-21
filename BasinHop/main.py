from core import ea
from rosetta import *
from pyrosetta import *
import sys
array_id = sys.argv[1]
for i in range(1250):
    main = ea('cfg.ini')
    main.run()
    with open(main.pdbid+'-'+array_id+'-PLOW_Vary9mer-Imp3mer-4Phase-Relax.txt', 'a') as f:
        relaxScore = create_score_function('score12_full')
        relax = protocols.relax.FastRelax()
        relax.set_scorefxn(relaxScore)
        main.cen2fa.apply(main.minState)
        relax.apply(main.minState)
        s = str(core.scoring.CA_rmsd(main.minState,main.knownNative))+" "+str(main.minScore)+"\n"
        f.write(s)
        if main.minScore < .5 and main.minScore > -.5:
            main.minState.dump_pdb(main.pdbid+"_0EnergyPose_"+array_id+"_"+str(i))