#!/usr/bin/env python
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import Bioinfo
import gzip
import argparse

#Get required variables 
parser = argparse.ArgumentParser(description="TBD")
parser.add_argument("-r1", "--r1_filename", help="filename for read1", required=True)
parser.add_argument("-r2", "--r2_filename", help="file name for read2", required=True)
parser.add_argument("-i1", "--i1_filename", help="file name for index1", required=True)
parser.add_argument("-i2", "--i2_filename", help="file name for index2", required=True)
parser.add_argument("-in", "--index_filename", help="file name for index barcodes", required=True)
# parser.add_argument("-d", "--output_dir", help="directory for outputs", required=True)
args = parser.parse_args()

#Convert to strings
r1_file_name=str(args.r1_filename)
r2_file_name=str(args.r2_filename)
i1_file_name=str(args.i1_filename)
i2_file_name=str(args.i2_filename)
i_file_name= str(args.index_filename)
# output_dir= "./"+str(args.output_dir)

#Read in the 2 read fastq files and 2 index fastq files
r1_fh = open(r1_file_name)
r2_fh = open(r2_file_name)
i1_fh = open(i1_file_name)
i2_fh = open(i2_file_name)



#Open Index file and create a dictionary to store the index and index sequence
ind_fh = open(i_file_name)
#Key= index sequence, Value = index
ind_dict = {}


first = 1 #use to skip first line
while True:
    this_line = ind_fh.readline()
    if (this_line == ""):
        break
    if (first == 1):
        first+=1
    else:
        this_ind = str.split(this_line.strip(), sep="\t")
        #Add index sequence and index to dictionary
        
        r1=open("./out_dir/"+str(this_ind[3]) + "_read1.fq","w")
        r2=open("./out_dir/"+str(this_ind[3]) + "_read2.fq","w")
        read_list=[r1,r2]
        
        ind_dict[this_ind[4]] = read_list











#Close all output files
for i in ind_dict:
    ind_dict[i][0].close()
    ind_dict[i][1].close()

#Close input files
r1_fh.close()
r2_fh.close()
i1_fh.close()
i2_fh.close()
ind_fh.close()
