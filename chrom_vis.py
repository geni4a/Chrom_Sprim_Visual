from bokeh.io import curdoc
from bokeh.plotting import figure
from bokeh.models import BoxAnnotation, Button, TapTool, Div, Select, TextInput
from bokeh.layouts import column
import numpy as np 
from utils import populations, pop_chrom_dict,addy, flatten_and_sort_lists
import pandas as pd


pop1 = None
pop2 = None
selected_number= 1
mode = "individual segments"
# Example usage
s = "/Users/eugeniaampofo/Downloads/Downloads/Sprime_files/visual/Chrom_Visual/Jupyter_Deliverables/Output_files_picke_and_images/"
df1 = None
df2 = None
criteria_regions_1 = None
criteria_regions_2 = None
end_part = None
chromosome_width = 10
increment = 50

view_start = -50
view_end = 0
# Create Bokeh figure
p = figure(width=1000, height=400, title="Variant Sharing")
p.visible = False

# Create lists to store colors for each part of the chromosome
colors_chr1 = []
colors_chr2 = []

paragraph = Div()
paragraph2 = Div()
paragraph2.visible = False

print(f"populatioons: {populations}")

def update_list():
    global mode, name, selected_number, df1, df2, criteria_regions_1, criteria_regions_2, end_part
    input_text = text_input.value
    try:
        paragraph.visible = False
        name = sorted(input_text.split(","))
        print(name)
        if name[0] not in populations or name[1] not in populations:
            paragraph.text = "Invalid input. Try again!"
            paragraph.visible = True
            paragraph2.visible = False
            p.visible = False
            next_button.visible = False
            previous_button.visible = False
        else:
            paragraph.visible = False
            if mode == "individual segments":
                nam_tup = tuple(name)
                ov, df1, df2 = addy(nam_tup)
                df1 = df1.drop_duplicates(subset=['CHROM', 'START', 'END'])
                df2 = df2.drop_duplicates(subset=['CHROM', 'START', 'END'])
                df1 = df1.loc[df1["CHROM"] == selected_number]
                df2 = df2.loc[df2["CHROM"] == selected_number]
                df1 = list(zip(df1['START'], df1['END']))
                df2 = list(zip(df2['START'], df2['END']))
                criteria_regions_1 = sorted([(x/1000000, y/1000000) for x,y in df1])
                criteria_regions_2 = sorted([(x/1000000, y/1000000) for x,y in df2])
                q = flatten_and_sort_lists(criteria_regions_1, criteria_regions_2)
                end_part = q[-1] # maximum chromosome value for both chromosomes
                paragraph2.text = "Done Loading"
                paragraph2.visible = True
                p.visible = True
                next_button.visible = True
                previous_button.visible = True

    except Exception as e:
        print("An error occurred.")
        print(f"Error type: {type(e).__name__}")
        print(f"Error details: {e}")
        paragraph.text = "Invalid input. Try again!"
        paragraph.visible = True


def filter_and_print_ranges(list1, list2, min_range, max_range):
    # Filter the entries in both lists that fall within the specified range
    filtered_list1 = [tup for tup in list1 if all(min_range <= x <= max_range for x in tup)]
    filtered_list2 = [tup for tup in list2 if all(min_range <= x <= max_range for x in tup)]
    # Print the filtered entries
    filt1 = []
    filt2 = []
    for entry in filtered_list1:
        filt1.append(entry)
    filt1 = sorted(filt1)

    for entry in filtered_list2:
        filt2.append(entry)
    filt2 = sorted(filt2)

    # Determine the new scaled down range
    all_filtered_entries = filtered_list1 + filtered_list2
    if all_filtered_entries:
        new_min = min(min(tup) for tup in all_filtered_entries)
        new_max = max(max(tup) for tup in all_filtered_entries)
        print(f"\nScaled Down Range: {new_min} - {new_max}")
    return filt1, filt2, new_min, new_max



# Customize plot properties
p.xaxis.axis_label = "Position in Mb"
p.yaxis.axis_label = "Chromosome"
p.grid.grid_line_color = None


# Function to update the display with new bars
def update_display():
    global view_start, view_end, colors_chr1, colors_chr2, increment
    # Clear the existing plot and color lists
    p.renderers = []
    # Update chromosome limits based on the current view window
    filtered_tuples1 = criteria_regions_1
    filtered_tuples2 = criteria_regions_2
    filt1, filt2, mini_chr1, mini_chr2 = filter_and_print_ranges(filtered_tuples1, filtered_tuples2, view_start, view_end)
    # Draw the chromosome parts for the current view windo
    for i in filt1:
        start, end = i
        width = end - start
        x_position = (start + end) / 2
        p.rect(x=x_position, y=0, width=width, height=chromosome_width,
            color="purple", alpha=0.5)
    for i in filt2:
        start, end = i
        width = end - start
        x_position = (start + end) / 2
        p.rect(x=x_position, y=-15, width=width, height=chromosome_width,
            color="orange", alpha=0.5)
    if view_start >=1 and view_end <= end_part:
        # Update x-axis range
        p.x_range.start = mini_chr1
        p.x_range.end = mini_chr2


# Function to handle next button click
def next_button_callback():
    global view_start, view_end
    view_start += increment
    view_end += increment
    if  0 <= view_start < end_part:
        update_display()
       
# Function to handle previous button click
def previous_button_callback():
    global view_start, view_end
    if view_start > 0:
        view_start -= increment
        view_end -= increment   
        update_display()
# Create buttons for next and previous
next_button = Button(label="Next", button_type="success")
next_button.on_click(next_button_callback)

previous_button = Button(label="Previous", button_type="success")
previous_button.on_click(previous_button_callback)
next_button.visible = False
previous_button.visible = False


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
text_input = TextInput(placeholder="Type Population pair names comma separated e.g JPT,ITU",width=400)

# Create button widget
button = Button(label="Load")

button.on_click(update_list)
interface2 = column(dropdown, dropdown2, text_input, paragraph, button,paragraph2, p, next_button, previous_button)



def ret2():
    return interface2

