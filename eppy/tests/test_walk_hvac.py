"""py.test for walk_hvac.py"""

# Copyright (c) 2016 Santosh Philip
# =======================================================================
#  Distributed under the MIT License.
#  (See accompanying file LICENSE or copy at
#  http://opensource.org/licenses/MIT)
# =======================================================================
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from eppy import walk_hvac

e1 = [(('p_loop Supply Inlet', 'epnode'), 'Central_Chiller'), ('Central_Chiller', ('Central_Chiller_np1_node', 'epnode')), (('Central_Chiller_np1_node', 'epnode'), 'np1'), ('np1', ('np1_np2_node', 'epnode')), (('np1_np2_node', 'epnode'), 'np2'), ('np2', ('np2_Outlet_Node_Name', 'epnode')), (('sb1_pipe_inlet', 'epnode'), 'sb1_pipe'), ('sb1_pipe', ('sb1_pipe_outlet', 'epnode')), (('sb2_pipe_inlet', 'epnode'), 'sb2_pipe'), ('sb2_pipe', ('sb2_pipe_outlet', 'epnode')), (('sb3_pipe_inlet', 'epnode'), 'sb3_pipe'), ('sb3_pipe', ('sb3_pipe_outlet', 'epnode')), (('sb4_pipe_inlet', 'epnode'), 'sb4_pipe'), ('sb4_pipe', ('p_loop Supply Outlet', 'epnode')), (('p_loop Demand Inlet', 'epnode'), 'db0_pipe'), ('db0_pipe', ('db0_pipe_outlet', 'epnode')), (('db1_pipe_inlet', 'epnode'), 'db1_pipe'), ('db1_pipe', ('db1_pipe_outlet', 'epnode')), (('db2_pipe_inlet', 'epnode'), 'db2_pipe'), ('db2_pipe', ('db2_pipe_outlet', 'epnode')), (('db3_pipe_inlet', 'epnode'), 'db3_pipe'), ('db3_pipe', ('db3_pipe_outlet', 'epnode')), (('db4_pipe_inlet', 'epnode'), 'db4_pipe'), ('db4_pipe', ('p_loop Demand Outlet', 'epnode')), (('np2_Outlet_Node_Name', 'epnode'), 'p_loop_supply_splitter'), ('p_loop_supply_splitter', ('sb1_pipe_inlet', 'epnode')), ('p_loop_supply_splitter', ('sb2_pipe_inlet', 'epnode')), ('p_loop_supply_splitter', ('sb3_pipe_inlet', 'epnode')), (('db0_pipe_outlet', 'epnode'), 'p_loop_demand_splitter'), ('p_loop_demand_splitter', ('db1_pipe_inlet', 'epnode')), ('p_loop_demand_splitter', ('db2_pipe_inlet', 'epnode')), ('p_loop_demand_splitter', ('db3_pipe_inlet', 'epnode')), ('p_loop_supply_mixer', ('sb4_pipe_inlet', 'epnode')), (('sb1_pipe_outlet', 'epnode'), 'p_loop_supply_mixer'), (('sb2_pipe_outlet', 'epnode'), 'p_loop_supply_mixer'), (('sb3_pipe_outlet', 'epnode'), 'p_loop_supply_mixer'), ('p_loop_demand_mixer', ('db4_pipe_inlet', 'epnode')), (('db1_pipe_outlet', 'epnode'), 'p_loop_demand_mixer'), (('db2_pipe_outlet', 'epnode'), 'p_loop_demand_mixer'), (('db3_pipe_outlet', 'epnode'), 'p_loop_demand_mixer')]

