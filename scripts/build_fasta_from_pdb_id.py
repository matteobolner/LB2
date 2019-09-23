#this script takes as input a list of PDB IDs and a fasta file of PDB sequences, and outputs a fasta file of the input IDs associated with their sequence

import sys

def create_id_list(id_file):
    f = open(id_file)
    id_list = []
    for line in f:
        pdb_id = line.rstrip()
        if pdb_id != ['']:              #avoid appending empty elements to the ID list
            id_list.append(pdb_id)
    return(id_list)

def get_fasta_from_id(id_file, sequences_file, output_file):
    k = create_id_list(id_file)    
    g = open(sequences_file)
    h = open(output_file, 'a')
    for line in g:
        stripped_line = line.rstrip()
        if stripped_line[0] == '>':
            splitted_line = stripped_line.split('>')            
        if splitted_line[1] in k:
            c = 1
        else:
            c = 0
        if c == 1:
            h.write(line)

if __name__ == "__main__":
    id_file = sys.argv[1]
    sequences_file = sys.argv[2]
    output_file = sys.argv[3]
    get_fasta_from_id(id_file, sequences_file, output_file) 
