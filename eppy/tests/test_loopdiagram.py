# Copyright (c) 2012 Santosh Philip
# Copyright (c) 2016 Jamie Bull
# =======================================================================
#  Distributed under the MIT License.
#  (See accompanying file LICENSE or copy at
#  http://opensource.org/licenses/MIT)
# =======================================================================
"""py.test for loopdiagram.py
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from eppy.useful_scripts.loopdiagram import clean_edges
from eppy.useful_scripts.loopdiagram import dropnodes
from eppy.useful_scripts.loopdiagram import edges2nodes
from eppy.useful_scripts.loopdiagram import replace_colon


def test_replace_colon():
    """py.test for replace_colon"""
    data = (("zone:aap", '@', "zone@aap"),# s, r, replaced
    )    
    for s, r, replaced in data:
        result = replace_colon(s, r)
        assert result == replaced


def test_cleanedges():
    """py.test for cleanedges"""
    data = (([('a:a', 'a'), (('a', 'a'), 'a:a'), ('a:a', ('a', 'a'))],
    (('a__a', 'a'), (('a', 'a'), 'a__a'), ('a__a', ('a', 'a')))), 
    # edg, clean_edg
    )
    for edg, clean_edg in data:
        result = clean_edges(edg)
        assert result == clean_edg


def test_dropnodes():
    """py.test for dropnodes"""
    # test 1
    node = "node"
    (a,b,c,d,e,f,g,h,i) = (('a', node),'b',('c', node),'d',
        ('e', node),'f',('g', node),'h',('i', node))
    edges = [(a, b),
    (b, c),
    (c, d),
    (d, e),
    (e, f),
    (f, g),
    (g, h),
    (h, i),]
    theresult = [('a', 'b'), ('b', 'd'), ('d', 'f'), ('f', 'h'), ('h', 'i')]
    result = dropnodes(edges)
    assert result == theresult
    # test 2
    (a,b,c,d,e,f,g,h,i,j) = (('a', node),'b',('c', node),
        ('d', node),'e','f',('g', node),('h', node),'i',('j', node))
    edges = [(a, b),
    (b, c),
    (c, e),
    (e, g),
    (g, i),
    (i, j),
    (b, d),
    (d, f),
    (f, h),
    (h, i),]
    theresult = [('a', 'b'), ('b', 'e'), ('e', 'i'), ('i', 'j'), 
            ('b', 'f'), ('f', 'i')]
    result = dropnodes(edges)
    assert result == theresult

def test_edges2nodes():
    """py.test for edges2nodes"""
    thedata = (([("a", "b"), ("b", "c"), ("c", "d")],
    ["a", "b", "c", "d"]), # edges, nodes
    )
    for edges, nodes in thedata:
        result = edges2nodes(edges)   
        assert result == nodes
