import os 
import sys
import numpy as np
np.set_printoptions(threshold=np.inf)

def fill_matrix(prediction, original):
    conf_dict = {"HH":0, "HE":0, "H-":0, "EH":0, "EE":0, "E-":0, "-H":0, "-E":0, "--":0, "TOT":0}       #"originalpredicted":0
    prediction = open(prediction, "r")
    original = open(original, "r")
    pred_filelist = [pred_line.rstrip() for pred_line in prediction]
    orig_filelist = [orig_line.rstrip() for orig_line in original]
    line_counter = -1
    for line in orig_filelist:
        line_counter += 1
        clean_line = line.rstrip()
        letter_counter = -1
        for letter in clean_line:
            letter_counter += len(letter)   #len letter just to shut up vscode, can be changed back to 1
            dict_header = orig_filelist[line_counter][letter_counter] + pred_filelist[line_counter][letter_counter]
            conf_dict[dict_header] += 1
            conf_dict["TOT"] += 1
    binary_matrix(conf_dict)
    return(conf_dict)

def binary_matrix(conf_dict):

    #binary matrix:
    #C(H) = P(HH)   00      Correct positive predictions
    #O(H) = P(EH) + P(-H)   01      Overpredictions
    #U(H) = P(HE) + P(H-)   10      Underpredictions
    #N(H) = P(EE) + P(-E) + P(E-) + P(--)   11  Correct negative predictions
  
    H_matrix = np.zeros((2,2), dtype='float64')
    E_matrix = np.zeros((2,2), dtype='float64')
    C_matrix = np.zeros((2,2), dtype='float64')

    C_H = conf_dict["HH"]
    O_H = conf_dict["EH"] + conf_dict["-H"]
    U_H = conf_dict["HE"] + conf_dict["H-"]
    N_H = conf_dict["EE"] + conf_dict["-E"] + conf_dict["E-"] + conf_dict["--"]

    C_E = conf_dict["EE"]
    O_E = conf_dict["HE"] + conf_dict["-E"]
    U_E = conf_dict["EH"] + conf_dict["E-"]
    N_E = conf_dict["HH"] + conf_dict["-H"] + conf_dict["H-"] + conf_dict["--"]

    C_C = conf_dict["--"]
    O_C = conf_dict["H-"] + conf_dict["E-"]
    U_C = conf_dict["-H"] + conf_dict["-E"]
    N_C = conf_dict["HH"] + conf_dict["EH"] + conf_dict["HE"] + conf_dict["EE"]


    H_matrix[0][0] = C_H
    H_matrix[0][1] = O_H
    H_matrix[1][0] = U_H
    H_matrix[1][1] = N_H
    E_matrix[0][0] = C_E
    E_matrix[0][1] = O_E
    E_matrix[1][0] = U_E
    E_matrix[1][1] = N_E
    C_matrix[0][0] = C_C
    C_matrix[0][1] = O_C
    C_matrix[1][0] = U_C
    C_matrix[1][1] = N_C
    
    SEN_H = round((C_H)/(C_H + U_H), 2)   #sensitivity/true positive rate
    PPV_H = round((C_H)/(C_H + O_H), 2)   #precision/positive predictive value
    MCC_H = round((((C_H*N_H)-(O_H*U_H))/np.sqrt((C_H+O_H)*(C_H+U_H)*(N_H+O_H)*(N_H+U_H))), 2)    #Matthew's correlation coefficient

    SEN_E = round((C_E)/(C_E + U_E), 2)
    PPV_E = round((C_E)/(C_E + O_E), 2)
    MCC_E = round((((C_E*N_E)-(O_E*U_E))/np.sqrt((C_E+O_E)*(C_E+U_E)*(N_E+O_E)*(N_E+U_E))), 2)
    SEN_C = round((C_C)/(C_C + U_C), 2)
    PPV_C = round((C_C)/(C_C + O_C), 2)
    MCC_C = round((((C_C*N_C)-(O_C*U_C))/np.sqrt((C_C+O_C)*(C_C+U_C)*(N_C+O_C)*(N_C+U_C))), 2)
    TCA = round((((C_H , 2)+ C_E + C_C)/conf_dict["TOT"]),2)    #three class accuracy
    
    print("#Counter dictionary (Original data|Prediction);")
    print(conf_dict)
    print("\n#H confusion matrix ;" )
    print(H_matrix)
    print("\n#E confusion matrix ;")
    print(E_matrix)
    print("\n#C confusion matrix ;")
    print(C_matrix)
    print("\n#H,E,C: \n")
    print("\n#SEN;"+ str(SEN_H) +";"+ str(SEN_E) + ";" + str(SEN_C))
    print("\n#PPV;"+ str(PPV_H) +";"+ str(PPV_E) + ";" + str(PPV_C))
    print("\n#MCC;"+ str(MCC_H) +";"+ str(MCC_E) + ";" + str(MCC_C))
    print("\n#TCA;"+str(TCA))
    return()


if __name__ == "__main__":
    original = sys.argv[1]
    prediction = sys.argv[2]
    fill_matrix(prediction, original)
