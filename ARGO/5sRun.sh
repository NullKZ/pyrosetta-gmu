#!/bin/sh
## Job name
#SBATCH --job-name 5sRun
## Partition name
#SBATCH --partition all-HiPri
## Estimated Time Required in the format D-HH:MM:SS
#SBATCH --time 0-00:00:05
## Name of output file (console output from your executable is written here)
## %N= node name, %j=job id
#SBATCH -o slurm-%N-%j.out
## Name of error file
#SBATCH -e slurm-%N-%j.err
## Email the user of job status
## < JobStatusCode> = NONE, BEGIN, END, FAIL, REQUEUE, ALL etc.
#SBATCH --mail-type=FAIL
#SBATCH --mail-user=kzou@gmu.edu
## Finally your executable line
python3.5 5srun.py
