

import pandas as pd
import numpy as np
import pickle
import json
import os

sprime_files = "/Users/eugeniaampofo/Downloads/Downloads/Sprime_files/Sprime_res/"
save_to ="/Users/eugeniaampofo/Downloads/Downloads/Vis_files/"

populations = []



def load_data():
    return
    # return pd.read_csv(filename)


def preprocess_data(pop_path, sprime, outp):
    with open(pop_path, "r") as json_file:
        pop_lst = json.load(json_file)
    make_pop_dat(sprime, pop_lst)
   
    

def make_pop_dat(sprime_files, poplst):
    pop_dataf = {}
    for file in os.listdir(sprime_files):
        for name in poplst:
            if name in file:
                try:
                    df= pd.read_csv(sprime_files + file, sep="\t", dtype=str)
                except:
                    df = pd.read_csv(sprime_files + file, compression='gzip', sep="\t", dtype=str)
                df.iloc[:, 0] = df.iloc[:, 0].astype(str)
                df_sorted = df.sort_values(by=[df.columns[0], "POS"], ascending=True)
                df_sorted = df_sorted[df_sorted[df_sorted.columns[0]] != "nan"]
                df_sorted[df.columns[0]] = df_sorted[df_sorted.columns[0]].astype(int)
                df_sorted["POS"] = df_sorted[df_sorted.columns[1]].astype(int)
                df_sorted["SEGMENT"] = df_sorted["SEGMENT"].astype(int)
                df_sorted = df_sorted.sort_values(by=[df_sorted.columns[0], "POS", "SEGMENT"], ascending=True)
                pop_dataf[name] = df_sorted
    with open(save_to + 'popdataf.pkl', 'wb') as json_file:
        pickle.dump(pop_dataf, json_file)


def make_everything(sprime, popnames):
    pass