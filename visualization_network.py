"""
CSC111 Project 2:- Beyond the Podium: A battle between F1’s greatest
=================================================================================================

This module provides functionality to visualize the network of driver
relationships using NetworkX and Plotly. It creates interactive graph
visualizations showing connections between drivers based on their shared race
history, enabling exploration of competition networks and driver clusters.

Copyright and Usage Information
=============================================================================================

This file is provided solely for the personal and private use of students
taking CSC111 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for this project, please reach out to the group!

This file is Copyright (c) 2026 Huda Anum, Grishma Arun Kumar, Mehal Patel, Jolly Yan
"""

import networkx as nx
from plotly.graph_objs import Scatter, Figure

import entities


def create_single_driver_graph(graph: entities.Graph, driver_name: str) -> nx.DiGraph:
    """Creates a NetworkX graph for a single driver"""
    network_graph = nx.DiGraph()
    racer = graph.get_driver(driver_name)

    network_graph.add_node(racer.name, codename=racer.codename)
    for driver in racer.neighbours:
        network_graph.add_node(driver.name, codename=driver.codename)
        network_graph.add_edge(driver.name, racer.name)

    return network_graph


def create_entire_graph(graph: entities.Graph) -> nx.Graph:
    """Creates a NetworkX graph visualizing the entire graph containing all the drivers"""
    network_graph = nx.Graph()
    racers = graph.get_list_of_drivers()

    for driver in racers:
        network_graph.add_node(driver.name, codename=driver.codename)

    for driver in racers:
        for driver_neighbour in driver.neighbours:
            if not network_graph.has_node(driver_neighbour.name):
                network_graph.add_node(driver_neighbour.name, codename=driver_neighbour.codename)

            network_graph.add_edge(driver.name, driver_neighbour.name)

    return network_graph


# Citation: Parts of Assignment 3, “a3_part2_recommendations.py”, were referenced for visualization_graph


def visualize_graph(graph_nx: nx.Graph | nx.DiGraph, layout: str = 'spring_layout') -> None:
    """Produces the visualization of the NetworkX graph"""
    pos = getattr(nx, layout)(graph_nx)

    x_values = [pos[k][0] for k in graph_nx.nodes]
    y_values = [pos[k][1] for k in graph_nx.nodes]
    full_name = list(graph_nx.nodes)

    code_name = [graph_nx.nodes[n].get('codename') for n in graph_nx.nodes]
    colours = ['rgb(0, 0, 0)' for _ in graph_nx.nodes]

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
                     line=dict(color='rgb(210,210,210)', width=1),
                     # to remove the extra information abt coordinates
                     # popping up on the graph
                     hoverinfo='none'
                     )

    # tracing the nodes
    trace4 = Scatter(x=x_values,
                     y=y_values,
                     mode='markers+text',
                     name='',
                     marker=dict(symbol='circle-dot',
                                 size=12,
                                 color=colours),
                     # to show that when you hover over the dots the name
                     # of the drivers appears
                     text=code_name,
                     textposition='top center',
                     customdata=full_name,
                     hovertemplate='<b>%{customdata}</b><extra></extra>')

    # to format all edges and nodes into one picture
    fig = Figure(data=[trace3, trace4])
    fig.update_layout(
        showlegend=False,
        hovermode='closest',
        margin=dict(b=0, l=0, r=0, t=0),  # Remove margins
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, visible=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, visible=False),
        plot_bgcolor='white'  # Set background to white for a cleaner look
    )
    fig.show()


if __name__ == '__main__':
    import doctest

    doctest.testmod()
