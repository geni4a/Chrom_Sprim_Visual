import pandas as pd
import numpy as np
import os
import pickle
import pybedtools
from itertools import combinations
import json


# In[ ]:


sprime_files = ""
save_to =""
populations = []
jsone=""

ov_chrom_df = pd.DataFrame(columns=populations, index=populations)



def population_ret():
    global populations, jsone                   
    with open(jsone, 'r') as file:
        populations = json.load(file)
    print(f"The populations are {populations}")
#population_ret(file)
#populations = sorted(populations)


# In[ ]:


#Generate all pairs of populations outside the chromosome loop
population_pairs = list(combinations(populations, 2))
population_pairs = [sorted(list(x)) for x in population_pairs]
# print(population_pairs)


# In[ ]:


# len(population_pairs)


# In[ ]:


pop_dataf = {}

def populate():
   global pop_dataf
   for i in range(1, 23):
    pop_dataf[i] = {}
    for pop in populations:
        for file in os.listdir(sprime_files):
            if pop in file and f"chr{i}." in file:
                df= pd.read_csv(sprime_files + file, sep="\t")
                df["CHROM"] = df["CHROM"].astype(int)
                df["POS"] = df["POS"].astype(int)
                df["SEGMENT"] = df["SEGMENT"].astype(int)
                df_sorted = df.sort_values(by=["CHROM", "POS", "SEGMENT"], ascending=True)
                pop_dataf[i][pop] = df_sorted
        
# populate()
# pop_dataf["GIH"]


# In[ ]:


def store_popdataf():
    global pop_dataf
    with open(save_to + 'popdataf.pkl', 'wb') as json_file:
        pickle.dump(pop_dataf, json_file)
    
    with open(save_to + 'popdataf.pkl', 'rb') as json_file:
        pop_dataf = pickle.load(json_file)
#store_popdataf()
#pop_dataf["GIH"]


# In[ ]:


pop_chrom_dict = {}
def make_chrom_dict():
    global pop_dataf, pop_chrom_dict
    for i in range(1, 23):
        pop_chrom_dict[i] = {}
        for pop in populations:
            df_sorted = pop_dataf[i][pop]
            df2 = df_sorted[["CHROM", "POS", "SEGMENT"]]
            # Convert DataFrame to BedTool object
            bed_df = pybedtools.BedTool.from_dataframe(df2)
            # Group by segment number and find min/max position
            result = bed_df.groupby(g=3, c=[2], o=['min', 'max'])
            # Convert result to DataFrame
            result_df = result.to_dataframe(names=['SEGMENT', 'START', 'END'])
            # Group by the 'SEGMENT' column and find min/max values for other columns
            result_df = result_df.groupby('SEGMENT').agg({'START': 'min', 'END': 'max'}).reset_index()
            # Merge df1 and df2 based on the shared column
            merged_df = pd.merge(df_sorted, result_df, on='SEGMENT', how='left')
            pop_chrom_dict[i][pop] = merged_df



# In[ ]:


def store_chrom_dict():
    global pop_chrom_dict
    with open(save_to + 'pop_chrom_dict.pkl', 'wb') as json_file:
        pickle.dump(pop_chrom_dict, json_file)
    with open(save_to + 'pop_chrom_dict.pkl', 'rb') as json_file:
        pop_chrom_dict = pickle.load(json_file)
#store_chrom_dict
# pop_chrom_dict[22]["TSI"]
# df = pop_dataf["TSI"]
# df = df.loc[df["CHROM"] == 21]
# df


# In[ ]:





# In[ ]:


concatenated_dict = {}
def make_concat():
    # Iterate over each unique name
    for name in set(name for chrom_dict in pop_chrom_dict.values() for name in chrom_dict.keys()):
        # Collect DataFrames associated with the current name across chromosomes
        dfs = [chrom_dict[name] for chrom_dict in pop_chrom_dict.values() if name in chrom_dict]
        
        # Concatenate DataFrames into a single DataFrame
        concatenated_df = pd.concat(dfs, ignore_index=True)
        concatenated_df = concatenated_df.sort_values(by=["CHROM", "POS", "SEGMENT"], ascending=True)
        
        # Store the concatenated DataFrame in the new dictionary
        concatenated_dict[name] = concatenated_df
# make_concat()
# concatenated_dict["Papuans"]


# In[ ]:


def store_concat():
    global concatenated_dict
    with open(save_to + 'concatenated_dict.pkl', 'wb') as json_file:
        pickle.dump(concatenated_dict, json_file)
    with open(save_to + 'concatenated_dict.pkl', 'rb') as json_file:
        concatenated_dict = pickle.load(json_file)
# store_concat()


