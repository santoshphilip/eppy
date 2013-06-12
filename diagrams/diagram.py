# Copyright (c) 2012 Santosh Philip

# This file is part of eppy.

# Eppy is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# Eppy is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with eppy.  If not, see <http://www.gnu.org/licenses/>.

"""routines to make the pydot diagrams"""
import pydot

def cleanedges(edges, replacechar=u'\xa6'):
    """replace the ':' in any nodes with unicode \xa6. """
    colon = ':'
    edges = list(edges) # in case it is a tuple
    for i, edge in enumerate(edges):
        edge = list(edge) # in ase it is a tuple
        for j, node in enumerate(edge):
            if type(node) == tuple:
                node = list(node)
                n1 = node[0]
                n1 = unicode(n1)
                if n1.find(colon) != -1:
                    n1 = n1.replace(colon, replacechar)
                n1 = node[0]
            else:
                node = unicode(node)
                if node.find(colon) != -1:
                    node = node.replace(colon, replacechar)
                edge[j] = node
        edges[i] = edge
    return edges
    
def makediagram(edges):
    """make the diagram with the edges"""
    graph = pydot.Dot(graph_type='digraph')
    nodes = edges2nodes(edges)
    epnodes = [(node, 
        makeanode(node[0])) for node in nodes if nodetype(node)=="epnode"]
    endnodes = [(node, 
        makeendnode(node[0])) for node in nodes if nodetype(node)=="EndNode"]
    epbr = [(node, makeabranch(node)) for node in nodes if not istuple(node)]
    nodedict = dict(epnodes + epbr + endnodes)
    for value in nodedict.values():
        graph.add_node(value)
    for e1, e2 in edges:
        graph.add_edge(pydot.Edge(nodedict[e1], nodedict[e2]))
    return graph

def edges2nodes(edges):
    """gather the nodes from the edges"""
    nodes = []
    for e1, e2 in edges:
        nodes.append(e1)
        nodes.append(e2)
    nodedict = dict([(n, None) for n in nodes])
    justnodes = nodedict.keys()
    justnodes.sort()
    return justnodes
    
def nodetype(anode):
    """return the type of node"""
    try:
        return anode[1]
    except IndexError, e:
        return None

def istuple(x):
    return type(x) == tuple

def makeabranch(name, encode=True):
    if encode:
        name = name.encode('UTF-8')
    return pydot.Node(name, shape="box3d", label=name)

def makeanode(name, encode=True):
    if encode:
        name = name.encode('UTF-8')
    return pydot.Node(name, shape="plaintext", label=name)
    
def makeendnode(name):
    return pydot.Node(name, shape="doubleoctagon", label=name, 
        style="filled", fillcolor="#e4e4e4")
    
    