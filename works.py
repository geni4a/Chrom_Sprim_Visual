# # from bokeh.io import curdoc
# # from bokeh.layouts import row, column
# # from bokeh.models import Button, Div

# # # SVG code for a rectangle
# # rectangle_svg = """
# # <svg width="100" height="100">
# #   <rect width="100" height="100" style="fill:blue" />
# # </svg>
# # """

# # # SVG code for a circle
# # circle_svg = """
# # <svg width="100" height="100">
# #   <circle cx="50" cy="50" r="40" stroke="black" stroke-width="3" fill="red" />
# # </svg>
# # """

# # # Function to toggle layout to rectangle SVG
# # def toggle_rectangle():
# #     div.text = rectangle_svg

# # # Function to toggle layout to circle SVG
# # def toggle_circle():
# #     div.text = circle_svg

# # # Create buttons to toggle layouts
# # button_rectangle = Button(label="Rectangle")
# # button_rectangle.on_click(toggle_rectangle)

# # button_circle = Button(label="Circle")
# # button_circle.on_click(toggle_circle)

# # # Arrange buttons in a row layout
# # button_row = row(button_rectangle, button_circle)

# # # Create a Div widget with initial SVG content (rectangle)
# # div = Div(text=rectangle_svg, width=200, height=100)

# # # Arrange buttons and Div widget in a column layout
# # layout = column(button_row, div)

# # # Add the layout to the document
# # curdoc().add_root(layout)

# from bokeh.io import curdoc
# from bokeh.layouts import row, column
# from bokeh.models import Button, Div
# from bokeh.plotting import figure

# # Function to update plot with rectangle glyph
# def update_rectangle():
#     p.rect(x=1, y=1, width=1, height=1, fill_color="blue")

# # Function to update plot with circle glyph
# def update_circle():
#     p.circle([1], [1], size=50, color="red")

# # Function to clear plot
# def clear_plot():
#     p.renderers = []

# # Create a Bokeh plot
# p = figure(width=200, height=200, tools="", toolbar_location=None)

# # Create buttons to toggle plot glyphs
# button_rectangle = Button(label="Rectangle")
# button_rectangle.on_click(update_rectangle)

# button_circle = Button(label="Circle")
# button_circle.on_click(update_circle)

# button_clear = Button(label="Clear")
# button_clear.on_click(clear_plot)

# # Arrange buttons and plot in row and column layouts
# buttons_row = row(button_rectangle, button_circle, button_clear)
# layout = column(buttons_row, p)

# # Add the layout to the document
# curdoc().add_root(layout)

from bokeh.io import curdoc
from bokeh.layouts import row, column
from bokeh.models import Button
from bokeh.plotting import figure

# Create a Bokeh plot
p = figure(width=200, height=200, tools="", toolbar_location=None)

# Function to update plot with rectangle glyph
def update_rectangle():
    clear_plot()
    p.rect(x=1, y=1, width=1, height=1, fill_color="blue")

# Function to update plot with circle glyph
def update_circle():
    clear_plot()
    p.circle([1], [1], size=50, color="red")

# Function to clear plot
def clear_plot():
    p.renderers = []

# Create buttons to toggle plot glyphs
button_rectangle = Button(label="Rectangle")
button_rectangle.on_click(update_rectangle)

button_circle = Button(label="Circle")
button_circle.on_click(update_circle)

# Arrange buttons and plot in row and column layouts
buttons_row = row(button_rectangle, button_circle)
layout = column(buttons_row, p)

# Add the layout to the document
curdoc().add_root(layout)

