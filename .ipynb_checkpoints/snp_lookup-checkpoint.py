from bokeh.io import curdoc
from bokeh.models import TextInput, Button, Div
from bokeh.layouts import column
import pandas as pd
from utils import pop_chrom_dict

dictionary = pop_chrom_dict

def update_list():
    input_text = text_input.value
    inpute = input_text.split(":")
    chrom = int(inpute[0])
    variant =  inpute[1]
    if input_text:
        paragraph.text = ""
        curdoc().add_next_tick_callback(lambda: process_input(chrom, variant))
    else:
        paragraph.text = ""
        loading_message.visible = False

# Function to process the input and generate DataFrame
def process_input(chrom, variant):
    # Simulate a delay to demonstrate loading
    paragraph.text = generate_dataframe(chrom, variant)

# Function to generate DataFrame based on user input
def generate_dataframe(chrom, variant):
    global loading_message
    loading_message.visible = True

    filtered_df = pd.DataFrame()
    # Sample DataFrame (replace this with your own)
   
    # Filter DataFrame based on user input
    for pop in dictionary[chrom]:
        df1 = dictionary[chrom][pop]
        df1["population"] = df1.apply(lambda x: pop, axis=1)
        df1["POS"] = df1['POS'].astype(str)
        filt = df1[df1["POS"].str.contains(variant, case=False)]

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
    loading_message.visible = False

    return html_table

# Create input widget
text_input = TextInput(placeholder="Type Position here")

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