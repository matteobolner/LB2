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
    ss_list = ["H","E","C","TOT"]
    line_list = f.read().split("\n")
   
    #for the heatmaps
    H_dict = {aa:np.zeros(17) for aa in aa_list}
    E_dict = {aa:np.zeros(17) for aa in aa_list}
    C_dict = {aa:np.zeros(17) for aa in aa_list}
    TOT_dict = {aa:np.zeros(17) for aa in aa_list}
    padding="0000000"

    counter_dict = {}
    for res in aa_list:
        counter_dict[res] = {ss:0 for ss in ss_list}
    for i in ["H_TOT", "E_TOT", "C_TOT", "TOT_TOT"]:
        counter_dict[i] = 0
    
    freq_dict = {}
    for res in aa_list:
        freq_dict[res] = {ss:0 for ss in ss_list}


    for line in line_list:
        if line == "":
            continue
        elif line[0] == ">":

            aa_line_index = int(line_list.index(line) + 1)
            ss_line_index = int(line_list.index(line) + 2)
            
            for aa, ss in zip(line_list[aa_line_index], line_list[ss_line_index]):
                counter_dict[aa][ss] +=1
                counter_dict[aa]["TOT"] +=1  
                counter_dict[ss+"_TOT"] +=1  
                counter_dict["TOT_TOT"] +=1    

            #for the heatmaps
            padded_line = padding + line_list[aa_line_index] + padding
            aa_index = -1
            for aa, ss in zip(line_list[aa_line_index], line_list[ss_line_index]):
                aa_index +=1
                if ss == "C":
                    counter_C = -1
                    for res in padded_line[aa_index:aa_index+17]:
                        counter_C +=1
                        if res == "0":
                            continue
                        else:
                            C_dict[res][counter_C] +=1
                            TOT_dict[res][counter_C] +=1
                elif ss == "H":
                    counter_H = -1
                    for res in padded_line[aa_index:aa_index+17]:
                        counter_H +=1
                        if res == "0":
                            continue
                        else:
                            H_dict[res][counter_H] +=1
                            TOT_dict[res][counter_H] +=1
                elif ss == "E":
                    counter_E = -1
                    for res in padded_line[aa_index:aa_index+17]:
                        counter_E +=1
                        if res == "0":
                            continue
                        else:
                            E_dict[res][counter_E] +=1
                            TOT_dict[res][counter_E] +=1
        else:
            continue
    for res in aa_list:
        for ss in "HEC":
            freq_dict[res][ss] = round((counter_dict[res][ss]/counter_dict[ss+'_TOT'])*100, 2)
        freq_dict[res]['TOT'] = round((counter_dict[res]['TOT']/counter_dict['TOT_TOT'])*100, 2)
    
    H_dict = {k: v / counter_dict['H_TOT']  for k, v in H_dict.items()} 
    E_dict = {j: k / counter_dict['E_TOT']  for j, k in E_dict.items()}    
    C_dict = {w: q / counter_dict['C_TOT']  for w, q in C_dict.items()} 
    TOT_dict = {m: n / counter_dict['TOT_TOT']  for m, n in TOT_dict.items()}
    #call the functions for the various plots
    #ss_piechart(counter_dict)
    barplot_aa_ss(counter_dict, freq_dict)
    #barplot_aa(counter_dict, freq_dict)
    #heatmap(H_dict,E_dict,C_dict, TOT_dict)
    
    return(counter_dict)    


def ss_piechart(counter_dict):
    ss_tot_freq_dict = {'Helix':counter_dict['H_TOT']/counter_dict['TOT_TOT']*100, 'Strand':counter_dict['E_TOT']/counter_dict['TOT_TOT']*100,'Coil':counter_dict['C_TOT']/counter_dict['TOT_TOT']*100}
    labels = list(ss_tot_freq_dict.keys())
    sizes = list(ss_tot_freq_dict.values())
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, labels = labels, autopct='%1.1f%%')
    plt.tight_layout()
    plt.savefig("ss_freq_piechart.png")
    plt.clf()
    return()

def barplot_aa(counter_dict, freq_dict):
    #GAVPLIMFWYSTCNQHDEKRX
    freqs_df = pd.DataFrame(freq_dict)
    aa_freqs_df = freqs_df.loc['TOT']
    aa_freqs_df = aa_freqs_df.reset_index().melt(id_vars=["index"])
    aa_freqs_df = aa_freqs_df.drop(index = 20 , axis = 0)
    aa_freqs_df = aa_freqs_df.rename(columns={'index': 'Residues', 'value':'Residue frequency (%)'})
    sns.set(rc={'figure.figsize':(11.7,8.27)})
    sns.barplot(data = aa_freqs_df, x = 'Residues', y = 'Residue frequency (%)', palette="muted", color=[''] )
    plt.savefig("aa_freq_barplot.png")
    plt.clf()
    return()

def barplot_aa_ss(counter_dict,freq_dict):
    freqs_df = pd.DataFrame(freq_dict)
    freqs_df = freqs_df.rename({'TOT':'Overall', 'H':'Helix', 'E':'Strand', 'C':'Coil'})
    freqs_df = freqs_df.reindex(['Overall', 'Helix', 'Strand', 'Coil'])
    freqs_df = freqs_df.reset_index().melt(id_vars=["index"])
    freqs_df = freqs_df.rename(columns={'index': 'SS', 'variable':'Residue','value':'SS frequency given the residue (%)'})
    sns.set(rc={'figure.figsize':(11.7,8.27)})
    sns.barplot(data = freqs_df, x = 'Residue', y = 'SS frequency given the residue (%)', hue='SS', palette = "muted")
    plt.savefig("aa_ss_barplot.png")
    plt.clf()
    return()

def heatmap(H_dict,E_dict,C_dict, TOT_dict):
    H_df = pd.DataFrame(H_dict)
    H_df = H_df.drop(columns='X')
    H_df = H_df.T
    E_df = pd.DataFrame(E_dict)
    E_df = E_df.drop(columns='X')
    E_df = E_df.T
    C_df = pd.DataFrame(C_dict)
    C_df = C_df.drop(columns='X')
    C_df = C_df.T
    TOT_df = pd.DataFrame(TOT_dict)
    TOT_df = TOT_df.drop(columns='X')
    TOT_df = TOT_df.T

    sns.set(rc={'figure.figsize':(11.7,8.27)})
    sns.heatmap(H_df, square = True, cmap = 'binary', linewidth = 0.01)
    plt.yticks(rotation = 0)    
    plt.savefig("H_heatmap.png")
    plt.clf()

    sns.set(rc={'figure.figsize':(11.7,8.27)})
    sns.heatmap(E_df, square = True, cmap = 'binary', linewidth = 0.01)
    plt.yticks(rotation = 0)    
    plt.savefig("E_heatmap.png")
    plt.clf()

    sns.set(rc={'figure.figsize':(11.7,8.27)})
    sns.heatmap(C_df, square = True, cmap = 'binary', linewidth = 0.01)
    plt.yticks(rotation = 0)    
    plt.savefig("C_heatmap.png")
    plt.clf()
    
    sns.set(rc={'figure.figsize':(11.7,8.27)})
    sns.heatmap(TOT_df, square = True, cmap = 'binary', linewidth = 0.01)
    plt.yticks(rotation = 0)    
    plt.savefig("TOT_heatmap.png")
    plt.clf()

    return()


if __name__ == "__main__":
    merged_file = sys.argv[1]
    count_aa_ss(merged_file)
