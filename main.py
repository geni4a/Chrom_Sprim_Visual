from bokeh.io import curdoc
from bokeh.layouts import row, column
from bokeh.models import Button
from utils import pare_og


user_input = input("Will you be submitting your own files? Enter Y or N:")
while user_input != "N" and user_input != "Y":
    print("Incorrect output")
    user_input = input("Will you be submitting your own files? Enter Y or N:")
if user_input == "N":
    pare_og(True)
elif user_input == "Y":
    print("Ensure your files are in the appropriate format according to README")
    print("Ensure your next inputs are in correct format. Check with README")
    input1 = input("Enter path to directory containing Sprime outputs: ")
    input2 = input("Enter path to json file containing names of populations: ")
    input3 = input("Enter path to save inbetween files: ")
    pare_og(False, input1,input3, input2)

# Initialize a list to keep track of added components
added_components = []

    
from overlap_lookup import ret_ov
from chrom_vis import ret2
from segment_lookup import ret_ov3
from snp_lookup import ret_s

# Function to toggle layout to circle SVG
def toggle_circle():
    clear_layout()
    r = ret_s()
    layout.children.append(r)
    added_components.append(r)

def toggle_chromvis():
    clear_layout()
    r = ret2()
    layout.children.append(r)
    added_components.append(r)

def clear_layout():
  if added_components:
    removed_component = added_components.pop()
    print(removed_component)
    layout.children.remove(removed_component)
def ove():
    clear_layout()
    r = ret_ov()
    layout.children.append(r)
    added_components.append(r)


def ove2():
    clear_layout()
    r = ret_ov3()
    layout.children.append(r)
    added_components.append(r)
# Create a button to trigger the layout clearing
clear_button = Button(label="Clear Layout")
clear_button.on_click(clear_layout)
    
# Create buttons to toggle layouts
button_rectangle = Button(label="Chromosome Pair Sharing Visual")
button_rectangle.on_click(toggle_chromvis)

button_circle = Button(label="SNP Lookup")
button_circle.on_click(toggle_circle)

button_ov = Button(label="Overlap Lookup")
button_ov.on_click(ove)

button_ov2 = Button(label="Segment Lookup")
button_ov2.on_click(ove2)



button_row = row(button_rectangle, button_circle,button_ov,button_ov2,clear_button)
    # Arrange buttons and Div widget in a column layout
layout = column(button_row)




# Add the layout to the document
curdoc().add_root(layout)
      







