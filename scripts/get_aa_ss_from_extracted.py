import sys 
import os
from pathlib import Path


def get_fasta_from_extracted(dssp_extracted_folder, id_chain_file):
    id_chain_file = Path(id_chain_file)
    id_chain_dict = {}
    for line in id_chain_file.open():
        b = line.rstrip().split("_")
        id_chain_dict[b[0]] = b[1]
    print(id_chain_dict)
    
    for extracted_file in os.listdir(dssp_extracted_folder):
       print(extracted_file)

        
    complete_bs = open("complete_bs.fasta", "a")
    for file in os.listdir(dssp_extracted_folder):
        file_path = Path(dssp_extracted_folder + file)
        complete_bs.write(">" + file + "_" + id_chain_dict[file] + "\n")
        a = file_path.open()  
       
        aa_seq_string = ""
        ss_seq_string = ""

        for line in a:
            splitted_line = line.split(":")
            
            chain = splitted_line[0]
            
            if chain == id_chain_dict[file]:
                aa_seq = splitted_line[1]
                aa_seq_string += aa_seq
            
                ss_seq = splitted_line[2]
                ss_seq_string += ss_seq

        complete_bs.write(aa_seq_string + "\n" + ss_seq_string + "\n")
        
    return()

if __name__ == "__main__":
    dssp_extractedfolder = sys.argv[1]
    id_chain_file = sys.argv[2]

    get_fasta_from_extracted(dssp_extractedfolder, id_chain_file)