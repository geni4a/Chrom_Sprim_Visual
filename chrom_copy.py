
# """####
# Create a list of colors that match the number of segments per population
# add in between colors

# Plot

# Overlay overlaps
# ####"""


# from bokeh.io import curdoc
# from bokeh.plotting import figure
# from bokeh.models import BoxAnnotation, Button, TapTool, Div, Select, TextInput
# from bokeh.layouts import column
# import numpy as np 
# from utils import populations, lok, pop_segment_dict, pop_chrom_dict, ov_dict


# df1 = None
# df2 = None
# overlapse = None
# mode = None


# def inbet(original_list):
#     result_list = []
#     start = 1
#     end = original_list[0][0] - 1
#     if start <= end:
#         result_list.append((start, end))

#     # Iterate through the original list
#     for i in range(len(original_list) - 1):
#         start = original_list[i][1] + 1
#         end = original_list[i + 1][0] - 1
#         if start <= end:
#             result_list.append((start, end))
#     return result_list

# def process_input(input_text1, chrome):
#     global df1, df2, overlapse
#     k = input_text1.split(",")
#     if k[0] and k[1] not in populations:
#         return "Invalid input: one or both populations are incorrect!"
#     chrom = int(chrome)
#     df1 = pop_chrom_dict[chrom][k[0]]
#     df1[['START', 'END']] = df1[['START', 'END']].astype(int)

#     # df1['start'] = df1['start'].astype(int)
#     # df1['end'] = df1['Column1'].astype(int)

#     df1 = list(zip(df1['START'], df1['END']))
#     df2 = pop_chrom_dict[chrom][k[1]]
#     df2[['START', 'END']] = df2[['START', 'END']].astype(int)
#     df2 = list(zip(df2['START'], df2['END']))
#     k = sorted(k)
#     name = f"{k[0]}-{k[1]}"
#     overlaps = ov_dict[name]
#     print(chrome)
#     # print(overlaps)
#     overlaps = overlaps.loc[overlaps["CHROM"] == chrom]
#     print(overlaps)
#     overlaps[['START', 'END']] = overlaps[['START', 'END']].astype(int)
#     print(overlapse)

#     overlapse = list(zip(overlaps['START'], overlaps['END']))

# process_input("GIH,TSI", "21")

# def avg_len(lst):
#     co = 0
#     for tup in lst:
#         co += tup[1]-tup[0]
#     return co/len(lst)

# # print(avg_len(df1))
# # print(avg_len(df2))
# # print(avg_len(overlapse))
# denom = np.mean([avg_len(df1), avg_len(df2), avg_len(overlapse)])





# # Define constants
# mini_chr1 = min(df1[0][0], df2[0][0])
# maxi_chr1 = max(df1[-1][1], df2[-1][1])
# chromosome_height= 10
# part_width_chr1 = 100
# criteria_regions_1 = df1
# df1_lst = inbet(df1)
# # print(df1[:5])
# # print(df1_lst[:5])
# # print(ldjf)
# # print(mini_chr1)
# # print(maxi_chr1)


# mini_chr2 = min(df1[0][0], df2[0][0])
# maxi_chr2 = max(df1[-1][1], df2[-1][1])
# part_width_chr2 = 100
# criteria_regions_2 = df2
# overlaps = overlapse

# end_part = 100  # maximum chromosome value for both chromosomes
# increment = 180000

# view_start = 1
# view_end = increment
# # Create Bokeh figure
# p = figure(width=800, height=200, title="Variant Sharing")
# p.xaxis.ticker = [i for i in range(view_start, view_end)]


# # Create lists to store colors for each part of the chromosome
# colors_chr1 = []
# colors_chr2 = []

# # Create BoxAnnotations to highlight the selected regions for each chromosome
# highlight_box_chr1 = BoxAnnotation(left=mini_chr1, right=maxi_chr1, top=5, bottom=-5,
#                                    line_color='black', line_width=2, line_alpha=0.5,
#                                    visible=False, fill_color='#D55E00')
# highlight_box_chr2 = BoxAnnotation(left=mini_chr2, right=maxi_chr2, top=-10, bottom=-20,
#                                    line_color='black', line_width=2, line_alpha=0.5,
#                                    visible=False, fill_color='#D55E00')
# highlight_box_ov = BoxAnnotation(top=5, bottom=-20,
#                                  line_color='black', line_width=2, line_alpha=0.5,
#                                  visible=False, fill_color='#D55E00')

# # Create the HTML component with the layout
# textbox_layout = """
# <div style="position:absolute; top:10px; left:100px; width:200px; height:100px;">
#     <div id="textbox_content"></div>
# </div>
# """

# # Create the Div widget with the layout
# textbox = Div(text=textbox_layout)

# # Customize plot properties
# p.xaxis.axis_label = "Position"
# p.yaxis.axis_label = "Chromosome"
# p.grid.grid_line_color = None
# # Create TapTool to detect clicks on the plot
# tap_tool = TapTool()
# p.add_tools(tap_tool)
# p.add_layout(highlight_box_chr1)
# p.add_layout(highlight_box_chr2)
# p.add_layout(highlight_box_ov)

# # Attach the event handler function to the plot
# # p.on_event('tap', tap_callback)

# # Create layout with plot and buttons
# layout = column(p)

# # Function to update the display with new bars
# def update_display():
#     global view_start, view_end, mini_chr1, maxi_chr1, mini_chr2, maxi_chr2, colors_chr1, colors_chr2, increment
    