e2 = (((u'VAV Sys 1 Inlet Node', 'epnode'), u'Return Fan 1'),
 (u'Return Fan 1', (u'Return Fan 1 Outlet Node', 'epnode')),
 ((u'Return Fan 1 Outlet Node', 'epnode'), u'OA Sys 1'),
 (u'OA Sys 1', (u'Mixed Air Node 1', 'epnode')),
 ((u'Mixed Air Node 1', 'epnode'), u'Main Cooling Coil 1'),
 (u'Main Cooling Coil 1', (u'Main Cooling Coil 1 Outlet Node', 'epnode')),
 ((u'Main Cooling Coil 1 Outlet Node', 'epnode'), u'Main Heating Coil 1'),
 (u'Main Heating Coil 1', (u'Main Heating Coil 1 Outlet Node', 'epnode')),
 ((u'Main Heating Coil 1 Outlet Node', 'epnode'), u'Supply Fan 1'),
 (u'Supply Fan 1', (u'VAV Sys 1 Outlet Node', 'epnode')),
 ((u'HW Supply Inlet Node', 'epnode'), u'HW Circ Pump'),
 (u'HW Circ Pump', (u'HW Pump Outlet Node', 'epnode')),
 ((u'Central Boiler Inlet Node', 'epnode'), u'Central Boiler'),
 (u'Central Boiler', (u'Central Boiler Outlet Node', 'epnode')),
 ((u'Heating Supply Bypass Inlet Node', 'epnode'),
  u'Heating Supply Side Bypass'),
 (u'Heating Supply Side Bypass',
  (u'Heating Supply Bypass Outlet Node', 'epnode')),
 ((u'Heating Supply Exit Pipe Inlet Node', 'epnode'),
  u'Heating Supply Outlet'),
 (u'Heating Supply Outlet', (u'HW Supply Outlet Node', 'epnode')),
 ((u'HW Demand Inlet Node', 'epnode'), u'Heating Demand Inlet Pipe'),
 (u'Heating Demand Inlet Pipe',
  (u'HW Demand Entrance Pipe Outlet Node', 'epnode')),
 ((u'HW Demand Exit Pipe Inlet Node', 'epnode'),
  u'Heating Demand Outlet Pipe'),
 (u'Heating Demand Outlet Pipe', (u'HW Demand Outlet Node', 'epnode')),
 ((u'SPACE1-1 Zone Coil Water In Node', 'epnode'), u'SPACE1-1 Zone Coil'),
 (u'SPACE1-1 Zone Coil', (u'SPACE1-1 Zone Coil Water Out Node', 'epnode')),
 ((u'SPACE2-1 Zone Coil Water In Node', 'epnode'), u'SPACE2-1 Zone Coil'),
 (u'SPACE2-1 Zone Coil', (u'SPACE2-1 Zone Coil Water Out Node', 'epnode')),
 ((u'SPACE3-1 Zone Coil Water In Node', 'epnode'), u'SPACE3-1 Zone Coil'),
 (u'SPACE3-1 Zone Coil', (u'SPACE3-1 Zone Coil Water Out Node', 'epnode')),
 ((u'SPACE4-1 Zone Coil Water In Node', 'epnode'), u'SPACE4-1 Zone Coil'),
 (u'SPACE4-1 Zone Coil', (u'SPACE4-1 Zone Coil Water Out Node', 'epnode')),
 ((u'SPACE5-1 Zone Coil Water In Node', 'epnode'), u'SPACE5-1 Zone Coil'),
 (u'SPACE5-1 Zone Coil', (u'SPACE5-1 Zone Coil Water Out Node', 'epnode')),
 ((u'Main Heating Coil 1 Water Inlet Node', 'epnode'), u'Main Heating Coil 1'),
 (u'Main Heating Coil 1',
  (u'Main Heating Coil 1 Water Outlet Node', 'epnode')),
 ((u'Heating Demand Bypass Inlet Node', 'epnode'), u'Heating Demand Bypass'),
 (u'Heating Demand Bypass', (u'Heating Demand Bypass Outlet Node', 'epnode')),
 ((u'CW Demand Inlet Node', 'epnode'), u'Cooling Demand Side Inlet Pipe'),
 (u'Cooling Demand Side Inlet Pipe',
  (u'CW Demand Entrance Pipe Outlet Node', 'epnode')),
 ((u'Main Cooling Coil 1 Water Inlet Node', 'epnode'), u'Main Cooling Coil 1'),
 (u'Main Cooling Coil 1',
  (u'Main Cooling Coil 1 Water Outlet Node', 'epnode')),
 ((u'CW Demand Bypass Inlet Node', 'epnode'), u'Cooling Demand Side Bypass'),
 (u'Cooling Demand Side Bypass', (u'CW Demand Bypass Outlet Node', 'epnode')),
 ((u'CW Demand Exit Pipe Inlet Node', 'epnode'),
  u'CW Demand Side Outlet Pipe'),
 (u'CW Demand Side Outlet Pipe', (u'CW Demand Outlet Node', 'epnode')),
 ((u'Supply Side Exit Pipe Inlet Node', 'epnode'), u'Supply Side Outlet Pipe'),
 (u'Supply Side Outlet Pipe', (u'CW Supply Outlet Node', 'epnode')),
 ((u'CW Supply Inlet Node', 'epnode'), u'CW Circ Pump'),
 (u'CW Circ Pump', (u'CW Pump Outlet Node', 'epnode')),
 ((u'Central Chiller Inlet Node', 'epnode'), u'Central Chiller'),
 (u'Central Chiller', (u'Central Chiller Outlet Node', 'epnode')),
 ((u'CW Supply Bypass Inlet Node', 'epnode'), u'Supply Side Bypass'),
 (u'Supply Side Bypass', (u'CW Supply Bypass Outlet Node', 'epnode')),
 ((u'Condenser Supply Inlet Node', 'epnode'), u'Cond Circ Pump'),
 (u'Cond Circ Pump', (u'Condenser Pump Outlet Node', 'epnode')),
 ((u'Condenser Tower Inlet Node', 'epnode'), u'Central Tower'),
 (u'Central Tower', (u'Condenser Tower Outlet Node', 'epnode')),
 ((u'Cond Supply Bypass Inlet Node', 'epnode'),
  u'Condenser Supply Side Bypass'),
 (u'Condenser Supply Side Bypass',
  (u'Cond Supply Bypass Outlet Node', 'epnode')),
 ((u'Condenser Supply Exit Pipe Inlet Node', 'epnode'),
  u'Condenser Supply Outlet'),
 (u'Condenser Supply Outlet', (u'Condenser Supply Outlet Node', 'epnode')),
 ((u'Condenser Demand Inlet Node', 'epnode'), u'Condenser Demand Inlet Pipe'),
 (u'Condenser Demand Inlet Pipe',
  (u'Condenser Demand Entrance Pipe Outlet Node', 'epnode')),
 ((u'Central Chiller Condenser Inlet Node', 'epnode'), u'Central Chiller'),
 (u'Central Chiller', (u'Central Chiller Condenser Outlet Node', 'epnode')),
 ((u'Cond Demand Bypass Inlet Node', 'epnode'),
  u'Condenser Demand Side Bypass'),
 (u'Condenser Demand Side Bypass',
  (u'Cond Demand Bypass Outlet Node', 'epnode')),
 ((u'Condenser Demand Exit Pipe Inlet Node', 'epnode'),
  u'Condenser Demand Outlet Pipe'),
 (u'Condenser Demand Outlet Pipe',
  (u'Condenser Demand Outlet Node', 'epnode')),
 ((u'HW Demand Entrance Pipe Outlet Node', 'epnode'),
  u'Heating Demand Splitter'),
 (u'Heating Demand Splitter', (u'SPACE1-1 Zone Coil Water In Node', 'epnode')),
 (u'Heating Demand Splitter', (u'SPACE2-1 Zone Coil Water In Node', 'epnode')),
 (u'Heating Demand Splitter', (u'SPACE3-1 Zone Coil Water In Node', 'epnode')),
 (u'Heating Demand Splitter', (u'SPACE4-1 Zone Coil Water In Node', 'epnode')),
 (u'Heating Demand Splitter', (u'SPACE5-1 Zone Coil Water In Node', 'epnode')),
 (u'Heating Demand Splitter',
  (u'Main Heating Coil 1 Water Inlet Node', 'epnode')),
 (u'Heating Demand Splitter', (u'Heating Demand Bypass Inlet Node', 'epnode')),
 ((u'HW Pump Outlet Node', 'epnode'), u'Heating Supply Splitter'),
 (u'Heating Supply Splitter', (u'Central Boiler Inlet Node', 'epnode')),
 (u'Heating Supply Splitter', (u'Heating Supply Bypass Inlet Node', 'epnode')),
 ((u'CW Pump Outlet Node', 'epnode'), u'CW Loop Splitter'),
 (u'CW Loop Splitter', (u'Central Chiller Inlet Node', 'epnode')),
 (u'CW Loop Splitter', (u'CW Supply Bypass Inlet Node', 'epnode')),
 ((u'CW Demand Entrance Pipe Outlet Node', 'epnode'), u'CW Demand Splitter'),
 (u'CW Demand Splitter', (u'Main Cooling Coil 1 Water Inlet Node', 'epnode')),
 (u'CW Demand Splitter', (u'CW Demand Bypass Inlet Node', 'epnode')),
 ((u'Condenser Demand Entrance Pipe Outlet Node', 'epnode'),
  u'Condenser Demand Splitter'),
 (u'Condenser Demand Splitter',
  (u'Central Chiller Condenser Inlet Node', 'epnode')),
 (u'Condenser Demand Splitter', (u'Cond Demand Bypass Inlet Node', 'epnode')),
 ((u'Condenser Pump Outlet Node', 'epnode'), u'Condenser Supply Splitter'),
 (u'Condenser Supply Splitter', (u'Condenser Tower Inlet Node', 'epnode')),
 (u'Condenser Supply Splitter', (u'Cond Supply Bypass Inlet Node', 'epnode')),
 (u'Heating Demand Mixer', (u'HW Demand Exit Pipe Inlet Node', 'epnode')),
 ((u'SPACE1-1 Zone Coil Water Out Node', 'epnode'), u'Heating Demand Mixer'),
 ((u'SPACE2-1 Zone Coil Water Out Node', 'epnode'), u'Heating Demand Mixer'),
 ((u'SPACE3-1 Zone Coil Water Out Node', 'epnode'), u'Heating Demand Mixer'),
 ((u'SPACE4-1 Zone Coil Water Out Node', 'epnode'), u'Heating Demand Mixer'),
 ((u'SPACE5-1 Zone Coil Water Out Node', 'epnode'), u'Heating Demand Mixer'),
 ((u'Main Heating Coil 1 Water Outlet Node', 'epnode'),
  u'Heating Demand Mixer'),
 ((u'Heating Demand Bypass Outlet Node', 'epnode'), u'Heating Demand Mixer'),
 (u'Heating Supply Mixer', (u'Heating Supply Exit Pipe Inlet Node', 'epnode')),
 ((u'Central Boiler Outlet Node', 'epnode'), u'Heating Supply Mixer'),
 ((u'Heating Supply Bypass Outlet Node', 'epnode'), u'Heating Supply Mixer'),
 (u'CW Loop Mixer', (u'Supply Side Exit Pipe Inlet Node', 'epnode')),
 ((u'Central Chiller Outlet Node', 'epnode'), u'CW Loop Mixer'),
 ((u'CW Supply Bypass Outlet Node', 'epnode'), u'CW Loop Mixer'),
 (u'CW Demand Mixer', (u'CW Demand Exit Pipe Inlet Node', 'epnode')),
 ((u'Main Cooling Coil 1 Water Outlet Node', 'epnode'), u'CW Demand Mixer'),
 ((u'CW Demand Bypass Outlet Node', 'epnode'), u'CW Demand Mixer'),
 (u'Condenser Demand Mixer',
  (u'Condenser Demand Exit Pipe Inlet Node', 'epnode')),
 ((u'Central Chiller Condenser Outlet Node', 'epnode'),
  u'Condenser Demand Mixer'),
 ((u'Cond Demand Bypass Outlet Node', 'epnode'), u'Condenser Demand Mixer'),
 (u'Condenser Supply Mixer',
  (u'Condenser Supply Exit Pipe Inlet Node', 'epnode')),
 ((u'Condenser Tower Outlet Node', 'epnode'), u'Condenser Supply Mixer'),
 ((u'Cond Supply Bypass Outlet Node', 'epnode'), u'Condenser Supply Mixer'),
 ((u'Zone Eq In Node', 'epnode'), u'Zone Supply Air Splitter 1'),
 (u'Zone Supply Air Splitter 1', (u'SPACE1-1 ATU In Node', 'epnode')),
 (u'Zone Supply Air Splitter 1', (u'SPACE2-1 ATU In Node', 'epnode')),
 (u'Zone Supply Air Splitter 1', (u'SPACE3-1 ATU In Node', 'epnode')),
 (u'Zone Supply Air Splitter 1', (u'SPACE4-1 ATU In Node', 'epnode')),
 (u'Zone Supply Air Splitter 1', (u'SPACE5-1 ATU In Node', 'epnode')),
 (u'Return-Plenum-1', (u'PLENUM-1 Out Node', 'epnode')),
 ((u'SPACE1-1 Out Node', 'epnode'), u'Return-Plenum-1'),
 ((u'SPACE2-1 Out Node', 'epnode'), u'Return-Plenum-1'),
 ((u'SPACE3-1 Out Node', 'epnode'), u'Return-Plenum-1'),
 ((u'SPACE4-1 Out Node', 'epnode'), u'Return-Plenum-1'),
 ((u'SPACE5-1 Out Node', 'epnode'), u'Return-Plenum-1'),
 (u'SPACE1-1', (u'SPACE1-1 Out Node', 'epnode')),
 (u'SPACE2-1', (u'SPACE2-1 Out Node', 'epnode')),
 (u'SPACE3-1', (u'SPACE3-1 Out Node', 'epnode')),
 (u'SPACE4-1', (u'SPACE4-1 Out Node', 'epnode')),
 (u'SPACE5-1', (u'SPACE5-1 Out Node', 'epnode')),
 (u'SPACE1-1 ATU', u'SPACE1-1'),
 (u'SPACE2-1 ATU', u'SPACE2-1'),
 (u'SPACE3-1 ATU', u'SPACE3-1'),
 (u'SPACE4-1 ATU', u'SPACE4-1'),
 (u'SPACE5-1 ATU', u'SPACE5-1'),
 (u'SPACE1-1 VAV Reheat', u'SPACE1-1 ATU'),
 (u'SPACE2-1 VAV Reheat', u'SPACE2-1 ATU'),
 (u'SPACE3-1 VAV Reheat', u'SPACE3-1 ATU'),
 (u'SPACE4-1 VAV Reheat', u'SPACE4-1 ATU'),
 (u'SPACE5-1 VAV Reheat', u'SPACE5-1 ATU'),
 ((u'SPACE1-1 ATU In Node', 'epnode'), u'SPACE1-1 VAV Reheat'),
 ((u'SPACE2-1 ATU In Node', 'epnode'), u'SPACE2-1 VAV Reheat'),
 ((u'SPACE3-1 ATU In Node', 'epnode'), u'SPACE3-1 VAV Reheat'),
 ((u'SPACE4-1 ATU In Node', 'epnode'), u'SPACE4-1 VAV Reheat'),
 ((u'SPACE5-1 ATU In Node', 'epnode'), u'SPACE5-1 VAV Reheat'))

