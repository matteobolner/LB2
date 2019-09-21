import sys
import os
from collections import Counter 
import pandas as pd
import matplotlib.pyplot as plt

def aa_composition(fasta_folder):
    f = fasta_folder
    for fasta_filename in os.listdir(f):
        fasta_file = open(fasta_filename, "r")
        for line in fasta_file:
            stripped_line = line.rstrip()
            if line[0] == ">" :
                continue
            else:       
                aa_counter = Counter(stripped_line)
                print(aa_counter)


    return()

if __name__ == "__main__":
    fasta_folder = sys.argv[1]
    aa_composition(fasta_folder)