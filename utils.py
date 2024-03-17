

import pandas as pd
import numpy as np
import pickle
import json
import os

sprime_files = "/Users/eugeniaampofo/Downloads/Downloads/Sprime_files/Sprime_res/"
save_to ="/Users/eugeniaampofo/Downloads/Downloads/Vis_files/"
save_to = "/Users/eugeniaampofo/Downloads/Downloads/Vis_files/"
path2 = save_to + 'ov_num_df.pkl'  # dictionary that maps chromosome to dataframe with all populations
path3 = save_to + 'popdataf.pkl'  # dictionary that maps population to dataframe
path4 = save_to + 'pop_chrom_dict.pkl'  # dictionary that maps chromosome to dataframe with all populations
path5 = save_to + "pop_segment_dict"


populations = []

lok = {}
pop_chrom_dict = {}
popdataf ={}
pop_segment_dict = {}



def create_og():
    global populations, lok
    populations = ['ITU','CHB','CHS','STU','MXL','CEU','GIH','IBS','KHV','GBR','TSI','PEL','FIN','BEB','CLM','JPT','PUR','CDX','PJL', 'Papuans']
    with open(path2, 'rb') as jsonf:
        lok = pickle.load(jsonf)
    with open(path2, 'rb') as jsonfe:
        lok = pickle.load(jsonfe)
    with open(path4, 'rb') as json_file:
        pop_chrom_dict = pickle.load(json_file)
    with open(path3, 'rb') as json_file:
        popdataf = pickle.load(json_file)
    with open(path5, 'rb') as json_file:
        pop_segment_dict = pickle.load(json_file)
    return populations, lok, pop_chrom_dict, popdataf, pop_segment_dict

def create_new(input, json_file):
    global populations, lok
    with open(json_file, "r") as file:
        populations = json.load(file)
    with open(json_file, "r") as file:
        populations = json.load(file)
    return populations, lok


def pare_og(boo, input=None, js=None):
    global populations, lok, pop_chrom_dict, popdataf, pop_segment_dict
    if boo: 
        populations, lok, pop_chrom_dict, popdataf, pop_segment_dict = create_og()
    else:
        populations, lok = create_new(input, js)

