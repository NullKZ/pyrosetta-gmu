#!/bin/sh
## Job name
#SBATCH --job-name hea1ail
## Partition name
#SBATCH --partition all-LoPri
## Estimated Time Required in the format D-HH:MM:SS
#SBATCH --time 4-00:00:00
#SBATCH --array=1-5
#SBATCH -o /scratch/kzou/.outerr-%j
#SBATCH -e /scratch/kzou/.output-%j
#SBATCH --mail-type=FAIL
#SBATCH --mail-user=kzou@gmu.edu
## Finally your executable line
module load pyrosetta
python main.py $SLURM_ARRAY_TASK_ID 1ail.ini > /dev/null
