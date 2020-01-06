import sys
import os
import numpy as np
np.set_printoptions(threshold=np.inf)



w = 17      #profile window size

#initiate empty matrices
H_matrix = np.zeros((int(w),20), dtype= 'float64')            #matrices containing the frequency of the residues corresponding to the considered ss
E_matrix = np.zeros((int(w),20), dtype= 'float64')            
C_matrix = np.zeros((int(w),20), dtype= 'float64')
aa_freq_matrix = np.zeros((int(w),20), dtype= 'float64')      #matrix containing the total frequency of all residues
ss_count_matrix = np.zeros((4,3), dtype= 'object')      #matrix containing the total number of ss with their corresponding frequency (independently of the residues)

ss_count_matrix[0][0] = "H"                             #ss_count_matrix headers
ss_count_matrix[1][0] = "E"
ss_count_matrix[2][0] = "-"
ss_count_matrix[3][0] = "TOT"



def fill_matrices(dssp_file,profile_file, H_matrix, E_matrix, C_matrix, aa_freq_matrix, ss_count_matrix):
    
    #open the current dssp file and obtain the ss sequence
    dssp_opened = open(dssp_file, "r")
    for line in dssp_opened:
        if line[0] == ">":
            continue
        else:
            dssp_seq = line.rstrip()

    #load the current sequence profile and initiate the window matrix with padding before and after the profile
    pad = (int(w)//2)
    padding_matrix = np.zeros((pad, 20), dtype = 'float64')
    profile_matrix = np.loadtxt(profile_file, dtype= 'float64')
    padded_profile = np.concatenate((padding_matrix,profile_matrix,padding_matrix), axis = 0 )
    

    #iterate over the dssp sequence and add the current window matrix to the corresponding matrices 
    c = -1
    for i in dssp_seq:
        c += 1
        window_matrix = np.divide(padded_profile[c:(c+17)],100)
        
        if i == "H":
            np.add(H_matrix, window_matrix, out = H_matrix)
            np.add(aa_freq_matrix, window_matrix, out = aa_freq_matrix)
            ss_count_matrix[0][1] += 1
            ss_count_matrix[3][1] += 1
            
        elif i == "E":
            np.add(E_matrix, window_matrix, out = E_matrix)
            np.add(aa_freq_matrix, window_matrix, out = aa_freq_matrix)
            ss_count_matrix[1][1] += 1
            ss_count_matrix[3][1] += 1

        elif i == "-":
            np.add(C_matrix, window_matrix, out = C_matrix)
            np.add(aa_freq_matrix, window_matrix, out = aa_freq_matrix)
            ss_count_matrix[2][1] += 1
            ss_count_matrix[3][1] += 1
        
    return()


def train_model(output_folder):
    id_list_open = open(id_list , "r")   

    #obtain the path of the profile and dssp files from the list, and run the fill_matrices function on each one of them
    for file in id_list_open:
        if (file.rstrip() + ".profile")  in os.listdir(profile_folder):
            profile_file = os.path.join(profile_folder, (file.rstrip() + ".profile"))
            dssp_file = os.path.join(profile_folder, (file.rstrip() + ".dssp"))
            fill_matrices(dssp_file, profile_file, E_matrix, H_matrix, C_matrix, aa_freq_matrix, ss_count_matrix)
        else:
            continue



    #normalize the matrices now filled, by dividing each element by the total number of ss 
    total_ss_number = (ss_count_matrix[3][1])
    normalized_H_matrix = np.divide(H_matrix, total_ss_number)
    normalized_E_matrix = np.divide(E_matrix, total_ss_number)
    normalized_C_matrix = np.divide(C_matrix, total_ss_number)
    normalized_aa_freq_matrix = np.divide(aa_freq_matrix, total_ss_number)
    for l in range(4):
        ss_count_matrix[l][2] = np.divide(ss_count_matrix[l][1], ss_count_matrix[3][1])

    #create the path for the output files
    ss_count_path = os.path.join(output_folder, "ss_count_matrix.txt" )
    H_path = os.path.join(output_folder, "H_MATRIX.txt" )
    E_path = os.path.join(output_folder, "E_MATRIX.txt" )
    C_path = os.path.join(output_folder, "C_MATRIX.txt" )
    aa_freq_path = os.path.join(output_folder, "aa_freq_matrix.txt")

    #save the output files in their respective paths
    np.savetxt(ss_count_path, ss_count_matrix, fmt='%s')
    np.savetxt(H_path, normalized_H_matrix, fmt='%s')
    np.savetxt(E_path, normalized_E_matrix, fmt='%s')
    np.savetxt(C_path, normalized_C_matrix, fmt='%s')
    np.savetxt(aa_freq_path, normalized_aa_freq_matrix, fmt='%s')
    
    return()



if __name__ == "__main__":
    profile_folder = sys.argv[1]
    id_list = sys.argv[2]
    output_folder = sys.argv[3]
    train_model(output_folder)