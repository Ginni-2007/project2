"""
CSC111 Project 2:- Beyond the Podium: A battle between F1’s greatest
========================================================

This module implements interactive bar chart visualizations using Bokeh to
display comparative performance metrics between two Formula 1 drivers. It loads
the graph data and generates a comprehensive visual comparison of statistics
including wins, podium finishes, finishing positions, and fastest laps.

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of students
taking CSC111 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for this project, please reach out to the group.

This file is Copyright (c) 2026 Huda Anum, Grishma Arun Kumar, Mehal Patel, Jolly Yan
"""
import load_data

from bokeh.models import ColumnDataSource, FactorRange
from bokeh.palettes import MediumContrast3
from bokeh.plotting import figure, show
from bokeh.transform import factor_cmap
from bokeh.models import HoverTool


def bar_chart(d1_id: str, d2_id: str):
    f1_graph = load_data.load_f1_data(
        "Dataset/drivers.csv",
        "Dataset/races.csv",
        "Dataset/results.csv"
    )
    id1, id2 = int(d1_id), int(d2_id)

    d1 = f1_graph._drivers.get(id1)
    d2 = f1_graph._drivers.get(id2)

    if not d1 or not d2:
        print(f"Error: One or both driver IDs ({d1_id}, {d2_id}) not found.")
        return

    stats_dict = f1_graph.compute_head_to_head(d1, d2)
    metrics = list(stats_dict.keys())
    driver_names = [d1.name, d2.name]

    y_values = []
    for m in metrics:
        y_values.extend(stats_dict[m])

    x = [(metric, name) for metric in metrics for name in driver_names]

    source = ColumnDataSource(data=dict(x=x, counts=y_values))

    p = figure(x_range=FactorRange(*x), height=500, width=1000, title="driver a vs driver b",
               toolbar_location=None, tools="", output_backend="svg")

    p.vbar(x='x', top='counts', width=0.9, source=source, line_color="white",
           fill_color=factor_cmap('x', palette=MediumContrast3, factors=driver_names, start=1, end=2))

    # y-axis
    p.y_range.start = 0
    p.y_range.end = 100
    p.yaxis.axis_label = "Percentage (%)"

    # x-axis labelling
    p.xaxis.major_label_orientation = 1.2
    p.xgrid.grid_line_color = None
    p.xaxis.group_text_font_size = "10pt"
    p.xaxis.group_text_font_style = "bold"
    p.min_border_bottom = 80

    # interactive hover tool
    hover = HoverTool(tooltips=[("Metric", "@x"), ("Value", "@counts{0.0}%")])
    p.add_tools(hover)

    p.title.text = "\nHead to head: " + d1.name + " vs. " + d2.name
    p.title.text_font_size = "14pt"
    p.title.align = "center"
    p.toolbar.logo = None
    p.toolbar_location = None

    show(p)


if __name__ == "__main__":
    # Example: 1 is Hamilton, 4 is Alonso
    bar_chart('1', '4')
