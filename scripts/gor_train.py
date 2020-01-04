import sys
import os
import numpy as np
np.set_printoptions(threshold=np.inf)

w = 17

E_matrix = np.zeros((int(w),20), dtype= 'i')
H_matrix = np.zeros((int(w),20), dtype= 'i')
C_matrix = np.zeros((int(w),20), dtype= 'i')
TOT_matrix = np.zeros((int(w),20), dtype= 'i')
counting_matrix = np.zeros((4,3), dtype= 'object')

counting_matrix[0][0] = "H"
counting_matrix[1][0] = "E"
counting_matrix[2][0] = "-"
counting_matrix[3][0] = "TOT"

def fill_matrices(dssp_file,profile_file, H_matrix, E_matrix, C_matrix, TOT_matrix, counting_matrix):
    dssp_opened = open(dssp_file, "r")
    for line in dssp_opened:
        if line[0] == ">":
            continue
        else:
            dssp_seq = line.rstrip()

    pad = (int(w)//2)
    padding_matrix = np.zeros((pad, 20), dtype = 'i')
    profile_matrix = np.loadtxt(profile_file, dtype= 'i')
    padded_profile = np.concatenate((padding_matrix,profile_matrix,padding_matrix), axis = 0 )
    #print(padded_profile)
    c = -1
    for i in dssp_seq:
        c += 1
        window_matrix = padded_profile[c:(c+17)]
        #print(window_matrix)
        if i == "H":
            H_matrix += window_matrix
            TOT_matrix += window_matrix
            counting_matrix[0][1] += 1
            counting_matrix[3][1] += 1
            
        elif i == "E":
            E_matrix += window_matrix
            TOT_matrix += window_matrix
            counting_matrix[1][1] += 1
            counting_matrix[3][1] += 1

        elif i == "-":
            C_matrix += window_matrix
            TOT_matrix += window_matrix
            counting_matrix[2][1] += 1
            counting_matrix[3][1] += 1
    return()


def train_model(output_folder):
    id_list_open = open(id_list , "r")   

    for file in id_list_open:
        if (file.rstrip() + ".profile")  in os.listdir(profile_folder):
            profile_file = os.path.join(profile_folder, (file.rstrip() + ".profile"))
            dssp_file = os.path.join(profile_folder, (file.rstrip() + ".dssp"))
            fill_matrices(dssp_file, profile_file, E_matrix, H_matrix, C_matrix, TOT_matrix, counting_matrix)
            #break
        else:
            continue
    

    total_number = (counting_matrix[3][1]*100)
    normalized_H_matrix = np.divide(H_matrix, total_number)
    
    normalized_E_matrix = np.divide(E_matrix, total_number)
    
    normalized_C_matrix = np.divide(C_matrix, total_number)
    
    normalized_TOT_matrix = np.divide(TOT_matrix, total_number)
    for l in range(3):
        counting_matrix[l][2] = np.divide(counting_matrix[l][1], counting_matrix[3][1])

    #*100 because the frequences must be in % and the profile contains the number not divided by 100

    counting_path = os.path.join(output_folder, "COUNTING_MATRIX.txt" )
    H_path = os.path.join(output_folder, "H_MATRIX.txt" )
    E_path = os.path.join(output_folder, "E_MATRIX.txt" )
    C_path = os.path.join(output_folder, "C_MATRIX.txt" )
    TOT_PATH = os.path.join(output_folder, "TOT_MATRIX.txt")

    np.savetxt(counting_path, counting_matrix, fmt='%s')
    np.savetxt(H_path, normalized_H_matrix, fmt='%s')
    np.savetxt(E_path, normalized_E_matrix, fmt='%s')
    np.savetxt(C_path, normalized_C_matrix, fmt='%s')
    np.savetxt(TOT_PATH, normalized_TOT_matrix, fmt='%s')
    
    return()


if __name__ == "__main__":
    profile_folder = sys.argv[1]
    id_list = sys.argv[2]
    output_folder = sys.argv[3]
    train_model(output_folder)