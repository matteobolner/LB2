import sys
import os
import pandas as pd
import matplotlib.pyplot as plt

def ss_composition(ss_file):
    f = open(ss_file, "r") 
    h_counter = 0
    e_counter = 0
    coil_counter = 0
    for line in f:
        for letter in line:
            if letter == "H":
                h_counter += 1 
            elif letter == "E":
                e_counter += 1
            elif letter == "-":
                coil_counter += 1
    a = open("ss_total_count.txt", "w+")
    a.write("H = " + str(h_counter) + "\n" + "E = " + str(e_counter) + "\n" + "- = " + str(coil_counter))

    print(h_counter)
    print(e_counter)
    print(coil_counter)

    df = pd.DataFrame([h_counter, e_counter, coil_counter], index = ['Helix' , 'Strand', 'Coil'], columns=[''])
    df.plot(kind='pie', subplots=True, figsize=(8, 8))
    plt.savefig('prova.png')
    return()


if __name__ == "__main__":
    ss_file = sys.argv[1]
    ss_composition(ss_file)
