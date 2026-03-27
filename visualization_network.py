"""
only the drivers


review a3 visual gaph and work with how to execute the visualiations
"""

import networkx as nx
from plotly.graph_objs import Scatter, Figure


def visualize_graph(graph: Graph,
                    layout: str = 'spring_layout') -> None:
    graph_nx = graph.to_networkx()

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
