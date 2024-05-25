from bokeh.io import curdoc
from bokeh.models import TextInput, Button, Div, Select
from bokeh.layouts import column
import pandas as pd
from utils import populations, lok, ov_full_df


selected_number = 1
format = "Full Genome"

def update_list():
    input_text = text_input.value
    if input_text in populations:
        loading_message.visible = True
        paragraph.text = ""
        curdoc().add_next_tick_callback(lambda: process_input(input_text))
        loading_message.visible = False
    else:
        paragraph.text = "Invalid input. Try again!"
        loading_message.visible = False

# Function to process the input and generate DataFrame
def process_input(input_text):
    # Simulate a delay to demonstrate loading
    a, b, c , d = generate_dataframe(input_text)
    if format == "Full Genome":
        m_t = f"{a} is the population which shares the most with {input_text} with sharing proportion of {b}"
    else:
        m_t = f"{a} is the population which shares the most with {input_text} on chromosome {selected_number} with score {b}"

    paragraph.text += m_t + "<br>"
    paragraph.text += c+ "<br>"
    paragraph.text += d+ "<br>"
    loading_message.visible = False

def second_largest_value_and_column(row_label,df):
    row_values = df.loc[row_label]
    sorted_values = sorted(row_values, reverse=True)
    second_largest = sorted_values[1]  # Indexing starts from 0
    second_largest_column = row_values[row_values == second_largest].index[0]
    return second_largest_column, second_largest

# Function to generate DataFrame based on user input
def generate_dataframe(input_text):
    if input_text not in populations:
        return "Invalid input"
    if format == "Full Genome":
        df1 = ov_full_df
    else:
        # Sample DataFrame (replace this with your own)
        df1 = lok[selected_number]
    filtered_df = df1
    col, val = second_largest_value_and_column(input_text, df1)
    # Convert DataFrame to HTML table
    html_table = "<table border='1' cellsƒcing='0' cellpadding='5'>"
    # Include row names as the first column
    html_table += "<tr><th></th><th>" + "</th><th>".join(filtered_df.columns) + "</th></tr>"
    for index, row in filtered_df.iterrows():
        html_table += "<tr>"
        html_table += "<td>" + str(index) + "</td>"  # Add row name
        html_table += "<td>" + "</td><td>".join(str(cell) for cell in row.values) + "</td>"
        html_table += "</tr>"
    html_table += "</table>"
    row_series = filtered_df.loc[input_text]
    row_series_sorted = row_series.sort_values(ascending=False)
    row_df = row_series_sorted.to_frame().T   
    row_html = row_df.to_html(index=True)
    return col, val,row_html, html_table

# Create input widget
text_input = TextInput(placeholder="Type Population name")

# Create button widget
button = Button(label="Search")

# Create Div to display DataFrame as HTML table
paragraph = Div()

# Loading message
loading_message = Div(text="Loading...", visible=False)

options = [str(i) for i in range(1, 23)]  # Convert numbers to strings
options2 = ["Full Genome", "By Chromosome"]
dropdown1 = Select(title="Select format:", value=options2[0], options=options2)

dropdown = Select(title="Select chromosome number:", value=options[0], options=options)


# Define a callback function to handle changes in the dropdown
def dropdown_callback(attr, old, new):
    global selected_number
    selected_number = int(new)


# Attach the callback function to the 'value' property of the dropdown
dropdown.on_change('value', dropdown_callback)
dropdown.visible = False

# Define a callback function to handle changes in the dropdown
def dropdown_callback2(attr, old, new):
    global format
    if new == "By Chromosome":
        format = new
        dropdown.visible = True
    else:
        dropdown.visible = False




# Attach the callback function to the 'value' property of the dropdown
dropdown1.on_change('value', dropdown_callback2)

# Callback for button click
button.on_click(update_list)

added_components = [text_input, button, dropdown, loading_message, paragraph]


# Layout
interface1 = column(text_input, button, dropdown1, dropdown, loading_message, paragraph)

def ret_ov():
    return interface1
  
  