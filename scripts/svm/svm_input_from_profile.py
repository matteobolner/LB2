
import sys
import os
import numpy as np
np.set_printoptions(threshold=np.inf)

'''
def get_profile_from_file(profile_file):
    profile_list = []
    profile_opened = open(profile_file, "r")
    for line in profile_opened:
        line = line.rstrip().split()
        profile_list.append(line)
    
    return profile_list'''

 
def add_padding():
    a = np.loadtxt(profile_file)
    window = 17                         #window size
    pad = (int(window)//2)
    padding_matrix = np.zeros((pad,20))
    padded_profile = np.concatenate((padding_matrix, a, padding_matrix))
    padded_profile = np.divide(padded_profile, 100)
    return padded_profile


    
def obtain_input(dssp_file):
    b = add_padding()
    ss = {"H" : "1", "E" : "2", "-" : 3}    #secondary structure elements as classes
    window = 17
    pad = (int(window)//2)
    output_filename = (dssp_file.split("/")[-1]).replace(".dssp", "") + ".svm"
    dssp_opened = open(dssp_file, "r")
    filepath = os.path.join(output_path, output_filename)
    final_output = open(filepath, "w")
    for line in dssp_opened:
        if line[0] == ">":
            continue
        else:
            dssp_seq = line.rstrip()
    for i,j in zip(dssp_seq, range(len(dssp_seq))):
        #print(i,j)
        v,f = [],0
        j += 8
        #print(j)
        for k in b[j-pad:j+1+pad]:
            for r in k:
                f +=1
                if r == 0:
                    continue
                else:
                    v.append(str(f) + ":" + str(r))   
        final_output.write(str(ss[i]) + " " + " ".join(v)+"\n")
    return()



if __name__ == "__main__":
    
    jpred_list = sys.argv[1]
    profile_folder = sys.argv[2]
    output_path = sys.argv[3]
    
    jpred_list_open = open(jpred_list , "r")

    for file in jpred_list_open:
        if (file.rstrip() + ".profile") in os.listdir(profile_folder):
            profile_file = os.path.join(profile_folder, (file.rstrip() + ".profile"))
            dssp_file = os.path.join(profile_folder, (file.rstrip() + ".dssp"))
            obtain_input(dssp_file)
        else:
            continue

        