def test_nextnode():
    """py.test for nextnode"""
    edges = e1
    nexts = ['Central_Chiller',
     'np1',
     'np2',
     'p_loop_supply_splitter',
     'sb1_pipe',
     'p_loop_supply_mixer',
     'sb4_pipe']

    c = 'Central_Chiller'

    n = 0
    i = 0 # counter
    while n == 0: # endless loop
        assert nexts[i] == c
        i += 1
        nextcs = walk_hvac.nextnode(edges, c)
        if len(nextcs) == 0:
            break
        c = nextcs[0]
    # test links that have no nodes - equipment in spaces
    edges = e2
    connections = ( (u'SPACE2-1 ATU', u'SPACE2-1'),
     (u'SPACE3-1 ATU', u'SPACE3-1'),
     (u'SPACE4-1 ATU', u'SPACE4-1'),
     (u'SPACE5-1 ATU', u'SPACE5-1'),
     (u'SPACE1-1 VAV Reheat', u'SPACE1-1 ATU'),
     (u'SPACE2-1 VAV Reheat', u'SPACE2-1 ATU'),
     (u'SPACE3-1 VAV Reheat', u'SPACE3-1 ATU'),
     (u'SPACE4-1 VAV Reheat', u'SPACE4-1 ATU'),
     (u'SPACE5-1 VAV Reheat', u'SPACE5-1 ATU'),
    )
    for comp, nextcomp in connections:
        result = walk_hvac.nextnode(edges, comp)
        assert result == [nextcomp]

