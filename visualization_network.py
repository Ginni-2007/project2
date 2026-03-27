"""
only the drivers


review a3 visual gaph and work with how to execute the visualiations
"""

import networkx as nx
from plotly.graph_objs import Scatter, Figure

import entities
import load_data

def create_graph(graph: entities.Graph, driver_name: str) -> nx.Graph:

    g = nx.Graph()
    racer = graph.get_driver(driver_name)

    g.add_node(driver_name)
    for driver in racer.neighbours:
        g.add_node(driver.name)
        g.add_edge(driver.name, driver_name)

    return g


# original idea
# def create_graph(graph: entities.Graph) -> nx.Graph:
#
#     g = nx.Graph()
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
#             g.add_edge(driver.name, driver_neighbour.name)
#
#     return g

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


def visualize_graph(graph_nx: nx.Graph,
                    layout: str = 'spring_layout') -> None:
    # graph_nx = graph.to_networkx()

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




# TODO visualize graph clusters... (which groups do we want it to be)
# TODO GRAPH CLASS METHOD to_networkx()
