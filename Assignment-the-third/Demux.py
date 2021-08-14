#!/usr/bin/env python
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
r1_fh = gzip.open(r1_file_name,"rt")
r2_fh = gzip.open(r2_file_name,"rt")
i1_fh = gzip.open(i1_file_name,"rt")
i2_fh = gzip.open(i2_file_name,"rt")

#Bad indexes (contains N or Index not found in indexes file)
garbage_fh = gzip.open("./out_dir/garbage_indexes.fq.gz","wt")

#Hopped indexes files
r1_hopped_fh = gzip.open("./out_dir/r1_hopped.fq.gz","wt")
r2_hopped_fh = gzip.open("./out_dir/r2_hopped.fq.gz","wt")

#Stats file
stats_fh = open("stats.txt","w")




#Open Index file and create a dictionary to store the index and index sequence
ind_fh = open(i_file_name)
#Key= index sequence, Value = list [read1 file object, read2 file object]
ind_dict = {}

#Key= index sequence, Value = list[SampleID, Count of matched reads]
count_matched = {}

first = 1 #use to skip first line
while True:
    this_line = ind_fh.readline()
    if (this_line == ""):
        break
    if (first == 1):
        first+=1
    else:
        #Split the tsv lines by tab
        this_ind = str.split(this_line.strip(), sep="\t")

        #Add index sequence and output file objects to dictionary        
        r1=gzip.open("./out_dir/"+str(this_ind[3]) + "_read1.fq.gz","wt")
        r2=gzip.open("./out_dir/"+str(this_ind[3]) + "_read2.fq.gz","wt")
        read_list=[r1,r2]
        count_list=[this_ind[3],0]
        
        ind_dict[this_ind[4]] = read_list
        count_matched[this_ind[4]] = count_list


#Initialize empty strings to hold each element of the outputs
r1_header=""
r2_header=""
i1_header=""
i2_header=""

i1_qscores ="" 
i2_qscores =""
r1_qscores ="" 
r2_qscores =""

r1_seq_line = ""
r2_seq_line = ""
i1_seq_line = ""
i2_seq_line = ""

#To count reads for each bin
read_count=0
hopped=0
bad_index=0




