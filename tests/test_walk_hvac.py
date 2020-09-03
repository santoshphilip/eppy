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

e1 = [
    (("p_loop Supply Inlet", "epnode"), "Central_Chiller"),
    ("Central_Chiller", ("Central_Chiller_np1_node", "epnode")),
    (("Central_Chiller_np1_node", "epnode"), "np1"),
    ("np1", ("np1_np2_node", "epnode")),
    (("np1_np2_node", "epnode"), "np2"),
    ("np2", ("np2_Outlet_Node_Name", "epnode")),
    (("sb1_pipe_inlet", "epnode"), "sb1_pipe"),
    ("sb1_pipe", ("sb1_pipe_outlet", "epnode")),
    (("sb2_pipe_inlet", "epnode"), "sb2_pipe"),
    ("sb2_pipe", ("sb2_pipe_outlet", "epnode")),
    (("sb3_pipe_inlet", "epnode"), "sb3_pipe"),
    ("sb3_pipe", ("sb3_pipe_outlet", "epnode")),
    (("sb4_pipe_inlet", "epnode"), "sb4_pipe"),
    ("sb4_pipe", ("p_loop Supply Outlet", "epnode")),
    (("p_loop Demand Inlet", "epnode"), "db0_pipe"),
    ("db0_pipe", ("db0_pipe_outlet", "epnode")),
    (("db1_pipe_inlet", "epnode"), "db1_pipe"),
    ("db1_pipe", ("db1_pipe_outlet", "epnode")),
    (("db2_pipe_inlet", "epnode"), "db2_pipe"),
    ("db2_pipe", ("db2_pipe_outlet", "epnode")),
    (("db3_pipe_inlet", "epnode"), "db3_pipe"),
    ("db3_pipe", ("db3_pipe_outlet", "epnode")),
    (("db4_pipe_inlet", "epnode"), "db4_pipe"),
    ("db4_pipe", ("p_loop Demand Outlet", "epnode")),
    (("np2_Outlet_Node_Name", "epnode"), "p_loop_supply_splitter"),
    ("p_loop_supply_splitter", ("sb1_pipe_inlet", "epnode")),
    ("p_loop_supply_splitter", ("sb2_pipe_inlet", "epnode")),
    ("p_loop_supply_splitter", ("sb3_pipe_inlet", "epnode")),
    (("db0_pipe_outlet", "epnode"), "p_loop_demand_splitter"),
    ("p_loop_demand_splitter", ("db1_pipe_inlet", "epnode")),
    ("p_loop_demand_splitter", ("db2_pipe_inlet", "epnode")),
    ("p_loop_demand_splitter", ("db3_pipe_inlet", "epnode")),
    ("p_loop_supply_mixer", ("sb4_pipe_inlet", "epnode")),
    (("sb1_pipe_outlet", "epnode"), "p_loop_supply_mixer"),
    (("sb2_pipe_outlet", "epnode"), "p_loop_supply_mixer"),
    (("sb3_pipe_outlet", "epnode"), "p_loop_supply_mixer"),
    ("p_loop_demand_mixer", ("db4_pipe_inlet", "epnode")),
    (("db1_pipe_outlet", "epnode"), "p_loop_demand_mixer"),
    (("db2_pipe_outlet", "epnode"), "p_loop_demand_mixer"),
    (("db3_pipe_outlet", "epnode"), "p_loop_demand_mixer"),
]

