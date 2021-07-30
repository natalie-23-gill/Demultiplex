#!/bin/bash

#SBATCH --partition=bgmp        ### Partition (like a queue in PBS)
#SBATCH --job-name=demux_p1   ### Job Name
#SBATCH --output=demux_p1_%j.out         ### File in which to store job output
#SBATCH --error=demux_p1_%j.err          ### File in which to store job error messages
#SBATCH --time=0-12:01:00       ### Wall clock time limit in Days-HH:MM:SS
#SBATCH --nodes=1              ### Number of nodes needed for the job
#SBATCH --ntasks-per-node=8    ### Number of tasks to be launched per node
#SBATCH --account=bgmp      ### Account used for job submission

conda activate bgmp_py39

/usr/bin/time -v python3 ./part1.py -r1 /projects/bgmp/shared/2017_sequencing/1294_S1_L008_R1_001.fastq.gz \
-r2 /projects/bgmp/shared/2017_sequencing/1294_S1_L008_R4_001.fastq.gz \
-i1 /projects/bgmp/shared/2017_sequencing/1294_S1_L008_R2_001.fastq.gz \
-i2 /projects/bgmp/shared/2017_sequencing/1294_S1_L008_R3_001.fastq.gz \
-in /projects/bgmp/shared/2017_sequencing/indexes.txt