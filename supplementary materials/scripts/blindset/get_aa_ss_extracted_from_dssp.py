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
        
        dssp_filename = str(dssp_extracted_folder) + "/" + file
        dssp_file_path = Path(dssp_filename)
        file_id_only = file.split(".")[0]
        a = dssp_file_path.open()  

        aa_seq_string = ""
        ss_seq_string = ""

        for line in a:
            splitted_line = line.split(":")
            chain = splitted_line[0]
            residue = splitted_line[1]
            secondary_structure = splitted_line[2]

            correct_ss = "PROBLEM"

            if secondary_structure in ("H", "G", "I"):
                correct_ss = "H"
                print(correct_ss)
            elif secondary_structure in ("B", "E"):
                correct_ss = "E"
                print(correct_ss)
            elif secondary_structure in ("T", "S", " "):
                correct_ss = "C"
                print(correct_ss)

            if chain == id_chain_dict[file_id_only]:
                aa_seq_string += residue
                ss_seq_string += correct_ss
        
        id_and_chain = file_id_only + "_" + id_chain_dict[file]

        complete_bs.write(">" + id_and_chain + "\n" + aa_seq_string.upper() + "\n" + ss_seq_string + "\n" + "\n")
        
    return()



if __name__ == "__main__":
    dssp_extractedfolder = sys.argv[1]
    id_file = sys.argv[2]
    get_fasta_from_extracted(dssp_extractedfolder, id_file)