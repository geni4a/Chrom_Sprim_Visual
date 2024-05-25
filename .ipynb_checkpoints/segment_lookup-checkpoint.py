
from bokeh.io import curdoc
from bokeh.models import TextInput, Button, Div, Select
from bokeh.layouts import column
import pandas as pd
from utils import pop_segment_dict,pop_chrom_dict


selected_number = 1

chrom_dict_values = {i: 250000000 for i in range(1, 23)}

dictionary = pop_segment_dict
pop_chrome = pop_chrom_dict

def update_list():
    global selected_number
    input_text = text_input.value
    input_text = input_text.split(":")
    selected_number = int(input_text[0])
    input_text = input_text[1].split("-")
    try:
        input_text = [int(x) for x in input_text]
        chrome = chrom_dict_values[selected_number]
        if input_text[0] <= chrome and input_text[1] <= chrome:
            loading_message.visible = True
            paragraph.text = ""
            curdoc().add_next_tick_callback(lambda: process_input(input_text, selected_number))
            loading_message.visible = False
        else:
            paragraph.text = "Invalid input. Try again!"
            loading_message.visible = False
    except:
        paragraph.text = "Invalid input. Try again!"
        loading_message.visible = False

    
# Function to process the input and generate DataFrame
def process_input(input_text,chrome):
    # Simulate a delay to demonstrate loading
    q,b = generate_dataframe(input_text,chrome)
    paragraph.text = q + "<br>"
    paragraph.text += b + "<br>"
    loading_message.visible = False



def generate_dataframe(input_text, chrom):
    filtered_df = pd.DataFrame()
    filtered_df2 = pd.DataFrame()
    # Sample DataFrame (replace this with your own)
    # Filter DataFrame based on user input
    for pop in dictionary:
        df1 = dictionary[pop]
        df1 = df1.loc[df1["CHROM"] == chrom]
        df1[['START', 'END']] = df1[['START', 'END']].astype(int)
        df1["population"] = df1.apply(lambda x: pop, axis=1)
        filt = df1[(df1['START'] <= input_text[0]) & (df1['END'] >= input_text[1])]
        filt1 = filt.drop_duplicates(subset=['CHROM', 'START', 'END'])

        if not filt.empty:
            filt2 = filt1[["CHROM", "START", "END", "population"]]
            filtered_df = pd.concat([filtered_df, filt2], ignore_index=True)
            filtered_df2 = pd.concat([filtered_df2, filt], ignore_index=True)
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
        html_table2 = "<table border='1' cellspacing='0' cellpadding='5'>"
        html_table2 += "<tr><th>" + "</th><th>".join(filtered_df2.columns) + "</th></tr>"
        for index, row in filtered_df2.iterrows():
            html_table2 += "<tr>"
            html_table2 += "<td>" + "</td><td>".join(str(cell) for cell in row.values) + "</td>"
            html_table2 += "</tr>"
        html_table2 += "</table>"

    return html_table, html_table2



# Create input widget
text_input = TextInput(placeholder="Type in this format: chrom:start-end", width=400)

# Create button widget
button = Button(label="Search")

# Create Div to display DataFrame as HTML table
paragraph = Div()

# Loading message
loading_message = Div(text="Loading...", visible=False)




# Callback for button clicked 
button.on_click(update_list)




# Layout
interface1 = column(text_input, button, loading_message, paragraph)

def ret_ov3():
    return interface1
  

