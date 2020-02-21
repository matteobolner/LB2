import sys 
import os
import numpy as np
import pandas as pd

engine='python'

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)



def get_files(perf_folder, perf_filetype, sov_filetype):
    perf_list = []
    sov_list = []
    for perf_file in os.listdir(perf_folder):

        if perf_file.startswith(perf_filetype):
            perf_path = os.path.join(perf_folder,perf_file)
            perf_list.append(pd.read_csv(perf_path, sep = ";", index_col=0, header=11, names=['H','E','C']))
        elif perf_file.startswith(sov_filetype):
            perf_path = os.path.join(perf_folder, perf_file)
            sov_list.append(pd.read_csv(perf_path, sep = ":\t", header = 0, names = ['SOV', '%'], index_col = 0 ,engine='python'))

    sov_df = pd.concat(sov_list)
    sov_df = sov_df.sort_index()
    sov_df = sov_df.groupby(level = 0)
    sov_mean = sov_df.mean()
    sov_sem = sov_df.sem(ddof = 0)
    sov_mean_and_sem = pd.concat([sov_mean, sov_sem], axis=1)
    sov_mean_and_sem = sov_mean_and_sem.transpose()
    sov_cols = ['H','E','-']
    sov_mean_and_sem = sov_mean_and_sem[sov_cols]

    perf_df = pd.concat(perf_list)
    perf_df = perf_df.sort_index()
    perf_df = perf_df.groupby(level = 0)
    perf_mean = perf_df.mean()
    perf_sem = perf_df.sem(ddof = 0)

    a = []
    for ss in ['H','E','C']:
        a.append(perf_mean[ss])
        a.append(perf_sem[ss])
    perf_mean_and_sem = pd.concat(a, axis =1)
    perf_mean_and_sem = perf_mean_and_sem.multiply(100).round(2)
    perf_cols = (' '.join(w) for w in zip(perf_mean_and_sem.columns[::2], perf_mean_and_sem.columns[1::2]))
    perf_mean_and_sem = pd.DataFrame(perf_mean_and_sem.iloc[:, ::2].astype(str).values + ' ± ' + perf_mean_and_sem.iloc[:, 1::2].astype(str).values, index=perf_mean_and_sem.index, columns=perf_cols)
    
sov_mean_and_sem = sov_mean_and_sem.transpose().round(2)
    sov_cols = (' '.join(k) for k in zip(sov_mean_and_sem.columns[::2], sov_mean_and_sem.columns[1::2]))
    sov_mean_and_sem = pd.DataFrame(sov_mean_and_sem.iloc[:, ::2].astype(str).values + ' ± ' + sov_mean_and_sem.iloc[:, 1::2].astype(str).values, index =['H','E','C'], columns = ['SOV'])
    perf_mean_and_sem = pd.DataFrame(perf_mean_and_sem.transpose())
    perf_mean_and_sem = perf_mean_and_sem.rename(index = {'H H':'H', 'E E':'E', 'C C':'C'})
    final_df = pd.DataFrame.join(perf_mean_and_sem, sov_mean_and_sem)
    final_cols = ['SEN', 'PPV', 'MCC', 'SOV', 'TCA']
    final_df = final_df[final_cols]
    print(final_df)

if __name__ == "__main__":
    perf_folder = sys.argv[1]
    perf_filetype = sys.argv[2]
    sov_filetype = sys.argv[3]
    get_files(perf_folder, perf_filetype, sov_filetype)
