#!/usr/bin/env python
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import Bioinfo
import gzip

read1 = "/projects/bgmp/shared/2017_sequencing/1294_S1_L008_R1_001.fastq.gz"
index1 = "/projects/bgmp/shared/2017_sequencing/1294_S1_L008_R2_001.fastq.gz"
index2 = "/projects/bgmp/shared/2017_sequencing/1294_S1_L008_R3_001.fastq.gz"
read2 = "/projects/bgmp/shared/2017_sequencing/1294_S1_L008_R4_001.fastq.gz"
# indexes = "/projects/bgmp/shared/2017_sequencing/indexes.txt"

# read1 = "./test_r1.fq.gz"
# index1 = "./test_i3.fq.gz"
# index2 = "./test_i2.fq.gz"
# read2 = "./test_r2.fq.gz"

def populate_list(fh,read_length):
    '''Takes in a fastq file with reads of length 101 and
     populates a numpy array with all of the quality scores for each base. '''

    qlist = np.zeros([read_length])
    k=1
    for line in fh:
        if k%4 ==0:
            for i,qscore in enumerate(line.strip()):
                qlist[i]+=qscore-33
            
        k+=1
    counter= k-1
    return qlist,counter


def plot_mean(mean_array,read_length,fh_name):
    '''Takes in a numpy array of means and graphs the distribution, saving the file to a given name'''
    x = range(0,read_length)
    y = mean_array
    plt.plot(x, y)
    plt.xlabel('Base', fontsize=15)
    plt.ylabel('Mean Quality Score', fontsize=15)
    plt.savefig("mean_distribution_"+str(fh_name)+".png")
    plt.close()



r1_f = gzip.open(read1)
r2_f = gzip.open(read2)
i1_f = gzip.open(index1)
i2_f = gzip.open(index2)

L_r1, c_r1 = populate_list(r1_f,101)
L_r2, c_r2 = populate_list(r2_f,101)
L_i1, c_i1 = populate_list(i1_f,8)
L_i2, c_i2 = populate_list(i2_f,8)


mean_r1 = L_r1/(c_r1/4)
mean_r2 = L_r2/(c_r2/4)
mean_i1 = L_i1/(c_i1/4)
mean_i2 = L_i2/(c_i2/4)


plot_mean(mean_r1,101,"read_1")
plot_mean(mean_r2,101,"read_2")
plot_mean(mean_i1,8,"index_1")
plot_mean(mean_i2,8,"index_2")

r1_f.close()
r2_f.close()
i1_f.close()
i2_f.close()