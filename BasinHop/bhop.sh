#!/bin/sh
## Job name
#SBATCH --job-name bh-ex1p
## Partition name
#SBATCH --partition all-LoPri
## Estimated Time Required in the format D-HH:MM:SS
#SBATCH --time 0-12:00:00
#SBATCH --array=1-8
#SBATCH -o .outerr-%j
#SBATCH -e .outBH-%j
#SBATCH --mail-type=FAIL
#SBATCH --mail-user=kzou@gmu.edu
## Finally your executable line
module load pyrosetta/4.0-py3.6-r153
python main.py $SLURM_ARRAY_TASK_ID > /dev/null