e2 = (
    (("VAV Sys 1 Inlet Node", "epnode"), "Return Fan 1"),
    ("Return Fan 1", ("Return Fan 1 Outlet Node", "epnode")),
    (("Return Fan 1 Outlet Node", "epnode"), "OA Sys 1"),
    ("OA Sys 1", ("Mixed Air Node 1", "epnode")),
    (("Mixed Air Node 1", "epnode"), "Main Cooling Coil 1"),
    ("Main Cooling Coil 1", ("Main Cooling Coil 1 Outlet Node", "epnode")),
    (("Main Cooling Coil 1 Outlet Node", "epnode"), "Main Heating Coil 1"),
    ("Main Heating Coil 1", ("Main Heating Coil 1 Outlet Node", "epnode")),
    (("Main Heating Coil 1 Outlet Node", "epnode"), "Supply Fan 1"),
    ("Supply Fan 1", ("VAV Sys 1 Outlet Node", "epnode")),
    (("HW Supply Inlet Node", "epnode"), "HW Circ Pump"),
    ("HW Circ Pump", ("HW Pump Outlet Node", "epnode")),
    (("Central Boiler Inlet Node", "epnode"), "Central Boiler"),
    ("Central Boiler", ("Central Boiler Outlet Node", "epnode")),
    (("Heating Supply Bypass Inlet Node", "epnode"), "Heating Supply Side Bypass"),
    ("Heating Supply Side Bypass", ("Heating Supply Bypass Outlet Node", "epnode")),
    (("Heating Supply Exit Pipe Inlet Node", "epnode"), "Heating Supply Outlet"),
    ("Heating Supply Outlet", ("HW Supply Outlet Node", "epnode")),
    (("HW Demand Inlet Node", "epnode"), "Heating Demand Inlet Pipe"),
    ("Heating Demand Inlet Pipe", ("HW Demand Entrance Pipe Outlet Node", "epnode")),
    (("HW Demand Exit Pipe Inlet Node", "epnode"), "Heating Demand Outlet Pipe"),
    ("Heating Demand Outlet Pipe", ("HW Demand Outlet Node", "epnode")),
    (("SPACE1-1 Zone Coil Water In Node", "epnode"), "SPACE1-1 Zone Coil"),
    ("SPACE1-1 Zone Coil", ("SPACE1-1 Zone Coil Water Out Node", "epnode")),
    (("SPACE2-1 Zone Coil Water In Node", "epnode"), "SPACE2-1 Zone Coil"),
    ("SPACE2-1 Zone Coil", ("SPACE2-1 Zone Coil Water Out Node", "epnode")),
    (("SPACE3-1 Zone Coil Water In Node", "epnode"), "SPACE3-1 Zone Coil"),
    ("SPACE3-1 Zone Coil", ("SPACE3-1 Zone Coil Water Out Node", "epnode")),
    (("SPACE4-1 Zone Coil Water In Node", "epnode"), "SPACE4-1 Zone Coil"),
    ("SPACE4-1 Zone Coil", ("SPACE4-1 Zone Coil Water Out Node", "epnode")),
    (("SPACE5-1 Zone Coil Water In Node", "epnode"), "SPACE5-1 Zone Coil"),
    ("SPACE5-1 Zone Coil", ("SPACE5-1 Zone Coil Water Out Node", "epnode")),
    (("Main Heating Coil 1 Water Inlet Node", "epnode"), "Main Heating Coil 1"),
    ("Main Heating Coil 1", ("Main Heating Coil 1 Water Outlet Node", "epnode")),
    (("Heating Demand Bypass Inlet Node", "epnode"), "Heating Demand Bypass"),
    ("Heating Demand Bypass", ("Heating Demand Bypass Outlet Node", "epnode")),
    (("CW Demand Inlet Node", "epnode"), "Cooling Demand Side Inlet Pipe"),
    (
        "Cooling Demand Side Inlet Pipe",
        ("CW Demand Entrance Pipe Outlet Node", "epnode"),
    ),
    (("Main Cooling Coil 1 Water Inlet Node", "epnode"), "Main Cooling Coil 1"),
    ("Main Cooling Coil 1", ("Main Cooling Coil 1 Water Outlet Node", "epnode")),
    (("CW Demand Bypass Inlet Node", "epnode"), "Cooling Demand Side Bypass"),
    ("Cooling Demand Side Bypass", ("CW Demand Bypass Outlet Node", "epnode")),
    (("CW Demand Exit Pipe Inlet Node", "epnode"), "CW Demand Side Outlet Pipe"),
    ("CW Demand Side Outlet Pipe", ("CW Demand Outlet Node", "epnode")),
    (("Supply Side Exit Pipe Inlet Node", "epnode"), "Supply Side Outlet Pipe"),
    ("Supply Side Outlet Pipe", ("CW Supply Outlet Node", "epnode")),
    (("CW Supply Inlet Node", "epnode"), "CW Circ Pump"),
    ("CW Circ Pump", ("CW Pump Outlet Node", "epnode")),
    (("Central Chiller Inlet Node", "epnode"), "Central Chiller"),
    ("Central Chiller", ("Central Chiller Outlet Node", "epnode")),
    (("CW Supply Bypass Inlet Node", "epnode"), "Supply Side Bypass"),
    ("Supply Side Bypass", ("CW Supply Bypass Outlet Node", "epnode")),
    (("Condenser Supply Inlet Node", "epnode"), "Cond Circ Pump"),
    ("Cond Circ Pump", ("Condenser Pump Outlet Node", "epnode")),
    (("Condenser Tower Inlet Node", "epnode"), "Central Tower"),
    ("Central Tower", ("Condenser Tower Outlet Node", "epnode")),
    (("Cond Supply Bypass Inlet Node", "epnode"), "Condenser Supply Side Bypass"),
    ("Condenser Supply Side Bypass", ("Cond Supply Bypass Outlet Node", "epnode")),
    (("Condenser Supply Exit Pipe Inlet Node", "epnode"), "Condenser Supply Outlet"),
    ("Condenser Supply Outlet", ("Condenser Supply Outlet Node", "epnode")),
    (("Condenser Demand Inlet Node", "epnode"), "Condenser Demand Inlet Pipe"),
    (
        "Condenser Demand Inlet Pipe",
        ("Condenser Demand Entrance Pipe Outlet Node", "epnode"),
    ),
    (("Central Chiller Condenser Inlet Node", "epnode"), "Central Chiller"),
    ("Central Chiller", ("Central Chiller Condenser Outlet Node", "epnode")),
    (("Cond Demand Bypass Inlet Node", "epnode"), "Condenser Demand Side Bypass"),
    ("Condenser Demand Side Bypass", ("Cond Demand Bypass Outlet Node", "epnode")),
    (
        ("Condenser Demand Exit Pipe Inlet Node", "epnode"),
        "Condenser Demand Outlet Pipe",
    ),
    ("Condenser Demand Outlet Pipe", ("Condenser Demand Outlet Node", "epnode")),
    (("HW Demand Entrance Pipe Outlet Node", "epnode"), "Heating Demand Splitter"),
    ("Heating Demand Splitter", ("SPACE1-1 Zone Coil Water In Node", "epnode")),
    ("Heating Demand Splitter", ("SPACE2-1 Zone Coil Water In Node", "epnode")),
    ("Heating Demand Splitter", ("SPACE3-1 Zone Coil Water In Node", "epnode")),
    ("Heating Demand Splitter", ("SPACE4-1 Zone Coil Water In Node", "epnode")),
    ("Heating Demand Splitter", ("SPACE5-1 Zone Coil Water In Node", "epnode")),
    ("Heating Demand Splitter", ("Main Heating Coil 1 Water Inlet Node", "epnode")),
    ("Heating Demand Splitter", ("Heating Demand Bypass Inlet Node", "epnode")),
    (("HW Pump Outlet Node", "epnode"), "Heating Supply Splitter"),
    ("Heating Supply Splitter", ("Central Boiler Inlet Node", "epnode")),
    ("Heating Supply Splitter", ("Heating Supply Bypass Inlet Node", "epnode")),
    (("CW Pump Outlet Node", "epnode"), "CW Loop Splitter"),
    ("CW Loop Splitter", ("Central Chiller Inlet Node", "epnode")),
    ("CW Loop Splitter", ("CW Supply Bypass Inlet Node", "epnode")),
    (("CW Demand Entrance Pipe Outlet Node", "epnode"), "CW Demand Splitter"),
    ("CW Demand Splitter", ("Main Cooling Coil 1 Water Inlet Node", "epnode")),
    ("CW Demand Splitter", ("CW Demand Bypass Inlet Node", "epnode")),
    (
        ("Condenser Demand Entrance Pipe Outlet Node", "epnode"),
        "Condenser Demand Splitter",
    ),
    ("Condenser Demand Splitter", ("Central Chiller Condenser Inlet Node", "epnode")),
    ("Condenser Demand Splitter", ("Cond Demand Bypass Inlet Node", "epnode")),
    (("Condenser Pump Outlet Node", "epnode"), "Condenser Supply Splitter"),
    ("Condenser Supply Splitter", ("Condenser Tower Inlet Node", "epnode")),
    ("Condenser Supply Splitter", ("Cond Supply Bypass Inlet Node", "epnode")),
    ("Heating Demand Mixer", ("HW Demand Exit Pipe Inlet Node", "epnode")),
    (("SPACE1-1 Zone Coil Water Out Node", "epnode"), "Heating Demand Mixer"),
    (("SPACE2-1 Zone Coil Water Out Node", "epnode"), "Heating Demand Mixer"),
    (("SPACE3-1 Zone Coil Water Out Node", "epnode"), "Heating Demand Mixer"),
    (("SPACE4-1 Zone Coil Water Out Node", "epnode"), "Heating Demand Mixer"),
    (("SPACE5-1 Zone Coil Water Out Node", "epnode"), "Heating Demand Mixer"),
    (("Main Heating Coil 1 Water Outlet Node", "epnode"), "Heating Demand Mixer"),
    (("Heating Demand Bypass Outlet Node", "epnode"), "Heating Demand Mixer"),
    ("Heating Supply Mixer", ("Heating Supply Exit Pipe Inlet Node", "epnode")),
    (("Central Boiler Outlet Node", "epnode"), "Heating Supply Mixer"),
    (("Heating Supply Bypass Outlet Node", "epnode"), "Heating Supply Mixer"),
    ("CW Loop Mixer", ("Supply Side Exit Pipe Inlet Node", "epnode")),
    (("Central Chiller Outlet Node", "epnode"), "CW Loop Mixer"),
    (("CW Supply Bypass Outlet Node", "epnode"), "CW Loop Mixer"),
    ("CW Demand Mixer", ("CW Demand Exit Pipe Inlet Node", "epnode")),
    (("Main Cooling Coil 1 Water Outlet Node", "epnode"), "CW Demand Mixer"),
    (("CW Demand Bypass Outlet Node", "epnode"), "CW Demand Mixer"),
    ("Condenser Demand Mixer", ("Condenser Demand Exit Pipe Inlet Node", "epnode")),
    (("Central Chiller Condenser Outlet Node", "epnode"), "Condenser Demand Mixer"),
    (("Cond Demand Bypass Outlet Node", "epnode"), "Condenser Demand Mixer"),
    ("Condenser Supply Mixer", ("Condenser Supply Exit Pipe Inlet Node", "epnode")),
    (("Condenser Tower Outlet Node", "epnode"), "Condenser Supply Mixer"),
    (("Cond Supply Bypass Outlet Node", "epnode"), "Condenser Supply Mixer"),
    (("Zone Eq In Node", "epnode"), "Zone Supply Air Splitter 1"),
    ("Zone Supply Air Splitter 1", ("SPACE1-1 ATU In Node", "epnode")),
    ("Zone Supply Air Splitter 1", ("SPACE2-1 ATU In Node", "epnode")),
    ("Zone Supply Air Splitter 1", ("SPACE3-1 ATU In Node", "epnode")),
    ("Zone Supply Air Splitter 1", ("SPACE4-1 ATU In Node", "epnode")),
    ("Zone Supply Air Splitter 1", ("SPACE5-1 ATU In Node", "epnode")),
    ("Return-Plenum-1", ("PLENUM-1 Out Node", "epnode")),
    (("SPACE1-1 Out Node", "epnode"), "Return-Plenum-1"),
    (("SPACE2-1 Out Node", "epnode"), "Return-Plenum-1"),
    (("SPACE3-1 Out Node", "epnode"), "Return-Plenum-1"),
    (("SPACE4-1 Out Node", "epnode"), "Return-Plenum-1"),
    (("SPACE5-1 Out Node", "epnode"), "Return-Plenum-1"),
    ("SPACE1-1", ("SPACE1-1 Out Node", "epnode")),
    ("SPACE2-1", ("SPACE2-1 Out Node", "epnode")),
    ("SPACE3-1", ("SPACE3-1 Out Node", "epnode")),
    ("SPACE4-1", ("SPACE4-1 Out Node", "epnode")),
    ("SPACE5-1", ("SPACE5-1 Out Node", "epnode")),
    ("SPACE1-1 ATU", "SPACE1-1"),
    ("SPACE2-1 ATU", "SPACE2-1"),
    ("SPACE3-1 ATU", "SPACE3-1"),
    ("SPACE4-1 ATU", "SPACE4-1"),
    ("SPACE5-1 ATU", "SPACE5-1"),
    ("SPACE1-1 VAV Reheat", "SPACE1-1 ATU"),
    ("SPACE2-1 VAV Reheat", "SPACE2-1 ATU"),
    ("SPACE3-1 VAV Reheat", "SPACE3-1 ATU"),
    ("SPACE4-1 VAV Reheat", "SPACE4-1 ATU"),
    ("SPACE5-1 VAV Reheat", "SPACE5-1 ATU"),
    (("SPACE1-1 ATU In Node", "epnode"), "SPACE1-1 VAV Reheat"),
    (("SPACE2-1 ATU In Node", "epnode"), "SPACE2-1 VAV Reheat"),
    (("SPACE3-1 ATU In Node", "epnode"), "SPACE3-1 VAV Reheat"),
    (("SPACE4-1 ATU In Node", "epnode"), "SPACE4-1 VAV Reheat"),
    (("SPACE5-1 ATU In Node", "epnode"), "SPACE5-1 VAV Reheat"),
)


