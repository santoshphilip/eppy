import pydot

# graph = pydot.Dot('graphname', graph_type='digraph') 
# subg = pydot.Subgraph('', rank='same') 
# subg.add_node(pydot.Node('a')) 
# graph.add_subgraph(subg) 
# subg.add_node(pydot.Node('b')) 
# subg.add_node(pydot.Node('c'))

# graph.write('a.png')


# edges = (("a", "b"), ("b", "c"), ("d", "a"), ("d", "b"))

a = u"a.`b"
a = chr(135)
a = u'Th\xe9r\xe8se Doe'
a = u'Th\xa6r\xe8se Doe'
# a = u'Th\x87r\xe8se Doe'
# a = u'Th\xa4r\xe8se Doe'
# http://www.alanwood.net/demos/ansi.html
# (a.encode('UTF-8')
edges = ((a.encode('UTF-8'), "b"), ("b", "c"), ("d", "a"), ("d", "b"))
g=pydot.graph_from_edges(edges, directed=True) 
g.write('a.dot')
g.write_png('a.png')