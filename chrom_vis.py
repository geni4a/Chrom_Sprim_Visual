from bokeh.io import curdoc
from bokeh.plotting import figure
from bokeh.models import BoxAnnotation, Button, TapTool, Div
from bokeh.layouts import column
import numpy as np 


# Define constants
mini_chr1 = 0
maxi_chr1 = 0
chromosome_width_chr1 = 10
part_width_chr1 = 1
criteria_regions_1 = [(5, 20), (35, 42)]

mini_chr2 = 0
maxi_chr2 = 0
chromosome_width_chr2 = 10
part_width_chr2 = 1
criteria_regions_2 = [(10, 30), (85, 90)]
overlaps = [(10, 20)]

end_part = 100  # maximum chromosome value for both chromosomes
increment = 10

view_start = 1
view_end = 11
# Create Bokeh figure
p = figure(width=800, height=200, title="Variant Sharing")
p.xaxis.ticker = [i for i in range(view_start, view_end)]


# Create lists to store colors for each part of the chromosome
colors_chr1 = []
colors_chr2 = []

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

# Create the HTML component with the layout
textbox_layout = """
<div style="position:absolute; top:10px; left:100px; width:200px; height:100px;">
    <div id="textbox_content"></div>
</div>
"""

# Create the Div widget with the layout
textbox = Div(text=textbox_layout)




def tap_callback(event):
    selected_index = event.x / part_width_chr1
    boo, k =  is_within_any_bounds2(selected_index, overlaps)
    boo2, k2 = is_within_any_bounds2(selected_index, criteria_regions_1)
    boo3, k3 =  is_within_any_bounds2(selected_index, criteria_regions_2)
    if boo:
        if (-5 <= event.y <= 5) or (-20 <= event.y <= -10):
            highlight_box_ov.visible = True
            highlight_box_ov.left = k -0.5
            highlight_box_ov.right = k+0.5
            highlight_box_chr1.visible = False
            highlight_box_chr2.visible = False
            textbox.text = f"Selected part of overlap: {selected_index} {k}"
        else:
            highlight_box_chr1.visible = False
            highlight_box_chr2.visible = False
            highlight_box_ov.visible = False
            textbox.text = ""
            textbox.text = f"Selected part of Chromosome 2: {selected_index} "

    elif -5 <= event.y <= 5 and boo2:  # Clicked on Chromosome 1
        textbox.text = f"Selected part of Chromosome 1: {selected_index}, {k2} "
        highlight_box_chr1.visible = True
        highlight_box_chr1.left = k2* part_width_chr1-0.5
        highlight_box_chr1.right = k2* part_width_chr1+0.5
        highlight_box_chr2.visible = False
        highlight_box_ov.visible = False        
    elif -20 <= event.y <= -10 and boo3:  # Clicked on Chromosome 2
        textbox.text = f"Selected part of Chromosome 2: {selected_index}, {k3} "
        highlight_box_chr2.visible = True
        highlight_box_chr2.left = k3* part_width_chr2-0.5
        highlight_box_chr2.right = k3* part_width_chr2+0.5
        highlight_box_chr1.visible = False
        highlight_box_ov.visible = False
    else:
        highlight_box_chr1.visible = False
        highlight_box_chr2.visible = False
        highlight_box_ov.visible = False
        textbox.text = f"Selected part of Chromosome 2: {selected_index}, {np.floor(selected_index)}"



# Customize plot properties
p.xaxis.axis_label = "Position"
p.yaxis.axis_label = "Chromosome"
p.grid.grid_line_color = None
# Create TapTool to detect clicks on the plot
tap_tool = TapTool()
p.add_tools(tap_tool)
p.add_layout(highlight_box_chr1)
p.add_layout(highlight_box_chr2)
p.add_layout(highlight_box_ov)

# Attach the event handler function to the plot
p.on_event('tap', tap_callback)

# Create layout with plot and buttons
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
    # Draw the chromosome parts for the current view window
    for i in range(view_start, view_end):
        x_position_chr1 = (i) * part_width_chr1
        if is_within_any_bounds(i, overlaps):
            colors_chr1.append("purple")
        elif is_within_any_bounds(i, criteria_regions_1):
            colors_chr1.append("red")
        else:
            colors_chr1.append("navy")
        p.rect(x=x_position_chr1, y=0, width=part_width_chr1, height=chromosome_width_chr1,
            color=colors_chr1[i-1], alpha=0.5)

        x_position_chr2 = (i)  * part_width_chr2
        if is_within_any_bounds(i, overlaps):
            colors_chr2.append("purple")
        elif is_within_any_bounds(i, criteria_regions_2):
            colors_chr2.append("orange")
        else:
            colors_chr2.append("green")
        p.rect(x=x_position_chr2, y=-15, width=part_width_chr2, height=chromosome_width_chr2,
            color=colors_chr2[i-1], alpha=0.5)
    # Update x-axis range
    p.x_range.start = view_start
    p.x_range.end = view_end
    p.xaxis.ticker = [i for i in range(view_start, view_end)]



# Function to check if a number is within any of the given bounds
def is_within_any_bounds(number, bounds_list):
    for bounds in bounds_list:
        if bounds[0] <= number <= bounds[1]:
            return True
    return False

def is_within_any_bounds2(number, bounds_list):
    q = np.ceil(number) #5 #6
    m = np.floor(number) #4 #5
    p = q-0.5
    x = float("inf")
    if number > p:
        x =  q
    else:
        x = m
    for bounds in bounds_list:
        if bounds[0] <= x <= bounds[1]:
            return True, x
    return False, x

# Function to handle next button click
def next_button_callback():
    global view_start, view_end
    if  view_start < end_part and view_start >= 1:
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
interface2 = column(textbox, p, next_button, previous_button)

def ret2():
    return interface2


