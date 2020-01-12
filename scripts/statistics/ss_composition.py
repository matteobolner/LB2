import sys
import os
import pandas as pd
import matplotlib.pyplot as plt

def ss_composition(ss_file):
    f = open(ss_file, "r") 
    h_counter = 0
    e_counter = 0
    coil_counter = 0
    total_counter = 0
    for line in f:
        for letter in line:
            if letter == "H":
                h_counter += 1 
                total_counter += 1
            elif letter == "E":
                e_counter += 1
                total_counter += 1
            elif letter == "-":
                coil_counter += 1
                total_counter += 1

    a = open("ss_total_count.txt", "w+")

    h_percent = "{0:.2f}".format((h_counter/total_counter) * 100)
    e_percent = "{0:.2f}".format((e_counter/total_counter) * 100)
    c_percent = "{0:.2f}".format((coil_counter/total_counter) * 100)


    a.write("H=" + str(h_counter) + "=" + str(h_percent) + "%\n" + "E=" + str(e_counter) + "=" + str(e_percent) + "%\n" + "-=" + str(coil_counter) + "=" + str(c_percent) + "%\n" + "TOT=" + str(total_counter))


    df = pd.DataFrame([h_counter, e_counter, coil_counter], index = ['Helix ' + h_percent + "%" , 'Strand ' + e_percent + "%" , 'Coil ' + c_percent + "%" ], columns=[''])
    df.plot(kind='pie', subplots=True, figsize=(8, 8), legend = None)
    plt.savefig('ss_composition.png')
    return()


if __name__ == "__main__":
    ss_file = sys.argv[1]
    ss_composition(ss_file)
