# Demultiplexing   

*version# 0.9*
</br>  

Author: Natalie Elphick   
</n>  
Script to demultiplex samples that have been dual indexed and summarize the percentage of matched indexes and hopped indexes.   
</n>   

#

Requirements: 
```
Bioinfo   
gzip   
argparse    
```
</br>

To use this script      
1) Demux.py has required arguments.  
</t> i) -r1,-r2 = The path of the read files.  
</t> ii) -i1,-i2 = The path of the index files.   
</t> iii) -in = the path to the indexes file. 
```
Note : The -in file must be tab delimited and must have the index in column 4 and index sequence in column 5.   
```
 
2) The script will output the matched read files in a new directory "out_dir" and a "stats.txt" with a high level summary of the output, be sure to rename these files if you want to preserve them and rerun the script.