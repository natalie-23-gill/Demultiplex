#!/user/bin/env python

#Module for adding functions for Bi621 and Bi622 assignments
import gzip

DNAbases="ATGCNatcgn"
RNAbases= "AUGCNnaucg"
def validate_base_seq(seq,RNAflag=False):
    '''This function takes a string. Returns True if string is composed
    of only As, Ts (or Us if RNAflag), Gs, Cs. False otherwise. Case insensitive.'''
    DNAbases = set('ATGCatcg')
    RNAbases = set("AUGCNnaucg")
    return set(seq)<=(RNAbases if RNAflag else DNAbases)

def convert_phred33(letter):
    """Converts a single character into a phred score"""
    return ord(letter)-33 #phred+33 encoding

def init_list(lst: list, value: float=0.0) -> list:
    '''This function takes an empty list and will populate it with
    the value passed in "value". If no value is passed, initializes list
    with 101 values of 0.0.'''
    
    lst = [value for i in range(101)]
    return lst

def populate_list(file):
    """Takes a fastq and converts the phred scores from each record to numbers and stores them in a list,
    returns array and counter"""

    qlist = init_list([])
    k=1
    with open(file,"r") as fh:
        for line in fh:
            if k%4 ==0:
                for i,qscore in enumerate(line.strip()):
                    
                    qlist[i]+=convert_phred33(qscore)
                    
            k+=1
        counter= k-1
        return qlist,counter

def populate_list_gz(file):
    """Takes a fastq and converts the phred scores from each record to numbers and stores them in a list,
    returns array and counter"""

    qlist = init_list([])
    k=1
    with gzip.open(file) as fh:
        for line in fh:
            if k%4 ==0:

                for i,qscore in enumerate(line.strip()):
                    qlist[i]+=(qscore-33)
                    
            k+=1
        counter= k-1
        return qlist,counter


def complement(letter):   
        ''' Takes in a letter and
         returns complimentary bases'''   
        letter=letter.upper()
        bases_dict={
            'A':'T',
            'T':'A',
            'G':'C',
            'C':'G',
            'N':'N'
        }    
        return bases_dict.get(letter)

def revcomp(sequence_line):   
    '''Takes in a sequence line of ATCGNs and returns the reverse complement'''   
    reverse_seq=""
    for letter in sequence_line[::-1]:
        reverse_seq+= complement(letter) 
    return reverse_seq
