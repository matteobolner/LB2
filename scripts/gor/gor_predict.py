import sys 
import os
import numpy as np
np.set_printoptions(threshold=np.inf)


#window size - must be the same as the training
w = 17


#functions to load the training model matrices
def get_h(model_folder):
    H_path = os.path.join(model_folder + "H_MATRIX.txt")
    H_matrix = np.loadtxt(H_path, dtype= 'float64')
    return(H_matrix)

def get_e(model_folder):
    E_path = os.path.join(model_folder + "E_MATRIX.txt")
    E_matrix = np.loadtxt(E_path, dtype= 'float64')
    return(E_matrix)

def get_c(model_folder):
    C_path = os.path.join(model_folder + "C_MATRIX.txt")
    C_matrix = np.loadtxt(C_path, dtype= 'float64')
    return(C_matrix)

def get_ss_counter(model_folder):
    ss_count_path = os.path.join(model_folder + "ss_count_matrix.txt")
    ss_count_matrix = np.loadtxt(ss_count_path, dtype= 'float64', usecols=2)
    return(ss_count_matrix)

def get_aa_freqs(model_folder):
    aa_freq_path = os.path.join(model_folder + "aa_freq_matrix.txt")
    aa_freq_matrix = np.loadtxt(aa_freq_path, dtype= 'float64')
    return(aa_freq_matrix)



def predict_from_set(model_folder):
    #function to iterate over the list of test ids and predict the ss sequence from them
    
    open_idlist = open(id_list, "r")

    H_matrix = get_h(model_folder)
    E_matrix = get_e(model_folder)
    C_matrix = get_c(model_folder)
    ss_count_matrix = get_ss_counter(model_folder)
    aa_freq_matrix = get_aa_freqs(model_folder)
    
    inf_matrix_H = np.log(np.divide(H_matrix, np.multiply(ss_count_matrix[0], aa_freq_matrix)))
    inf_matrix_E = np.log(np.divide(E_matrix, np.multiply(ss_count_matrix[1], aa_freq_matrix)))
    inf_matrix_C = np.log(np.divide(C_matrix, np.multiply(ss_count_matrix[2], aa_freq_matrix)))

    counter_dict = {"H":0, "E":0, "-":0}

    for line in open_idlist:
        print(">" + line.rstrip())
        profile_name = line.rstrip() + ".profile"
        profile_path = os.path.join(profile_folder, profile_name)
        predict_ss(profile_path, inf_matrix_H, inf_matrix_E, inf_matrix_C, ss_count_matrix, aa_freq_matrix, counter_dict)
        print("\n")
        print(counter_dict)

    return(inf_matrix_H, inf_matrix_E, inf_matrix_C, counter_dict)



def predict_ss(profile_file, inf_matrix_H, inf_matrix_E, inf_matrix_C, ss_count_matrix, aa_freq_matrix, counter_dict):
  
    #open the profile and set up the padding for the window matrix
  
    profile_opened = open(profile_file, "r")
    pad = (int(w)//2)
    padding_matrix = np.zeros((pad, 20), dtype = 'float64')
    profile_matrix = np.loadtxt(profile_file, dtype= 'float64')
    padded_profile = np.concatenate((padding_matrix,profile_matrix,padding_matrix), axis = 0 )

    #initiate the empty ss sequence
    predicted_sequence = ""
    
    c = -1
    for line in profile_opened:
        c += 1   

        current_profile_matrix = np.divide(padded_profile[c:(c+17)], 100)
        
        infcont_H = np.sum(np.multiply(inf_matrix_H, current_profile_matrix))
        infcont_E = np.sum(np.multiply(inf_matrix_E, current_profile_matrix))
        infcont_C = np.sum(np.multiply(inf_matrix_C, current_profile_matrix))

        infcont_dict = {infcont_H:"H",infcont_E:"E",infcont_C:"-"} 
        chosen_ss = infcont_dict.get(max(infcont_dict))
        predicted_sequence += chosen_ss
        counter_dict[chosen_ss] += 1

    print(predicted_sequence)
    return(predicted_sequence)  


if __name__ == "__main__":
    model_folder = sys.argv[1]
    id_list = sys.argv[2]
    profile_folder = sys.argv[3]
    predict_from_set(model_folder)
    