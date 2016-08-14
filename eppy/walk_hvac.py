# Copyright (c) 2012 Santosh Philip
# Copyright (c) 2016 Jamie Bull
# =======================================================================
#  Distributed under the MIT License.
#  (See accompanying file LICENSE or copy at
#  http://opensource.org/licenses/MIT)
# =======================================================================

def nextnode(edges, component):
    """Get the next component in the loop
    
    Parameters
    ----------
    edges : list
        List of tuples representing components in a plant or air loop.
    component : str
        A component in the loop.
    
    Returns
    -------
    str
    
    """
    e = edges
    c = component
    n2c = [(a, b) for a, b in e if type(a) == tuple]
    c2nodes = [(a, b) for a, b in e if a == c]
    node2cs = []
    for c2node in c2nodes:
        node2c = [(a, b) for a, b in n2c if a == c2node[-1]]
        if len(node2c) == 0:
            return []
        node2cs.append(node2c[0])
    cs = [b for a, b in node2cs]
    return cs


def prevnode(edges, component):
    """Get the previous component in the loop
    
    Parameters
    ----------
    edges : list
        List of tuples representing components in a plant or air loop.
    component : str
        A component in the loop.
    
    Returns
    -------
    str
    
    """
    e = edges
    c = component
    c2n = [(a, b) for a, b in e if type(b) == tuple]
    node2cs = [(a, b) for a, b in e if b == c]
    c2nodes = []
    for node2c in node2cs:
        c2node = [(a, b) for a, b in c2n if b == node2c[0]]
        if len(c2node) == 0:
            return []
        c2nodes.append(c2node[0])
    cs = [a for a, b in c2nodes]
    return cs
    