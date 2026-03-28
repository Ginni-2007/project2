"""
CSC111 Project 2:- Beyond the Podium: A battle between F1’s greatest
========================================================

This module provides functionality to visualize the network of driver
relationships using NetworkX and Plotly. It creates interactive graph
visualizations showing connections between drivers based on their shared race
history, enabling exploration of competition networks and driver clusters.

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of students
taking CSC111 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for this project, please reach out to the group.

This file is Copyright (c) 2026 Huda Anum, Grishma Arun Kumar, Mehal Patel, Jolly Yan
"""

import networkx as nx
from plotly.graph_objs import Scatter, Figure

import entities
import load_data

def create_single_driver_graph(graph: entities.Graph, driver_name: str) -> nx.DiGraph:
    """Creates a single networkX graph"""
    g = nx.DiGraph()
    racer = graph.get_driver(driver_name)

    g.add_node(racer.name)
    for driver in racer.neighbours:
        g.add_node(driver.name)
        g.add_edge(driver.name, racer.name, weight=racer.neighbours[driver])

    return g

# def create_single_driver_graph(graph: entities.Graph, driver_name: str) -> nx.Graph:
#
#     g = nx.Graph()
#     racer = graph.get_driver(driver_name)
#
#     g.add_node(driver_name)
#     for driver in racer.neighbours:
#         g.add_node(driver.name)
#         g.add_edge(driver.name, driver_name)
#
#     return g


# original idea
def create_entire_graph(graph: entities.Graph) -> nx.Graph:

    g = nx.Graph()
    racers = graph.get_list_of_drivers()

    for driver in racers:
        g.add_node(driver.name)

    for driver in racers:
        for driver_neighbour in driver.neighbours:
            if not g.has_node(driver_neighbour.name):
                g.add_node(driver_neighbour.name)

            g.add_edge(driver.name, driver_neighbour.name)

    return g

    # g = nx.DiGraph()
    #     racers = graph.get_list_of_drivers()
    #
    #     for driver in racers:
    #         g.add_node(driver.name)
    #
    #     for driver in racers:
    #         for driver_neighbour in driver.neighbours:
    #             if not g.has_node(driver_neighbour.name):
    #                 g.add_node(driver_neighbour.name)
    #
    #             if not g.has_edge(driver.name, driver_neighbour.name) or not g.has_edge(driver_neighbour.name, driver.name):
    #                 if driver.neighbours[driver_neighbour] > driver_neighbour.neighbours[driver]:
    #                     g.add_edge(driver.name, driver_neighbour.name, weight=driver.neighbours[driver_neighbour])
    #                 else:
    #                     g.add_edge(driver.name, driver_neighbour.name, weight=driver_neighbour.neighbours[driver])
    #     return g


def visualize_graph(graph_nx: nx.Graph | nx.DiGraph, layout: str = 'spring_layout') -> None:

    pos = getattr(nx, layout)(graph_nx)

    x_values = [pos[k][0] for k in graph_nx.nodes]
    y_values = [pos[k][1] for k in graph_nx.nodes]
    labels = list(graph_nx.nodes)

    colours = ['rgb(255, 0, 0)' for node in graph_nx.nodes]

    x_edges = []
    y_edges = []
    for edge in graph_nx.edges:
        # none is there to prevent scribble (to lift the pen drawing the edges)
        x_edges += [pos[edge[0]][0], pos[edge[1]][0], None]
        y_edges += [pos[edge[0]][1], pos[edge[1]][1], None]

    # tracing the edges
    trace3 = Scatter(x=x_edges,
                     y=y_edges,
                     mode='lines',
                     # I set color to light gray for the edges but we
                     # can change it later
                     line=dict(color='rgb(210,210,210)', width=1),
                     # to remove the extra information abt coordinates
                     # popping up on the graph
                     hoverinfo='none'
                     )

    # tracing the nodes
    trace4 = Scatter(x=x_values,
                     y=y_values,
                     mode='markers',
                     marker=dict(symbol='circle-dot',
                                 size=5,
                                 color=colours),
                     # to show that when you hover over the dots the name
                     # of the drivers appears
                     text=labels,
                     hovertemplate='%{text}')

    # to format all edges and nodes into one picture
    fig = Figure(data=[trace3, trace4])
    fig.update_layout({'showlegend': False})
    fig.show()

