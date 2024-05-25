
from Further_prop import make_files
import pickle

save_to ="/Users/eugeniaampofo/Downloads/Downloads/Vis_files/"
save_to = "/Users/eugeniaampofo/Downloads/Downloads/Vis_files/"
# path2 = save_to + 'ov_num_df.pkl'  # dictionary that maps chromosome to dataframe with all populations
path2 = save_to + 'ov_num_dict.pkl'
path3 = save_to + 'popdataf.pkl'  # dictionary that maps population to dataframe
path4 = save_to + 'pop_chrom_dict.pkl'  # dictionary that maps chromosome to dataframe with all populations
# path5 = save_to + "pop_segment_dict.pkl"
path5 = save_to + "concatenated_dict.pkl"
path6 = save_to + "ov_dict.pkl"
path7 =  save_to + "ov_full_df.pkl"




populations = []

lok = {}
pop_chrom_dict = {}
popdataf ={}
pop_segment_dict = {}
ov_dict = {}
ov_full_df = None


def create_og():
    global populations, lok, pop_chrom_dict, popdataf, pop_segment_dict, ov_dict, ov_full_df
    populations = ['ITU','CHB','CHS','STU','MXL','CEU','GIH','IBS','KHV','GBR','TSI','PEL','FIN','BEB','CLM','JPT','PUR','CDX','PJL', 'Papuans']
    with open(path2, 'rb') as jsonf:
        lok = pickle.load(jsonf)
    with open(path4, 'rb') as json_file:
        pop_chrom_dict = pickle.load(json_file)
    with open(path3, 'rb') as json_file:
        popdataf = pickle.load(json_file)
    with open(path5, 'rb') as json_file:
        pop_segment_dict = pickle.load(json_file)
    with open(path6, 'rb') as json_file:
        ov_dict = pickle.load(json_file)
    with open(path7, "rb") as json_file:
        ov_full_df  = pickle.load(json_file)
   


def create_new(input, sav, json_file):
    global populations, lok, pop_chrom_dict, popdataf, pop_segment_dict, ov_dict, ov_full_df
    populations, lok, pop_chrom_dict, popdataf, pop_segment_dict, ov_dict,  ov_full_df= make_files(input, sav, json_file)


def pare_og(boo, input=None, sav=None, js=None):
    if boo: 
        create_og()
    else:
        create_new(input, sav,js) 

