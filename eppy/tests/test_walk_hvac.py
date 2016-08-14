# Copyright (c) 2016 Jamie Bull
# =======================================================================
#  Distributed under the MIT License.
#  (See accompanying file LICENSE or copy at
#  http://opensource.org/licenses/MIT)
# =======================================================================
"""pytest for walk_hvac.py"""

from eppy.walk_hvac import nextnode
from eppy.walk_hvac import prevnode


def test_walk_hvac():
    e = [(('p_loop Supply Inlet', 'epnode'), 'Central_Chiller'), 
         ('Central_Chiller', ('Central_Chiller_np1_node', 'epnode')), 
         (('Central_Chiller_np1_node', 'epnode'), 'np1'), 
         ('np1', ('np1_np2_node', 'epnode')), 
         (('np1_np2_node', 'epnode'), 'np2'), 
         ('np2', ('np2_Outlet_Node_Name', 'epnode')), 
         (('sb1_pipe_inlet', 'epnode'), 'sb1_pipe'), 
         ('sb1_pipe', ('sb1_pipe_outlet', 'epnode')), 
         (('sb2_pipe_inlet', 'epnode'), 'sb2_pipe'), 
         ('sb2_pipe', ('sb2_pipe_outlet', 'epnode')), 
         (('sb3_pipe_inlet', 'epnode'), 'sb3_pipe'), 
         ('sb3_pipe', ('sb3_pipe_outlet', 'epnode')), 
         (('sb4_pipe_inlet', 'epnode'), 'sb4_pipe'), 
         ('sb4_pipe', ('p_loop Supply Outlet', 'epnode')), 
         (('p_loop Demand Inlet', 'epnode'), 'db0_pipe'), 
         ('db0_pipe', ('db0_pipe_outlet', 'epnode')), 
         (('db1_pipe_inlet', 'epnode'), 'db1_pipe'), 
         ('db1_pipe', ('db1_pipe_outlet', 'epnode')), 
         (('db2_pipe_inlet', 'epnode'), 'db2_pipe'), 
         ('db2_pipe', ('db2_pipe_outlet', 'epnode')), 
         (('db3_pipe_inlet', 'epnode'), 'db3_pipe'), 
         ('db3_pipe', ('db3_pipe_outlet', 'epnode')), 
         (('db4_pipe_inlet', 'epnode'), 'db4_pipe'), 
         ('db4_pipe', ('p_loop Demand Outlet', 'epnode')), 
         (('np2_Outlet_Node_Name', 'epnode'), 'p_loop_supply_splitter'), 
         ('p_loop_supply_splitter', ('sb1_pipe_inlet', 'epnode')), 
         ('p_loop_supply_splitter', ('sb2_pipe_inlet', 'epnode')), 
         ('p_loop_supply_splitter', ('sb3_pipe_inlet', 'epnode')), 
         (('db0_pipe_outlet', 'epnode'), 'p_loop_demand_splitter'), 
         ('p_loop_demand_splitter', ('db1_pipe_inlet', 'epnode')), 
         ('p_loop_demand_splitter', ('db2_pipe_inlet', 'epnode')), 
         ('p_loop_demand_splitter', ('db3_pipe_inlet', 'epnode')), 
         ('p_loop_supply_mixer', ('sb4_pipe_inlet', 'epnode')), 
         (('sb1_pipe_outlet', 'epnode'), 'p_loop_supply_mixer'), 
         (('sb2_pipe_outlet', 'epnode'), 'p_loop_supply_mixer'), 
         (('sb3_pipe_outlet', 'epnode'), 'p_loop_supply_mixer'), 
         ('p_loop_demand_mixer', ('db4_pipe_inlet', 'epnode')), 
         (('db1_pipe_outlet', 'epnode'), 'p_loop_demand_mixer'), 
         (('db2_pipe_outlet', 'epnode'), 'p_loop_demand_mixer'),
         (('db3_pipe_outlet', 'epnode'), 'p_loop_demand_mixer')]

    c = 'Central_Chiller'
    loop_forwards = []    
    while True:
        loop_forwards.append(c)
        nextcs = nextnode(e, c)
        if len(nextcs) == 0:
            break
        c = nextcs[0]
    expected = [
        'Central_Chiller', 'np1', 'np2', 
        'p_loop_supply_splitter', 'sb1_pipe', 
        'p_loop_supply_mixer', 'sb4_pipe']
    assert loop_forwards == expected

    c = "sb4_pipe"
    loop_backwards = []    
    while True:
        loop_backwards.append(c)
        prevcs = prevnode(e, c)
        if len(prevcs) == 0:
            break
        c = prevcs[0]
    expected.reverse()
    assert loop_backwards == expected
