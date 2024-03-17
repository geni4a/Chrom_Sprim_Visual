from bokeh.io import curdoc
from bokeh.models import TextInput, Button, Div
from bokeh.layouts import column
import pandas as pd
import pickle
import time

save_to = "/Users/eugeniaampofo/Downloads/Downloads/Vis_files/"

path = save_to + 'popdataf.pkl'  # dictionary that maps population to dataframe
path2 = save_to + 'pop_chrom_dict.pkl'  # dictionary that maps chromosome to dataframe with all populations

def update_list():
    input_text = text_input.value
    if input_text:
        loading_message.visible = True
        paragraph.text = ""
        curdoc().add_next_tick_callback(lambda: process_input(input_text))
    else:
        paragraph.text = ""
        loading_message.visible = False

# Function to process the input and generate DataFrame
def process_input(input_text):
    # Simulate a delay to demonstrate loading
    time.sleep(2)
    paragraph.text = generate_dataframe(input_text)
    loading_message.visible = False

# Function to generate DataFrame based on user input
def generate_dataframe(input_text):
    filtered_df = pd.DataFrame()
    # Sample DataFrame (replace this with your own)
    with open(path2, 'rb') as json_file:
        dictionary = pickle.load(json_file)

    # Filter DataFrame based on user input
    for chrom in dictionary:
        for pop in dictionary[chrom]:
            df1 = dictionary[chrom][pop]
            filt = df1[df1["ID"].str.contains(input_text, case=False)]
            if not filt.empty:
                filtered_df = pd.concat([filtered_df, filt], ignore_index=True)
    if filtered_df.empty:
        return "None Found"
    else:
        # Convert DataFrame to HTML table
        html_table = "<table border='1' cellspacing='0' cellpadding='5'>"
        html_table += "<tr><th>" + "</th><th>".join(filtered_df.columns) + "</th></tr>"
        for index, row in filtered_df.iterrows():
            html_table += "<tr>"
            html_table += "<td>" + "</td><td>".join(str(cell) for cell in row.values) + "</td>"
            html_table += "</tr>"
        html_table += "</table>"

    return html_table

# Create input widget
text_input = TextInput(placeholder="Type SNP here")

# Create button widget
button = Button(label="Search")

# Create Div to display DataFrame as HTML table
paragraph = Div()

# Loading message
loading_message = Div(text="Loading...", visible=False)

# Callback for button click
button.on_click(update_list)

# Layout
interface1 = column(text_input, button, loading_message, paragraph)

def ret_s():
    return interface1