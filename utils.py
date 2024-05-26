
from Further_prop import make_files
import pickle

# save_to ="/Users/eugeniaampofo/Downloads/Downloads/Vis_files/"
save_to = "/Users/eugeniaampofo/Downloads/Downloads/Sprime_files/visual/Chrom_Visual/Jupyter_Deliverables/data_files/"
# path2 = save_to + 'ov_num_df.pkl'  # dictionary that maps chromosome to dataframe with all populations
path2 = save_to + 'ov_num_dict.pkl'
path3 = save_to + 'pop_dataf.pkl'  # dictionary that maps population to dataframe
path4 = save_to + 'pop_chrom_dict.pkl'  # dictionary that maps chromosome to dataframe with all populations
path5 = save_to + "concatenated_dict.pkl"
path6 = save_to + "ov_dict.pkl"
path7 =  save_to + "ov_full_df.pkl"




populations = []

lok = {}
pop_chrom_dict = {}
popdataf ={}
concatenated_dict = {}
ov_dict = {}
ov_full_df = None


def create_og():
    global populations, lok, pop_chrom_dict, popdataf, concatenated_dict, ov_dict, ov_full_df
    populations = ['ITU','CHB','CHS','STU','MXL','CEU','GIH','IBS','KHV','GBR','TSI','PEL','FIN','BEB','CLM','JPT','PUR','CDX','PJL', 'Papuans']
    with open(path2, 'rb') as jsonf:
        lok = pickle.load(jsonf)
    with open(path4, 'rb') as json_file:
        pop_chrom_dict = pickle.load(json_file)
    with open(path3, 'rb') as json_file:
        popdataf = pickle.load(json_file)
    with open(path5, 'rb') as json_file:
        concatenated_dict = pickle.load(json_file)
    with open(path6, 'rb') as json_file:
        ov_dict = pickle.load(json_file)
    with open(path7, "rb") as json_file:
        ov_full_df  = pickle.load(json_file)
   


def create_new(input, sav, json_file):
    global populations, lok, pop_chrom_dict, popdataf, concatenated_dict, ov_dict, ov_full_df
    populations, lok, pop_chrom_dict, popdataf, concatenated_dict, ov_dict,  ov_full_df= make_files(input, sav, json_file)


def pare_og(boo, input=None, sav=None, js=None):
    if boo: 
        create_og()
    else:
        create_new(input, sav,js) 

def add_on2(df1,df2):
    s = [None for x in range(len(df1))]
    e = [None for x in range(len(df1))]
    start_end_list = list(zip(df2["CHROM"], df2['START'], df2['END']))
    input_list = list(zip(df1["CHROM"], df1['POS']))
    for index1, row1 in enumerate(input_list):
        # Iterate over each row in df2
        for chrom, start, end in start_end_list:
            if row1[0] == chrom:
                # Check if POS falls between START and END
                if start <= row1[1] <= end:
                    # Set START and END values from df2 to df1
                    s[index1] = int(start)
                    e[index1] = int(end)
                    break  # Break the inner loop if condition is satisfied   
    return s, e
                    

def addy(k):
    global concatenated_dict, ov_dict
    print(concatenated_dict.keys())
    # print(ov_dict.keys())
    df1 = concatenated_dict[k[0]]
    df2 = concatenated_dict[k[1]]
    ov = ov_dict['-'.join(k)]
    # print(ov)
    f1, f2 = add_on2(df1, ov)
    t1, t2 = add_on2(df2, ov)
    df1["START_2"] = f1
    df2["START_2"] = t1
    df1["END_2"] = f2
    df2["END_2"] = t2
    df1 = df1.dropna()  
    df2 = df2.dropna()  
    df1["START_2"] = df1["START_2"].astype(int)
    df1["END_2"] = df1["END_2"].astype(int)  
    df2["START_2"] = df2["START_2"].astype(int)
    df2["END_2"] = df2["END_2"].astype(int)
    df1 = df1.sort_values(by=["CHROM", "START"], ascending=True)
    ov = ov.sort_values(by=["CHROM", "START"], ascending=True)

    return  ov, df1, df2

def flatten_and_sort_lists(list1, list2):
    # Flatten the lists of tuples into a single list
    flattened_list = [item for sublist in list1 for item in sublist] + [item for sublist in list2 for item in sublist]
    # Sort the flattened list
    sorted_list = sorted(flattened_list)
    
    return sorted_list