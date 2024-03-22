
"""####
Create a list of colors that match the number of segments per population
add in between colors

Plot

Overlay overlaps
####"""


from bokeh.io import curdoc
from bokeh.plotting import figure
from bokeh.models import BoxAnnotation, Button, TapTool, Div, Select, TextInput
from bokeh.layouts import column
import numpy as np 
import pickle
# sprime_files = "/Users/eugeniaampofo/Downloads/Downloads/Sprime_files/Sprime_res/"
save_to ="/Users/eugeniaampofo/Downloads/Downloads/Vis_files/"
save_to = "/Users/eugeniaampofo/Downloads/Downloads/Vis_files/"
# path2 = save_to + 'ov_num_df.pkl'  # dictionary that maps chromosome to dataframe with all populations
path2 = save_to + 'ov_num_dict.pkl'
path3 = save_to + 'popdataf.pkl'  # dictionary that maps population to dataframe
path4 = save_to + 'pop_chrom_dict.pkl'  # dictionary that maps chromosome to dataframe with all populations
# path5 = save_to + "pop_segment_dict.pkl"
path5 = save_to + "concatenated_dict.pkl"
path6 = save_to + "ov_dict.pkl"


lok = {}
pop_chrom_dict = {}
popdataf ={}
pop_segment_dict = {}
ov_dict = {}


def create_og():
    global populations, lok, pop_chrom_dict, popdataf, pop_segment_dict, ov_dict
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
    return populations, lok, pop_chrom_dict, popdataf, pop_segment_dict, ov_dict

create_og()

p = figure(width=800, height=200, title="Variant Sharing")

df1 = None
df2 = None
df11 = None
df22 = None
overlapse = None
overlapse11 = None
mode = None
denom = None

def inbet(original_list):
    result_list = []
    start = 1
    end = original_list[0][0] - 1
    if start <= end:
        result_list.append((start, end))

    # Iterate through the original list
    for i in range(len(original_list) - 1):
        start = original_list[i][1] + 1
        end = original_list[i + 1][0] - 1
        if start <= end:
            result_list.append((start, end))
    return result_list

def process_input(input_text1, chrome, mode):
    global df1, df2, overlapse, df11, df22, denom
    k = input_text1.split(",")
    pair = "-".join(sorted(k))
    print(pair)


    if k[0] and k[1] not in populations:
        return "Invalid input: one or both populations are incorrect!"
    chrom = int(chrome)
    overlapse = ov_dict[pair]
    overlapse = overlapse.loc[overlapse["CHROM"] == chrom]
    if mode == "individual segments":
        print(k[0])
        df1 = pop_chrom_dict[chrom][k[0]]
        # print(df1)
        df2 = pop_chrom_dict[chrom][k[0]]
    else:
        df1 = overlapse
        df2 = overlapse


def avg_len(lst):
    co = 0
    for tup in lst:
        co += tup[1]-tup[0]
    return co/len(lst)

mode = "individual segments"
process_input("GIH,TSI", "21", "individual segments")

df11 = df1[["CHROM","START", "END"]]

df11 = df11.drop_duplicates(subset=['CHROM', 'START', 'END'])
print(df11)
df11 = list(zip(df11["START"], df11["END"]))
df22 = df2.drop_duplicates(subset=['CHROM', 'START', 'END'])
df22 = list(zip(df22["START"], df22["END"]))
overlapse = list(zip(overlapse["START"], overlapse["END"]))
denom = np.mean([avg_len(df11), avg_len(df22), avg_len(overlapse)])


# print(df1)




# print(avg_len(df1))
# print(avg_len(df2))
# print(avg_len(overlapse))


 # Create lists to store colors for each part of the chromosome
colors_chr1 = []
colors_chr2 = []

