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

e = [(('p_loop Supply Inlet', 'epnode'), 'Central_Chiller'), ('Central_Chiller', ('Central_Chiller_np1_node', 'epnode')), (('Central_Chiller_np1_node', 'epnode'), 'np1'), ('np1', ('np1_np2_node', 'epnode')), (('np1_np2_node', 'epnode'), 'np2'), ('np2', ('np2_Outlet_Node_Name', 'epnode')), (('sb1_pipe_inlet', 'epnode'), 'sb1_pipe'), ('sb1_pipe', ('sb1_pipe_outlet', 'epnode')), (('sb2_pipe_inlet', 'epnode'), 'sb2_pipe'), ('sb2_pipe', ('sb2_pipe_outlet', 'epnode')), (('sb3_pipe_inlet', 'epnode'), 'sb3_pipe'), ('sb3_pipe', ('sb3_pipe_outlet', 'epnode')), (('sb4_pipe_inlet', 'epnode'), 'sb4_pipe'), ('sb4_pipe', ('p_loop Supply Outlet', 'epnode')), (('p_loop Demand Inlet', 'epnode'), 'db0_pipe'), ('db0_pipe', ('db0_pipe_outlet', 'epnode')), (('db1_pipe_inlet', 'epnode'), 'db1_pipe'), ('db1_pipe', ('db1_pipe_outlet', 'epnode')), (('db2_pipe_inlet', 'epnode'), 'db2_pipe'), ('db2_pipe', ('db2_pipe_outlet', 'epnode')), (('db3_pipe_inlet', 'epnode'), 'db3_pipe'), ('db3_pipe', ('db3_pipe_outlet', 'epnode')), (('db4_pipe_inlet', 'epnode'), 'db4_pipe'), ('db4_pipe', ('p_loop Demand Outlet', 'epnode')), (('np2_Outlet_Node_Name', 'epnode'), 'p_loop_supply_splitter'), ('p_loop_supply_splitter', ('sb1_pipe_inlet', 'epnode')), ('p_loop_supply_splitter', ('sb2_pipe_inlet', 'epnode')), ('p_loop_supply_splitter', ('sb3_pipe_inlet', 'epnode')), (('db0_pipe_outlet', 'epnode'), 'p_loop_demand_splitter'), ('p_loop_demand_splitter', ('db1_pipe_inlet', 'epnode')), ('p_loop_demand_splitter', ('db2_pipe_inlet', 'epnode')), ('p_loop_demand_splitter', ('db3_pipe_inlet', 'epnode')), ('p_loop_supply_mixer', ('sb4_pipe_inlet', 'epnode')), (('sb1_pipe_outlet', 'epnode'), 'p_loop_supply_mixer'), (('sb2_pipe_outlet', 'epnode'), 'p_loop_supply_mixer'), (('sb3_pipe_outlet', 'epnode'), 'p_loop_supply_mixer'), ('p_loop_demand_mixer', ('db4_pipe_inlet', 'epnode')), (('db1_pipe_outlet', 'epnode'), 'p_loop_demand_mixer'), (('db2_pipe_outlet', 'epnode'), 'p_loop_demand_mixer'), (('db3_pipe_outlet', 'epnode'), 'p_loop_demand_mixer')]



def next(edges, component):
    """get the next component in the loop"""
    e = edges
    c = component    
    n2c = [(a, b) for a, b in e if type(a) == tuple]
    c2nodes = [(a, b) for a, b in e if a == c]
    node2cs =[]
    for c2node in c2nodes:
        node2c = [(a, b) for a, b in n2c if a == c2node[-1]]
        if len(node2c) == 0:
            return []
        node2cs.append(node2c[0])
    cs = [b for a, b in node2cs]
    return cs
    
def prev(edges, component):
    """get the pervious component in the loop"""
    e = edges
    c = component
    n2c = [(a, b) for a, b in e if type(a) == tuple]
    c2n = [(a, b) for a, b in e if type(b) == tuple]
    node2cs = [(a, b) for a, b in e if b == c]
    c2nodes =[]
    for node2c in node2cs:
        c2node = [(a, b) for a, b in c2n if b == node2c[0]]
        if len(c2node) == 0:
            return []
        c2nodes.append(c2node[0]) 
    cs = [a for a, b in c2nodes]
    return cs

def main():
    edges = e
    # c = 'p_loop_supply_splitter'
    # print next(edges, component)   

    c = 'Central_Chiller'

    n = 0
    while n == 0:
        print c
        nextcs = next(e, c)
        if len(nextcs) == 0:
            break
        c = nextcs[0]
        # next(e, c)
    
    print '-'

    c = "sb4_pipe" 
    n = 0
    while n == 0:
        print c
        prevcs = prev(e, c)
        if len(prevcs) == 0:
            break
        c = prevcs[0]
        # next(e, c)

if __name__ == '__main__':
	main()

# TODO pytests