import sys
import os
import numpy as np
np.set_printoptions(threshold=np.inf)

w = 17

E_matrix = np.zeros((int(w),20), dtype= 'i')
H_matrix = np.zeros((int(w),20), dtype= 'i')
C_matrix = np.zeros((int(w),20), dtype= 'i')
counting_matrix = np.zeros((3,2), dtype= 'object')
counting_matrix[0][0] = "H"
counting_matrix[1][0] = "E"
counting_matrix[2][0] = "-"


def fill_matrices(dssp_file,profile_file, H_matrix, E_matrix, C_matrix, counting_matrix):
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
        if i == "H":
            H_matrix += window_matrix
            counting_matrix[0][1] += 1
        elif i == "E":
            E_matrix += window_matrix
            counting_matrix[1][1] += 1

        elif i == "-":
            C_matrix += window_matrix
            counting_matrix[2][1] += 1
    
    return()


def train_model(output_folder):
    id_list_open = open(id_list , "r")   

    for file in id_list_open:
        if (file.rstrip() + ".profile")  in os.listdir(profile_folder):
            profile_file = os.path.join(profile_folder, (file.rstrip() + ".profile"))
            dssp_file = os.path.join(profile_folder, (file.rstrip() + ".dssp"))
            fill_matrices(dssp_file, profile_file, E_matrix, H_matrix, C_matrix, counting_matrix)
            #break
        else:
            continue
    
    H_matrix_sum = np.sum(H_matrix)
    normalized_H_matrix = np.divide(H_matrix, H_matrix_sum)
    
    E_matrix_sum = np.sum(E_matrix)
    normalized_E_matrix = np.divide(E_matrix, E_matrix_sum)
    
    C_matrix_sum = np.sum(C_matrix)
    normalized_C_matrix = np.divide(C_matrix, C_matrix_sum)
    
    check_sum_H = np.sum(normalized_H_matrix)
    check_sum_E = np.sum(normalized_E_matrix)
    check_sum_C = np.sum(normalized_C_matrix)
    print(check_sum_C,check_sum_E,check_sum_H)

    counting_path = os.path.join(output_folder, "COUNTING_MATRIX.txt" )
    H_path = os.path.join(output_folder, "H_MATRIX.txt" )
    E_path = os.path.join(output_folder, "E_MATRIX.txt" )
    C_path = os.path.join(output_folder, "C_MATRIX.txt" )

    np.savetxt(counting_path, counting_matrix, fmt='%s' )
    np.savetxt(H_path, normalized_H_matrix, fmt='%s')
    np.savetxt(E_path, normalized_E_matrix, fmt='%s')
    np.savetxt(C_path, normalized_C_matrix, fmt='%s')
    
    return()


if __name__ == "__main__":
    profile_folder = sys.argv[1]
    id_list = sys.argv[2]
    output_folder = sys.argv[3]
    train_model(output_folder)
    