def test_nextnode():
    """py.test for nextnode"""
    edges = e1
    nexts = [
        "Central_Chiller",
        "np1",
        "np2",
        "p_loop_supply_splitter",
        "sb1_pipe",
        "p_loop_supply_mixer",
        "sb4_pipe",
    ]

    c = "Central_Chiller"

    n = 0
    i = 0  # counter
    while n == 0:  # endless loop
        assert nexts[i] == c
        i += 1
        nextcs = walk_hvac.nextnode(edges, c)
        if len(nextcs) == 0:
            break
        c = nextcs[0]
    # test links that have no nodes - equipment in spaces
    edges = e2
    connections = (
        ("SPACE2-1 ATU", "SPACE2-1"),
        ("SPACE3-1 ATU", "SPACE3-1"),
        ("SPACE4-1 ATU", "SPACE4-1"),
        ("SPACE5-1 ATU", "SPACE5-1"),
        ("SPACE1-1 VAV Reheat", "SPACE1-1 ATU"),
        ("SPACE2-1 VAV Reheat", "SPACE2-1 ATU"),
        ("SPACE3-1 VAV Reheat", "SPACE3-1 ATU"),
        ("SPACE4-1 VAV Reheat", "SPACE4-1 ATU"),
        ("SPACE5-1 VAV Reheat", "SPACE5-1 ATU"),
    )
    for comp, nextcomp in connections:
        result = walk_hvac.nextnode(edges, comp)
        assert result == [nextcomp]


def test_prevnode():
    """py.test for prevnode"""
    edges = e1
    prevs = [
        "sb4_pipe",
        "p_loop_supply_mixer",
        "sb1_pipe",
        "p_loop_supply_splitter",
        "np2",
        "np1",
        "Central_Chiller",
    ]

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
    connections = (
        ("SPACE2-1 ATU", "SPACE2-1"),
        ("SPACE3-1 ATU", "SPACE3-1"),
        ("SPACE4-1 ATU", "SPACE4-1"),
        ("SPACE5-1 ATU", "SPACE5-1"),
        ("SPACE1-1 VAV Reheat", "SPACE1-1 ATU"),
        ("SPACE2-1 VAV Reheat", "SPACE2-1 ATU"),
        ("SPACE3-1 VAV Reheat", "SPACE3-1 ATU"),
        ("SPACE4-1 VAV Reheat", "SPACE4-1 ATU"),
        ("SPACE5-1 VAV Reheat", "SPACE5-1 ATU"),
    )
    for prevcomp, comp in connections:
        result = walk_hvac.prevnode(edges, comp)
        assert result == [prevcomp]
