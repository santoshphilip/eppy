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

"""py.test for diagram.py"""

import diagram

def test_cleanedges():
    """py.test for cleanedges"""
    thedata = ( ( (('a:b', 'b'), ('a:b', 'c')), u'*',
        [[u'a*b', u'b'], [u'a*b', u'c']]), # edges, replacechar, newedges
        ( (('a:b', ('b', "epnode")), ('a:b', 'c')), u'*',
        [[u'a*b', ( u'b', u'epnode')], [u'a*b', u'c']]), 
        # edges, replacechar, newedges
    )
    for edges, replacechar, newedges in thedata:
        result = diagram.cleanedges(edges, replacechar='*')
        print result
        print newedges
        assert result == newedges
        
def test_edges2nodes():
    """py.test for edges2nodes"""
    thedata = (([("a", "b"), ("b", "c"), ("c", "d")],
    ["a", "b", "c", "d"]), # edges, nodes
    )
    for edges, nodes in thedata:
        result = diagram.edges2nodes(edges)   
        assert result == nodes
                
def test_encodenodes():
    """py.test for encodenodes"""
    thedata = (([u'a', u'b']),
    ([u'a'.encode('UTC-8'), u'b'.encode('UTC-8')])# nodes, newnodes
    )