ov_dict = {}
def find_overlaps():
    # Iterate over chromosomes
    for pop in populations:
        k = [x for x in population_pairs if pop in x]
        df1 = concatenated_dict[pop][["CHROM", "START","END"]]
        df1 = df1.sort_values(by=["CHROM", "START"], ascending=True)
        df1 = df1.drop_duplicates(subset=['CHROM', 'START', 'END'])
        df1 = pybedtools.BedTool.from_dataframe(df1)
        for q in k:
            ov_name = "-".join(q)
            if ov_name not in ov_dict.keys():
                pair = q.copy()
                # print(pair)
                pair.remove(pop)
                # print(pair)
                df2 = concatenated_dict[pair[0]][["CHROM", "START","END"]]
                df2 =df2.drop_duplicates(subset=['CHROM', 'START', 'END'])
                df2 = df2.sort_values(by=["CHROM", "START"], ascending=True)
                df2 = pybedtools.BedTool.from_dataframe(df2)
                intersected_bed= df1.intersect(df2).sort().merge()
                ov_df = intersected_bed.to_dataframe(names=['CHROM', 'START', 'END'])#intersected_df
                ov_dict[ov_name] = ov_df.sort_values(by=["CHROM", "START"], ascending=True)
                count += 1
                del df2 
        del df1
# find_overlaps()
# ov_dict['CHB-ITU']


# In[ ]:


def store_overlaps():
    global ov_dict
    with open(save_to + 'ov_dict.pkl', 'wb') as json_file:
        pickle.dump(ov_dict, json_file)
    with open(save_to + 'ov_dict.pkl', 'rb') as json_file:
        ov_dict = pickle.load(json_file)
# store_overlaps()


# In[ ]:


# #461
# ov_dict['CHB-ITU']


# In[ ]:


def sum_seg(df):
    lol_both = [x[1]-x[0] for x in list(zip(df["START"],df["END"]))]
    return sum(lol_both)
ov_num_dict = {}
def calc_sharing():
    for chrom in range(1,23):
        ov_num_dict[chrom] ={}
        ov_df = pd.DataFrame(columns=populations, index=populations)
        pop_set = set()
        for pop in populations:
            k = [list(x) for x in population_pairs if pop in x]
            ov_df.at[pop,pop] = 1
            df1 = pop_chrom_dict[chrom][pop][["CHROM", "START", "END"]]
            sum_1 = sum_seg(df1)
            # print(pop)
            for ele in k:
                ov_name = "-".join(ele)
                pop_set.add(ov_name)
                # print(ov_name)
                pair = ele.copy()
                pair.remove(pop)
                df_both = ov_dict[ov_name].loc[ov_dict[ov_name]["CHROM"] == chrom]
                sum_b = sum_seg(df_both)
                ov_df.at[pop, pair[0]] = sum_b/sum_1
            # print(ov_df)
            # print(elrje)
        ov_num_dict[chrom] = ov_df
        # print(ov_df)
        # print(elrje)


def store_calc_sharing():
    with open(save_to + 'ov_num_dict.pkl', 'wb') as json_file:
        pickle.dump(ov_num_dict, json_file)
    with open(save_to + 'ov_num_dict.pkl', 'rb') as json_file:
        ov_num_dict = pickle.load(json_file)
# store_calc_sharing()



def final_calc_sharing():
    global ov_chrom_df
    for pop in populations:
        ov_chrom_df.at[pop,pop] = 1
        k = [list(x) for x in population_pairs if pop in x]
        sum_pop = 0
        for chrom in range(1, 23):
            df1 = pop_chrom_dict[chrom][pop][["CHROM", "START", "END"]]
            df1 = df1.drop_duplicates(subset=['CHROM', 'START', 'END'])
            sum_1 = sum_seg(df1)
            sum_pop += sum_1
        for ele in k:
            ov_name = "-".join(ele)
            pair = ele.copy()
            pair.remove(pop)
            df_both = ov_dict[ov_name]
            df_both = df_both.drop_duplicates(subset=['CHROM', 'START', 'END'])
            sum_b = sum_seg(df_both)
            ov_chrom_df.at[pop, pair[0]] = sum_b/sum_pop
    

def make_files(path1, path2, path3):
    global sprime_files, save_to, jsone, populations, ov_num_dict
    sprime_files = path1
    save_to = path2
    jsone = path3
    population_ret()
    print("Done 1/10")
    populate()
    print("Done 2/10")
    store_popdataf()
    print("Done 3/10")
    make_chrom_dict()
    print("Done 4/10")
    store_chrom_dict()
    print("Done 5/10")
    make_concat()
    print("Done 6/10")
    store_concat()
    print("Done 7/10")
    find_overlaps()
    print("Done 8/10")
    store_overlaps()
    print("Done 9/10")
    calc_sharing()
    print("Done 10/10")
    final_calc_sharing()
    return populations, ov_num_dict, pop_chrom_dict, pop_dataf, concatenated_dict, ov_dict, ov_chrom_df

    
# %%


#make_files("/Users/eugeniaampofo/Downloads/Downloads/Sprime_files/", "/Users/eugeniaampofo/Downloads/Downloads/Sprime_files/Vis2/","/Users/eugeniaampofo/Downloads/Downloads/Vis_files/populations.json")