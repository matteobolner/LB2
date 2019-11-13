import sys 
import os
from pathlib import Path


def get_fasta_from_extracted(dssp_extracted_folder, id_file):
    open_id_file = open(id_file, "r")
    id_chain_dict = {}
    for line in open_id_file:
        b = line.rstrip().split("_")
        id_chain_dict[b[0]] = b[1]
    
    complete_bs = open("complete_bs.fasta", "a")
    
    for file in os.listdir(dssp_extracted_folder):
        df = str(dssp_extracted_folder) + "/" + file
        dssp_file_path = Path(df)
        file_id_only = file.split(".")[0]
        #print(file_id_only)
        ff = str(fasta_files_folder) + "/" + file_id_only + "_" + id_chain_dict[file_id_only]
        fasta_file_path = Path(ff)
        a = dssp_file_path.open()  
        id_and_fasta_file = open(fasta_file_path, "r")
        for line in id_and_fasta_file:
            cleanline = line.rstrip()
            #print(cleanline)
            print(len(cleanline))
            complete_bs.write(line)

        ss_seq_string = ""

        for line in a:
            splitted_line = line.split(":")
            
            chain = splitted_line[0]
            #print(chain)
            #print(id_chain_dict[file_id_only])
            if chain == id_chain_dict[file_id_only]:
                ss_seq = splitted_line[2]
                ss_seq_string += ss_seq
        #print(ss_seq_string)
        print(len(ss_seq_string))

        complete_bs.write(ss_seq_string + "\n")
        
    return()

''' situation at the moment: the program works as intended but there is the problem of pdb sequences being different from the fasta obtained from pdb; the best solution apparently is to just delete all sequences with different sequences, which would mean adding other new sequences fromt the "whole" blind set
OR, another solution could be to just use the dssp for both sequence and ss, putting the aa sequence in all caps to avoid the problem with the bisulpide bonds '''


if __name__ == "__main__":
    dssp_extractedfolder = sys.argv[1]
    id_file = sys.argv[2]
    fasta_files_folder = sys.argv[3]
    get_fasta_from_extracted(dssp_extractedfolder, id_file, fasta_files_folder)