def define_constants():
    global mini_chr1, mini_chr2, maxi_chr1, maxi_chr2, criteria_regions_1, criteria_regions_2 ,chromosome_height, part_width_chr1, overlaps,df1_lst,df2_lst,part_width_chr2,view_start,view_end, highlight_box_chr1, highlight_box_chr2, highlight_box_ov, end_part
        # # Define constants
    mini_chr1 = min(df11[0][0], df22[0][0])
    maxi_chr1 = max(df11[-1][1], df22[-1][1])
    chromosome_height= 10
    part_width_chr1 = 100
    criteria_regions_1 = df1
    df1_lst = inbet(df11)
    df2_lst = inbet(df22)
    mini_chr2 = min(df11[0][0], df22[0][0])
    maxi_chr2 = max(df11[-1][1], df22[-1][1])
    part_width_chr2 = 100
    criteria_regions_2 = df2
    overlaps = overlapse
    end_part = 100  # maximum chromosome value for both chromosomes
    increment = 180000

    view_start = 1
    view_end = increment
    # Create Bokeh figure
    # p.xaxis.ticker = [i for i in range(view_start, view_end)]
    # Create BoxAnnotations to highlight the selected regions for each chromosome
    highlight_box_chr1 = BoxAnnotation(left=mini_chr1, right=maxi_chr1, top=5, bottom=-5,
                                    line_color='black', line_width=2, line_alpha=0.5,
                                    visible=False, fill_color='#D55E00')
    highlight_box_chr2 = BoxAnnotation(left=mini_chr2, right=maxi_chr2, top=-10, bottom=-20,
                                    line_color='black', line_width=2, line_alpha=0.5,
                                    visible=False, fill_color='#D55E00')
    highlight_box_ov = BoxAnnotation(top=5, bottom=-20,
                                    line_color='black', line_width=2, line_alpha=0.5,
                                    visible=False, fill_color='#D55E00')


   

define_constants()

# Create the HTML component with the layout
textbox_layout = """
<div style="position:absolute; top:10px; left:100px; width:200px; height:100px;">
    <div id="textbox_content"></div>
</div>
"""

# Create the Div widget with the layout
textbox = Div(text=textbox_layout)

# Customize plot properties
p.xaxis.axis_label = "Position"
p.yaxis.axis_label = "Chromosome"
p.grid.grid_line_color = None
# Create TapTool to detect clicks on the plot
tap_tool = TapTool()
p.add_tools(tap_tool)

layout = column(p)

# Function to update the display with new bars
def update_display():
    global view_start, view_end, mini_chr1, maxi_chr1, mini_chr2, maxi_chr2, colors_chr1, colors_chr2, increment
    define_constants()
    # Clear the existing plot and color lists
    p.renderers = []

    # Update chromosome limits based on the current view window
    mini_chr1 = view_start
    maxi_chr1 = view_end
    mini_chr2 = view_start
    maxi_chr2 = view_end
    # print(view_start)
    # print(view_end)

    count = 0
    for tup in range(len(df1)):
        colors_chr1.append("red")
        count +=1
        diff = (df1[tup][1]-df1[tup][0])/denom
        p.rect(x=count, y=0, width=diff, height=chromosome_height,color=colors_chr1[tup], alpha=0.5)

    count = 0
    for tup in range(len(df2)):
        colors_chr2.append("blue")
        count +=1
        diff = (df2[tup][1]-df2[tup][0])/denom
        p.rect(x=count, y=-15, width=diff, height=chromosome_height, color=colors_chr2[tup], alpha=0.5)

    p.xaxis.ticker = [i for i in range(view_start, view_end)]


# Function to handle next button click
def next_button_callback():
    global view_start, view_end
    # if  view_start < end_part and view_start >= 1:
    update_display()
    view_start += increment
    view_end += increment


# Function to handle previous button click
def previous_button_callback():
    global view_start, view_end
    if view_start > 1:
        view_start -= increment
        view_end -= increment   
        update_display()

# Create buttons for next and previous
next_button = Button(label="Next", button_type="success")
next_button.on_click(next_button_callback)

previous_button = Button(label="Previous", button_type="success")
previous_button.on_click(previous_button_callback)

def dropdown_callback(attr, old, new):
    global selected_number
    selected_number = int(new)

options = [str(i) for i in range(1, 23)]  # Convert numbers to strings
dropdown = Select(title="Select chromosome number:", value=options[0], options=options)

# Attach the callback function to the 'value' property of the dropdown
dropdown.on_change('value', dropdown_callback)



def dropdown_callback2(attr, old, new):
    global mode
    mode = new

options2 = ["individual segments", "overlaps"]  # Convert numbers to strings
dropdown2 = Select(title="Select chromosome number:", value=options2[0], options=options2)

# Attach the callback function to the 'value' property of the dropdown
dropdown2.on_change('value', dropdown_callback)

# Create input widget
text_input = TextInput(placeholder="Type Population pair names comma separated e.g (JPT,ITU)",width=400)

# Create button widget
button = Button(label="Search")

interface2 = column(textbox, dropdown, dropdown2, text_input, button, p, next_button, previous_button)

def ret2():
    # define_constants()
    return interface2

curdoc().add_root(ret2())

