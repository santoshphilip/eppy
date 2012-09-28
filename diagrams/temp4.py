# -*- coding: utf-8 -*-
"""
pydot example 2
@author: Federico Cáceres
@url: http://pythonhaven.wordpress.com/2009/12/09/generating_graphs_with_pydot
"""
import pydot

# this time, in graph_type we specify we want a DIrected GRAPH
graph = pydot.Dot(graph_type='digraph')

# in the last example, we did no explicitly create nodes, we just created the edges and
# they automatically placed nodes on the graph. Unfortunately, this way we cannot specify
# custom styles for the nodes (although you CAN set a default style for all objects on
# the graph...), so let's create the nodes manually.

# creating nodes is as simple as creating edges!
node_a = pydot.Node("Node A", style="filled", fillcolor="red")
# but... what are all those extra stuff after "Node A"?
# well, these arguments define how the node is going to look on the graph,
# you can find a full reference here:
# http://www.graphviz.org/doc/info/attrs.html
# which in turn is part of the full docs in
# http://www.graphviz.org/Documentation.php

# neat, huh? Let us create the rest of the nodes!
node_b = pydot.Node("Node B", style="filled", fillcolor="green")
node_c = pydot.Node("Node C", style="filled", fillcolor="#0000ff")
node_d = pydot.Node("Node D", style="filled", fillcolor="#976856")

#ok, now we add the nodes to the graph
graph.add_node(node_a)
graph.add_node(node_b)
graph.add_node(node_c)
graph.add_node(node_d)

# and finally we create the edges
# to keep it short, I'll be adding the edge automatically to the graph instead
# of keeping a reference to it in a variable
graph.add_edge(pydot.Edge(node_a, node_b))
graph.add_edge(pydot.Edge(node_b, node_c))
graph.add_edge(pydot.Edge(node_c, node_d))
# but, let's make this last edge special, yes?
graph.add_edge(pydot.Edge(node_d, node_a, label="and back we go again", labelfontcolor="#009933", fontsize="10.0", color="blue"))

# and we are done
graph.write_png('example2_graph.png')

# this is too good to be true!
