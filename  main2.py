from bokeh.io import curdoc
from bokeh.layouts import row, column
from bokeh.models import Button, Div
from snp_lookup import ret_s
from chrom_vis import ret2
from overlap_lookup import ret_ov


# Initialize a list to keep track of added components
added_components = []

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
    print("S")
    layout.children.remove(removed_component)

def ove():
    clear_layout()
    r = ret_ov()
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

# Arrange buttons in a row layout
button_row = row(button_rectangle, button_circle,button_ov,clear_button)

# Arrange buttons and Div widget in a column layout

layout = column(button_row)
# Add the layout to the document



def go():
    user_input = input("Will you be submitting your own files? Enter Y or N:")
    if user_input == "N":
        curdoc().add_root(layout)
    elif user_input == "Y":
        print("Ensure your files are in the appropriate format according to README")
        input1 = input("Enter path to directory containing Sprime outputs")
        input2 = input("Enter path to json file containing names of populations")
    else:
        print("Incorrect output.")

go()

      