#     # Clear the existing plot and color lists
#     p.renderers = []

#     # Update chromosome limits based on the current view window
#     mini_chr1 = view_start
#     maxi_chr1 = view_end
#     mini_chr2 = view_start
#     maxi_chr2 = view_end
#     print(view_start)
#     print(view_end)

#     count = 0
#     for tup in range(len(df1)):
#         colors_chr1.append("red")
#         count +=1
#         diff = (df1[tup][1]-df1[tup][0])/denom
#         p.rect(x=count, y=0, width=diff, height=chromosome_height,color=colors_chr1[tup], alpha=0.5)

#     count = 0
#     for tup in range(len(df2)):
#         colors_chr2.append("blue")
#         count +=1
#         diff = (df2[tup][1]-df2[tup][0])/denom
#         p.rect(x=count, y=-15, width=diff, height=chromosome_height, color=colors_chr2[tup], alpha=0.5)

#     p.xaxis.ticker = [i for i in range(view_start, view_end)]


# # Function to handle next button click
# def next_button_callback():
#     global view_start, view_end
#     # if  view_start < end_part and view_start >= 1:
#     update_display()
#     view_start += increment
#     view_end += increment


# # Function to handle previous button click
# def previous_button_callback():
#     global view_start, view_end
#     if view_start > 1:
#         view_start -= increment
#         view_end -= increment   
#         update_display()

# # Create buttons for next and previous
# next_button = Button(label="Next", button_type="success")
# next_button.on_click(next_button_callback)

# previous_button = Button(label="Previous", button_type="success")
# previous_button.on_click(previous_button_callback)

# def dropdown_callback(attr, old, new):
#     global selected_number
#     selected_number = int(new)

# options = [str(i) for i in range(1, 23)]  # Convert numbers to strings
# dropdown = Select(title="Select chromosome number:", value=options[0], options=options)

# # Attach the callback function to the 'value' property of the dropdown
# dropdown.on_change('value', dropdown_callback)



# def dropdown_callback2(attr, old, new):
#     global selected_number
#     selected_number = int(new)

# options2 = ["individual segments", "overlaps"]  # Convert numbers to strings
# dropdown2 = Select(title="Select mode:", value=options2[0], options=options2)

# # Attach the callback function to the 'value' property of the dropdown
# dropdown2.on_change('value', dropdown_callback)

# # Create input widget
# text_input = TextInput(placeholder="Type Population pair names comma separated e.g (JPT,ITU)",width=400)

# # Create button widget
# button = Button(label="Search")

# interface2 = column(textbox, dropdown, text_input, button, p, next_button, previous_button)

# def ret2():
#     return interface2


# # ret2()


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
from utils import populations, lok, pop_segment_dict, pop_chrom_dict, ov_dict



df1 = None
df2 = None
df11 = None
df22 = None
overlapse = None
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
    if k[0] and k[1] not in populations:
        return "Invalid input: one or both populations are incorrect!"
    chrom = int(chrome)
    if mode == "individual segments":
        print(k[0])
        df1 = pop_chrom_dict[chrom][k[0]]
        print(df1)
        df2 = pop_chrom_dict[chrom][k[0]]
    else:
        pair = "-".join(sorted(k))
        print(pair)
        overlapse = ov_dict[pair]
        overlapse = overlapse.loc[overlapse["CHROM" == chrom]]

        df1 = overlapse
        df2 = overlapse
def avg_len(lst):
    co = 0
    for tup in lst:
        co += tup[1]-tup[0]
    return co/len(lst)

p = figure(width=800, height=200, title="Variant Sharing")


df11 = list(zip(df1["START"], df1["END"]))
df22 = list(zip(df2["START"], df2["END"]))
denom = np.mean([avg_len(df11), avg_len(df22), avg_len(overlapse)])

# mode = "individual segments"
# process_input("GIH,TSI", "21", "individual segments")
# print(df1)




# print(avg_len(df1))
# print(avg_len(df2))
# print(avg_len(overlapse))




# def define_constants():
#     global mini_chr1, mini_chr2, maxi_chr1, maxi_chr2, criteria_regions_1, criteria_regions_2 ,chromosome_height, part_width_chr1, overlaps,df1_lst,df2_lst,part_width_chr2,view_start,view_end
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
p.xaxis.ticker = [i for i in range(view_start, view_end)]


# Create lists to store colors for each part of the chromosome
colors_chr1 = []
colors_chr2 = []

# # Create BoxAnnotations to highlight the selected regions for each chromosome
# highlight_box_chr1 = BoxAnnotation(left=mini_chr1, right=maxi_chr1, top=5, bottom=-5,
#                                    line_color='black', line_width=2, line_alpha=0.5,
#                                    visible=False, fill_color='#D55E00')
# highlight_box_chr2 = BoxAnnotation(left=mini_chr2, right=maxi_chr2, top=-10, bottom=-20,
#                                    line_color='black', line_width=2, line_alpha=0.5,
#                                    visible=False, fill_color='#D55E00')
# highlight_box_ov = BoxAnnotation(top=5, bottom=-20,
#                                  line_color='black', line_width=2, line_alpha=0.5,
#                                  visible=False, fill_color='#D55E00')

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
    # Clear the existing plot and color lists
    p.renderers = []

    # Update chromosome limits based on the current view window
    mini_chr1 = view_start
    maxi_chr1 = view_end
    mini_chr2 = view_start
    maxi_chr2 = view_end
    print(view_start)
    print(view_end)

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


