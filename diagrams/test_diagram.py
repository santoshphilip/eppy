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