def test_prevnode():
    """py.test for prevnode"""
    edges = e1
    prevs = ['sb4_pipe',
     'p_loop_supply_mixer',
     'sb1_pipe',
     'p_loop_supply_splitter',
     'np2',
     'np1',
     'Central_Chiller']

    c = "sb4_pipe"
    i = 0
    n = 0
    while n == 0:
        assert prevs[i] == c
        i += 1
        prevcs = walk_hvac.prevnode(edges, c)
        if len(prevcs) == 0:
            break
        c = prevcs[0]
    # test links that have no nodes - equipment in spaces
    edges = e2
    connections = ( (u'SPACE2-1 ATU', u'SPACE2-1'),
     (u'SPACE3-1 ATU', u'SPACE3-1'),
     (u'SPACE4-1 ATU', u'SPACE4-1'),
     (u'SPACE5-1 ATU', u'SPACE5-1'),
     (u'SPACE1-1 VAV Reheat', u'SPACE1-1 ATU'),
     (u'SPACE2-1 VAV Reheat', u'SPACE2-1 ATU'),
     (u'SPACE3-1 VAV Reheat', u'SPACE3-1 ATU'),
     (u'SPACE4-1 VAV Reheat', u'SPACE4-1 ATU'),
     (u'SPACE5-1 VAV Reheat', u'SPACE5-1 ATU'),
    )
    for prevcomp, comp in connections:
        result = walk_hvac.prevnode(edges, comp)
        assert result == [prevcomp]
        
