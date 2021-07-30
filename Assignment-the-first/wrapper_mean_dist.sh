#!/bin/bash

#SBATCH --partition=bgmp        ### Partition (like a queue in PBS)
#SBATCH --job-name=mean_dist   ### Job Name
#SBATCH --output=mean_dist_%j.out         ### File in which to store job output
#SBATCH --error=mean_dist_%j.err          ### File in which to store job error messages
#SBATCH --time=0-12:01:00       ### Wall clock time limit in Days-HH:MM:SS
#SBATCH --nodes=1              ### Number of nodes needed for the job
#SBATCH --ntasks-per-node=8    ### Number of tasks to be launched per node
#SBATCH --account=bgmp      ### Account used for job submission

conda activate bgmp_py39

/usr/bin/time -v python3 ./mean_dist.py