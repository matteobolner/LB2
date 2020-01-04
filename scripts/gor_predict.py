import sys 
import os
import numpy as np
np.set_printoptions(threshold=np.inf)

#input: 1)a folder containing the sequence profiles of the input proteins 
#       2)the folder containing the GOR model

w = 17

def get_h(model_folder):
    H_path = os.path.join(model_folder + "H_MATRIX.txt")
    H_matrix = np.loadtxt(H_path)
    return(H_matrix)

def get_e(model_folder):
    E_path = os.path.join(model_folder + "E_MATRIX.txt")
    E_matrix = np.loadtxt(E_path)
    return(E_matrix)

def get_c(model_folder):
    C_path = os.path.join(model_folder + "C_MATRIX.txt")
    C_matrix = np.loadtxt(C_path)
    return(C_matrix)

def get_counter(model_folder):
    counting_path = os.path.join(model_folder + "COUNTING_MATRIX.txt")
    counting_matrix = np.loadtxt(counting_path, usecols=2)
    return(counting_matrix)

def get_aa_freqs(model_folder):
    total_path = os.path.join(model_folder + "TOT_MATRIX.txt")
    total_matrix = np.loadtxt(total_path)
    return(total_matrix)

def predict_from_set(model_folder):
    H_matrix = get_h(model_folder)
    #print(H_matrix)
    E_matrix = get_e(model_folder)
    C_matrix = get_c(model_folder)
    counting_matrix = get_counter(model_folder)
    total_matrix = get_aa_freqs(model_folder)
    open_idlist = open(id_list, "r")
    
    for line in open_idlist:
        profile_name = line.rstrip() + ".profile"
        profile_path = os.path.join(profile_folder, profile_name)
        predict_ss(profile_path, H_matrix, E_matrix, C_matrix, counting_matrix, total_matrix)
   
    return()



def predict_ss(profile_file, H_matrix, E_matrix, C_matrix, counting_matrix, total_matrix):
    profile_opened = open(profile_file, "r")
    pad = (int(w)//2)
    padding_matrix = np.zeros((pad, 20), dtype = 'i')
    profile_matrix = np.loadtxt(profile_file, dtype= 'i')
    #print(profile_matrix)
    padded_profile = np.concatenate((padding_matrix,profile_matrix,padding_matrix), axis = 0 )

    predicted_sequence = ""
    c = -1
    for line in profile_opened:
        c += 1        
        current_profile_matrix = padded_profile[c:(c+17)]
        #print(current_profile_matrix)
        #print(np.multiply(counting_matrix[0], total_matrix))
        print(np.sum(np.log(np.divide(E_matrix,np.multiply(counting_matrix[1], total_matrix)))))
        #print(np.multiply(counting_matrix[1], total_matrix))

        #I = log(SS_matrix/(SS_freq*AA_freq))
        inf_matrix_H = np.log(np.divide(H_matrix, np.multiply(counting_matrix[0], total_matrix)))
        inf_matrix_E = np.log(np.divide(E_matrix, np.multiply(counting_matrix[1], total_matrix)))
        inf_matrix_C = np.log(np.divide(C_matrix, np.multiply(counting_matrix[2], total_matrix)))

        #print(inf_matrix_H)
        #print(inf_matrix_C)
        #print(inf_matrix_E)

        infcont_H = np.sum(np.multiply(inf_matrix_H, current_profile_matrix))
        #print(infcont_H)
        infcont_E = np.sum(np.multiply(inf_matrix_E, current_profile_matrix))
        #print(infcont_E)
        infcont_C = np.sum(np.multiply(inf_matrix_C, current_profile_matrix))
        #print(infcont_C)
        #print(infcont_H)
        infcont_dict = {infcont_H:"H",infcont_E:"E",infcont_C:"-"} 
        predicted_sequence += infcont_dict.get(max(infcont_dict)) 
        #print(infcont_dict)  
        break
    print(predicted_sequence)

    return(predicted_sequence)    
if __name__ == "__main__":
    model_folder = sys.argv[1]
    id_list = sys.argv[2]
    profile_folder = sys.argv[3]
    predict_from_set(model_folder)
    