import sys
import collections
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
sns.set()

def count_aa_ss(merged_file):
    
    f = open(merged_file, "r")
    aa_list = list("GAVPLIMFWYSTCNQHDEKRX")
    ss_list = ["H","E","-","TOT"]
    line_list = f.read().split("\n")
    H_dict = {aa:np.zeros(17) for aa in aa_list}
    E_dict = {aa:np.zeros(17) for aa in aa_list}
    #C_dict = {aa:np.zeros(17) for aa in aa_list}
    padding="0000000"

    counter_dict = {}
    for res in aa_list:
        counter_dict[res] = {ss:0 for ss in ss_list}
    for i in ["H_TOT", "E_TOT", "-_TOT", "TOT_TOT"]:
        counter_dict[i] = 0
    
    freq_dict = {}
    for res in aa_list:
        freq_dict[res] = {ss:0 for ss in ss_list}


    for line in line_list:
        if line == "":
            break
        if line[0] == ">":

            aa_line_index = int(line_list.index(line) + 1)
            ss_line_index = int(line_list.index(line) + 2)

            for aa, ss in zip(line_list[aa_line_index], line_list[ss_line_index]):
                counter_dict[aa][ss] +=1
                counter_dict[aa]["TOT"] +=1  
                counter_dict[ss+"_TOT"] +=1  
                counter_dict["TOT_TOT"] +=1    

            padded_line = padding + line_list[aa_line_index] + padding
            #print(padded_line)
            aa_index = -1
            for aa, ss in zip(line_list[aa_line_index], line_list[ss_line_index]):
                aa_index +=1
                if ss == "-":
                    continue
                elif ss == "H":
                    counter = -1
                    for res in padded_line[aa_index:aa_index+17]:
                        counter +=1
                        if res == "0":
                            continue
                        else:
                            H_dict[res][counter] +=1
                elif ss == "E":
                    counter_bis = -1
                    for res in padded_line[aa_index:aa_index+17]:
                        counter_bis +=1
                        if res == "0":
                            continue
                        else:
                            E_dict[res][counter_bis] +=1
        else:
            continue

    for res in aa_list:
        for ss in "HE-":
            freq_dict[res][ss] = round((counter_dict[res][ss]/counter_dict[ss+'_TOT'])*100, 2)
        freq_dict[res]['TOT'] = round((counter_dict[res]['TOT']/counter_dict['TOT_TOT'])*100, 2)
    
    H_dict = {k: v / counter_dict['H_TOT']  for k, v in H_dict.items()} 
    E_dict = {j: k / counter_dict['E_TOT']  for j, k in E_dict.items()}      



    #ss_piechart(counter_dict)
    #arplot_aa_ss(counter_dict, freq_dict)
    #barplot_aa(counter_dict, freq_dict)
    heatmap(H_dict,E_dict)
    return(counter_dict)    


def ss_piechart(counter_dict):
    ss_tot_freq_dict = {'Helix':counter_dict['H_TOT']/counter_dict['TOT_TOT']*100, 'Strand':counter_dict['E_TOT']/counter_dict['TOT_TOT']*100,'Coil':counter_dict['-_TOT']/counter_dict['TOT_TOT']*100}
    labels = list(ss_tot_freq_dict.keys())
    sizes = list(ss_tot_freq_dict.values())
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, labels = labels, autopct='%1.1f%%')
    plt.tight_layout()
    plt.savefig("ss_freq_piechart.png")
    return()

def barplot_aa(counter_dict, freq_dict):
    freqs_df = pd.DataFrame(freq_dict)
    aa_freqs_df = freqs_df.loc['TOT']
    aa_freqs_df = aa_freqs_df.reset_index().melt(id_vars=["index"])
    aa_freqs_df = aa_freqs_df.rename(columns={'index': 'Residues', 'value':'Residue frequency (%)'})
    sns.barplot(data = aa_freqs_df, x = 'Residues', y = 'Residue frequency (%)', palette="bright" )
    plt.savefig("aa_freq_barplot.png")
    return()

def barplot_aa_ss(counter_dict,freq_dict):
    freqs_df = pd.DataFrame(freq_dict)
    #print(freqs_df)
    #print(freqs_df.info(verbose=True))
    freqs_df = freqs_df.rename({'-':'Coil', 'E':'Strand', 'H':'Helix', 'TOT':'Overall'})
    freqs_df = freqs_df.reset_index().melt(id_vars=["index"])
    freqs_df = freqs_df.rename(columns={'index': 'SS', 'variable':'Residue','value':'Residue frequency (%)'})
    #print(freqs_df)
    sns.set(rc={'figure.figsize':(11.7,8.27)})
    aa_ss_plot = sns.barplot(data = freqs_df, x = 'Residue', y = 'Residue frequency (%)', hue='SS') #, palette = "bright")
    #aa_ss_plot.legend(loc='upper center')
    plt.savefig("aa_ss_barplot.png")

def heatmap(H_dict,E_dict):
    H_df = pd.DataFrame(H_dict)
    H_df = H_df.drop(columns='X')
    H_df = H_df.T
    E_df = pd.DataFrame(E_dict)
    E_df = E_df.drop(columns='X')
    E_df = E_df.T
    
    sns.set(rc={'figure.figsize':(11.7,8.27)})
    sns.heatmap(H_df, square = True, cmap = 'binary', linewidth = 0.01)
    plt.savefig("prova.png")



if __name__ == "__main__":
    merged_file = sys.argv[1]
    count_aa_ss(merged_file)