#Line counters to pull the correct lines using modulo
line_counter = 1
lc2 = 0
while True:
    #Read the files a line at a time
    r1_thisline = r1_fh.readline().strip()
    if (r1_thisline == ""): #break at the end of th read1 file
        break
    
    r2_thisline = r2_fh.readline().strip()
    i1_thisline = i1_fh.readline().strip()
    i2_thisline = i2_fh.readline().strip()


    #Pull header lines
    if (lc2%4 == 0):
        r1_header = r1_thisline
        r2_header = r2_thisline
        i1_header = i1_thisline
        i2_header = i2_thisline

    #Pull qscore lines
    if (line_counter%4 == 0):
        #Store index qscore lines
        i1_qscores =  i1_thisline 
        i2_qscores =  i2_thisline
        r1_qscores =  r1_thisline 
        r2_qscores =  r2_thisline

    #Pull sequence lines
    if (lc2%4 == 1):
        #Store all sequence lines
        r1_seq_line = r1_thisline
        r2_seq_line = r2_thisline
        i1_seq_line = i1_thisline
        i2_seq_line = i2_thisline
    line_counter+=1
    lc2+=1
    
    #Start checking indexes after the qscores are read in
    if len(i1_qscores) != 0:
        read_count+=1

        #reverse complement of index2
        revcomp_i2 = Bioinfo.revcomp(i2_seq_line)

        #For any index with an N, write read1 and read2 to the "garbage" file
        if "N" in i1_seq_line or "N" in i2_seq_line: #Move out to make faster
                
            garbage_fh.write(r1_header + "\n")
            garbage_fh.write(r1_seq_line + "\n")
            garbage_fh.write("+"+"\n")
            garbage_fh.write(r1_qscores + "\n")

            garbage_fh.write(r2_header + "\n")
            garbage_fh.write(r2_seq_line + "\n")
            garbage_fh.write("+"+"\n")
            garbage_fh.write(r2_qscores + "\n")
            bad_index+=1
            #print("garbage")

        elif i1_seq_line != revcomp_i2: # Do i1 and i2 match?
        
            if i1_seq_line not in ind_dict and revcomp_i2 not in ind_dict: # If one of the indexes doesn't exist
                
                garbage_fh.write(r1_header + "\n")
                garbage_fh.write(r1_seq_line + "\n")
                garbage_fh.write("+"+"\n")
                garbage_fh.write(r1_qscores + "\n")

                garbage_fh.write(r2_header + "\n")
                garbage_fh.write(r2_seq_line + "\n")
                garbage_fh.write("+"+"\n")
                garbage_fh.write(r2_qscores + "\n")
                bad_index+=1
                #print("bad index")
            else: #If the indexes dont match and if it is not a bad index
                
                r1_hopped_fh.write(r1_header + " "+ str(i1_seq_line)+ "-"+str(i2_seq_line) +"\n")
                r1_hopped_fh.write(r1_seq_line + "\n")
                r1_hopped_fh.write("+"+"\n")
                r1_hopped_fh.write(r1_qscores + "\n")

                r2_hopped_fh.write(r2_header + " "+ str(i1_seq_line)+ "-"+str(i2_seq_line) +"\n")
                r2_hopped_fh.write(r2_seq_line + "\n")
                r2_hopped_fh.write("+"+"\n")
                r2_hopped_fh.write(r2_qscores + "\n")
                #print("hopped")
                hopped+=1
        elif i1_seq_line not in ind_dict: # if they match but don't exist
            #print("bad index")
            garbage_fh.write(r1_header + "\n")
            garbage_fh.write(r1_seq_line + "\n")
            garbage_fh.write("+"+"\n")
            garbage_fh.write(r1_qscores + "\n")

            garbage_fh.write(r2_header + "\n")
            garbage_fh.write(r2_seq_line + "\n")
            garbage_fh.write("+"+"\n")
            garbage_fh.write(r2_qscores + "\n")
            bad_index+=1
        else: # Sort reads into correct file
            #print("match")
            #print(ind_dict[i1_seq_line][0])
            #print(ind_dict[i1_seq_line][1])
            ind_dict[i1_seq_line][0].write(r1_header +" "+ str(i1_seq_line)+ "-"+str(i2_seq_line) + "\n")
            ind_dict[i1_seq_line][0].write(r1_seq_line + "\n")
            ind_dict[i1_seq_line][0].write("+"+"\n")
            ind_dict[i1_seq_line][0].write(r1_qscores + "\n")

            ind_dict[i1_seq_line][1].write(r2_header +" "+ str(i1_seq_line)+ "-"+str(i2_seq_line) + "\n")
            ind_dict[i1_seq_line][1].write(r2_seq_line + "\n")
            ind_dict[i1_seq_line][1].write("+"+"\n")
            ind_dict[i1_seq_line][1].write(r2_qscores + "\n")
            count_matched[i1_seq_line][1]+=1
            

stats_fh.write("Number of Bad Indexes: "+str(bad_index)+"\n")
stats_fh.write("Number of Hopped Indexes: "+str(hopped)+ "\n")
stats_fh.write("Number of Reads: "+str(read_count)+"\n")

for i in count_matched:
    stats_fh.write("Sample "+ str(count_matched[i][0]) +"  matched read %: "+str(count_matched[i][1]/read_count *100)+"\n")



#Close all output files
for i in ind_dict:
    ind_dict[i][0].close()
    ind_dict[i][1].close()

stats_fh.close()
garbage_fh.close()
r1_hopped_fh.close()
r2_hopped_fh.close()

#Close input files
r1_fh.close()
r2_fh.close()
i1_fh.close()
i2_fh.close()
ind_fh.close()
