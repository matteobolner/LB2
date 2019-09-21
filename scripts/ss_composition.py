import sys
import os
import pandas as pd
import matplotlib.pyplot as plt

def ss_composition(dssp_folder):
    f = dssp_folder 
    h_counter = 0
    e_counter = 0
    coil_counter = 0


    for dssp_filename in os.listdir(f):
        dssp_file = open(dssp_filename, "r")
        for line in dssp_file:
            if line[0] == ">" :
                continue
            #elif line[0] != ">":
            else:
                #line.rstrip()
                for letter in line:
                    if letter == "H":
                        h_counter += 1 
                    elif letter == "E":
                        e_counter += 1
                    elif letter == "-":
                        coil_counter += 1
    a = open("ss_total_values.txt", "w+")
    a.write("H = " + str(h_counter) + "\n" + "E = " + str(e_counter) + "\n" + "- = " + str(coil_counter))

    print(h_counter)
    print(e_counter)
    print(coil_counter)

    df = pd.DataFrame([h_counter, e_counter, coil_counter], index = ['Helix' , 'Strand', 'Coil'], columns=[''])
    df.plot(kind='pie', subplots=True, figsize=(8, 8))
    plt.show()
    return()


if __name__ == "__main__":
    dssp_folder = sys.argv[1]
    ss_composition(dssp_folder)
