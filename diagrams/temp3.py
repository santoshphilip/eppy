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