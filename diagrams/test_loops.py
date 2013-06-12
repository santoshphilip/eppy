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

"""py.test for loops.py"""
from StringIO import StringIO
import sys
sys.path.append('../EPlusInputcode')

import iddV6_0
from EPlusCode.EPlusInterfaceFunctions import readidf

import loops


def readidfsnippet(snippet, theidd, commdct):
    """read an idf snippet"""
    fname = StringIO(snippet)
    data, commdct = readidf.readdatacommdct(fname, theidd, commdct)
    return `data`
    

def test_readidfsnippet():
    """py.test for readidfsnippet"""
    data = (("""PlantLoop, Hot_Water_Loop_Hot_Water_Loop, Water,
     Hot_Water_Loop_Operation, Hot Water Loop HW Supply Outlet, 100, 10, 
     autosize, 0, autosize, Hot Water Loop HW Supply Inlet, 
     Hot Water Loop HW Supply Outlet, Hot_Water_Loop_HW_Supply_Side_Branches, 
     Hot_Water_Loop_HW_Supply_Side_Connectors, Hot Water Loop HW Demand Inlet, 
     Hot Water Loop HW Demand Outlet, Hot_Water_Loop_HW_Demand_Side_Branches, 
     Hot_Water_Loop_HW_Demand_Side_Connectors, Sequential, , SingleSetpoint;
      """, iddV6_0.theidd, iddV6_0.commdct,
      """PlantLoop,
     Hot_Water_Loop_Hot_Water_Loop,
     Water,
     Hot_Water_Loop_Operation,
     Hot Water Loop HW Supply Outlet,
     100,
     10,
     autosize,
     0,
     autosize,
     Hot Water Loop HW Supply Inlet,
     Hot Water Loop HW Supply Outlet,
     Hot_Water_Loop_HW_Supply_Side_Branches,
     Hot_Water_Loop_HW_Supply_Side_Connectors,
     Hot Water Loop HW Demand Inlet,
     Hot Water Loop HW Demand Outlet,
     Hot_Water_Loop_HW_Demand_Side_Branches,
     Hot_Water_Loop_HW_Demand_Side_Connectors,
     Sequential,
     ,
     SingleSetpoint;
"""), # snippet, theidd, commdct, cleanidf
    )
    for snippet, theidd, commdct, cleanidf in data:
        result = readidfsnippet(snippet, theidd, commdct)
        result = result.strip()
        cleanidf = cleanidf.strip()
        cleanidf = cleanidf.replace('\n', '\r\n')
        assert result == cleanidf

def test_extractfields():
    """py.test for extractfields"""
    thedata = (("""PlantLoop, Hot_Water_Loop_Hot_Water_Loop, Water,
     Hot_Water_Loop_Operation, Hot Water Loop HW Supply Outlet, 100, 10, 
     autosize, 0, autosize, Hot Water Loop HW Supply Inlet, 
     Hot Water Loop HW Supply Outlet, Hot_Water_Loop_HW_Supply_Side_Branches, 
     Hot_Water_Loop_HW_Supply_Side_Connectors, Hot Water Loop HW Demand Inlet, 
     Hot Water Loop HW Demand Outlet, Hot_Water_Loop_HW_Demand_Side_Branches, 
     Hot_Water_Loop_HW_Demand_Side_Connectors, Sequential, , SingleSetpoint;
     
     PlantLoop, Hot_Water_Loop_Hot_Water_Loop1, Water,
     Hot_Water_Loop_Operation, Hot Water Loop HW Supply Outlet, 100, 10, 
     autosize, 0, autosize, Hot Water Loop HW Supply Inlet, 
     Hot Water Loop HW Supply Outlet, Hot_Water_Loop_HW_Supply_Side_Branches, 
     Hot_Water_Loop_HW_Supply_Side_Connectors, Hot Water Loop HW Demand Inlet, 
     Hot Water Loop HW Demand Outlet, Hot_Water_Loop_HW_Demand_Side_Branches, 
     Hot_Water_Loop_HW_Demand_Side_Connectors, Sequential, , SingleSetpoint;
      """, 'plantloop'.upper(), [['Name',
       'Plant Side Inlet Node Name',
       'Plant Side Outlet Node Name',
       'Plant Side Branch List Name',
       'Demand Side Inlet Node Name',
       'Demand Side Outlet Node Name',
       'Demand Side Branch List Name',
      ]] * 2,
      [[ 1,
       'Plant Side Inlet Node Name',
       11,
       'Plant Side Branch List Name',
       'Demand Side Inlet Node Name',
       'Demand Side Outlet Node Name',
       'Demand Side Branch List Name',
      ]] * 2,
      [['Hot_Water_Loop_Hot_Water_Loop', 'Hot Water Loop HW Supply Inlet', 
      'Hot Water Loop HW Supply Outlet',
      'Hot_Water_Loop_HW_Supply_Side_Branches', 
      'Hot Water Loop HW Demand Inlet', 
      'Hot Water Loop HW Demand Outlet', 
      'Hot_Water_Loop_HW_Demand_Side_Branches'],
      ['Hot_Water_Loop_Hot_Water_Loop1', 'Hot Water Loop HW Supply Inlet', 
      'Hot Water Loop HW Supply Outlet',
      'Hot_Water_Loop_HW_Supply_Side_Branches', 
      'Hot Water Loop HW Demand Inlet', 
      'Hot Water Loop HW Demand Outlet', 
      'Hot_Water_Loop_HW_Demand_Side_Branches']]
      ),  # idftxt, objkey, fieldlist1, fieldlist2, fieldcontents
    )
    for idftxt, objkey, fieldlist1, fieldlist2, fieldcontents in thedata:
        fname = StringIO(idftxt)
        data, commdct = readidf.readdatacommdct(fname, iddV6_0.theidd,
                                                            iddV6_0.commdct)
        result = loops.extractfields(data, commdct, objkey, fieldlist1)
        assert result == fieldcontents
        # test with fieldlist2
        result = loops.extractfields(data, commdct, objkey, fieldlist2)
        assert result == fieldcontents
        # also test plantloopfields, since the test data is for plantloop
        result = loops.plantloopfields(data, commdct)
        assert result == fieldcontents

def test_branchlist2branches():
    """py.test branchlist2branches"""
    thedata = (("""BranchList,
        Hot_Water_Loop_HW_Supply_Side_Branches,  !- Name
        Hot_Water_Loop_HW_Supply_Inlet_Branch,  !- Branch 1 Name
        Main_Boiler_HW_Branch,   !- Branch 2 Name
        Hot_Water_Loop_HW_Supply_Bypass_Branch,  !- Branch 3 Name
        Hot_Water_Loop_HW_Supply_Outlet_Branch;  !- Branch 4 Name

    BranchList,
        Hot_Water_Loop_HW_Demand_Side_Branches,  !- Name
        Hot_Water_Loop_HW_Demand_Inlet_Branch,  !- Branch 1 Name
        SPACE1__1_Heating_Coil_HW_Branch,  !- Branch 2 Name
        SPACE2__1_Heating_Coil_HW_Branch,  !- Branch 3 Name
        SPACE3__1_Heating_Coil_HW_Branch,  !- Branch 4 Name
        SPACE4__1_Heating_Coil_HW_Branch,  !- Branch 5 Name
        SPACE5__1_Heating_Coil_HW_Branch,  !- Branch 6 Name
        Hot_Water_Loop_HW_Demand_Bypass_Branch,  !- Branch 7 Name
        Hot_Water_Loop_HW_Demand_Outlet_Branch;  !- Branch 8 Name
    """,'Hot_Water_Loop_HW_Supply_Side_Branches', 
    ['Hot_Water_Loop_HW_Supply_Inlet_Branch',
    'Main_Boiler_HW_Branch',
    'Hot_Water_Loop_HW_Supply_Bypass_Branch',
    'Hot_Water_Loop_HW_Supply_Outlet_Branch']), # idftxt, branchlist, branches
    )
    for idftxt, branchlist, branches in thedata:
        fname = StringIO(idftxt)
        data, commdct = readidf.readdatacommdct(fname, iddV6_0.theidd,
                                                            iddV6_0.commdct)
        result = loops.branchlist2branches(data, commdct, branchlist)
        assert result == branches

def test_branch_inlet_outlet():
    """py.test for branch_inlet_outlet"""
    thedata = (("""Branch,
        SPACE1__1_Cooling_Coil_ChW_Branch,  !- Name
        ,                        !- Maximum Flow Rate {m3/s}
        ,                        !- Pressure Drop Curve Name
        Coil:Cooling:Water,      !- Component 1 Object Type
        SPACE1__1_Cooling_Coil,  !- Component 1 Name
        SPACE1-1 Cooling Coil ChW Inlet,  !- Component 1 Inlet Node Name
        SPACE1-1 Cooling Coil ChW Outlet,  !- Component 1 Outlet Node Name
        Active;                  !- Component 1 Branch Control Type

        Branch,
          VAV WITH REHEAT Air Loop Main Branch,  !- Name
          AUTOSIZE,                !- Maximum Flow Rate {m3/s}
          ,                        !- Pressure Drop Curve Name
          AirLoopHVAC:OutdoorAirSystem,  !- Component 1 Object Type
          VAV WITH REHEAT_OA,      !- Component 1 Name
          VAV WITH REHEAT Supply Equipment Inlet Node,  !- Component 1 Inlet Node Name
          VAV WITH REHEAT_OA-VAV WITH REHEAT_CoolCNode,  !- Component 1 Outlet Node Name
          PASSIVE,                 !- Component 1 Branch Control Type
          Coil:Cooling:Water,      !- Component 2 Object Type
          VAV WITH REHEAT_CoolC,   !- Component 2 Name
          VAV WITH REHEAT_OA-VAV WITH REHEAT_CoolCNode,  !- Component 2 Inlet Node Name
          VAV WITH REHEAT_CoolC-VAV WITH REHEAT_HeatCNode,  !- Component 2 Outlet Node Name
          PASSIVE,                 !- Component 2 Branch Control Type
          Coil:Heating:Water,      !- Component 3 Object Type
          VAV WITH REHEAT_HeatC,   !- Component 3 Name
          VAV WITH REHEAT_CoolC-VAV WITH REHEAT_HeatCNode,  !- Component 3 Inlet Node Name
          VAV WITH REHEAT_HeatC-VAV WITH REHEAT FanNode,  !- Component 3 Outlet Node Name
          PASSIVE,                 !- Component 3 Branch Control Type
          Fan:VariableVolume,      !- Component 4 Object Type
          VAV WITH REHEAT Fan,     !- Component 4 Name
          VAV WITH REHEAT_HeatC-VAV WITH REHEAT FanNode,  !- Component 4 Inlet Node Name
          VAV WITH REHEAT Supply Equipment Outlet Node,  !- Component 4 Outlet Node Name
          ACTIVE;                  !- Component 4 Branch Control Type
""", 'VAV WITH REHEAT Air Loop Main Branch', 
    ['VAV WITH REHEAT Supply Equipment Inlet Node',
    'VAV WITH REHEAT Supply Equipment Outlet Node']), 
                # idftxt, branchname, inletoutlet
    )
    for idftxt, branchname, inletoutlet in thedata:
        fname = StringIO(idftxt)
        data, commdct = readidf.readdatacommdct(fname, iddV6_0.theidd,
                                                            iddV6_0.commdct)
        result = loops.branch_inlet_outlet(data, commdct, branchname)
        assert result == inletoutlet
        

def test_splittermixerfieldlists():
    """py.test for splittermixerfieldlists"""
    thedata = (("""Connector:Splitter,
         Hot_Water_Loop_HW_Supply_Splitter,
         Hot_Water_Loop_HW_Supply_Inlet_Branch,
         Hot_Water_Loop_HW_Supply_Bypass_Branch,
         Main_Boiler_HW_Branch;

    Connector:Splitter,
         Hot_Water_Loop_HW_Demand_Splitter,
         Hot_Water_Loop_HW_Demand_Inlet_Branch,
         SPACE1__1_Heating_Coil_HW_Branch,
         SPACE2__1_Heating_Coil_HW_Branch,
         SPACE3__1_Heating_Coil_HW_Branch,
         SPACE4__1_Heating_Coil_HW_Branch,
         SPACE5__1_Heating_Coil_HW_Branch,
         Hot_Water_Loop_HW_Demand_Bypass_Branch;
    """, 'Connector:Splitter',
    [[1,2,3,4],[1,2,3,4,5,6,7,8]]), # idftxt, objkey, fieldlists
    )    
    for idftxt, objkey, fieldlists in thedata:
        fname = StringIO(idftxt)
        data, commdct = readidf.readdatacommdct(fname, iddV6_0.theidd,
                                                            iddV6_0.commdct)
        result = loops.splittermixerfieldlists(data, commdct, objkey)
        assert result == fieldlists

def test_mixerfieldlists():
    """py.test for mixerfieldlists"""
    thedata = (("""Connector:Mixer,
         Hot_Water_Loop_HW_Supply_Mixer,
         Hot_Water_Loop_HW_Supply_Outlet_Branch,
         Hot_Water_Loop_HW_Supply_Bypass_Branch,
         Main_Boiler_HW_Branch;

    Connector:Mixer,
         Hot_Water_Loop_HW_Demand_Mixer,
         Hot_Water_Loop_HW_Demand_Outlet_Branch,
         SPACE1__1_Heating_Coil_HW_Branch,
         SPACE2__1_Heating_Coil_HW_Branch,
         SPACE3__1_Heating_Coil_HW_Branch,
         SPACE4__1_Heating_Coil_HW_Branch,
         SPACE5__1_Heating_Coil_HW_Branch,
         Hot_Water_Loop_HW_Demand_Bypass_Branch;
    """, [1,2,3,4], [1,2,3,4,5,6,7]), # idftxt, fieldlists
    )
    
def test_repeatingfields():
    """py.test for repeatingfields"""
    thedata = ((iddV6_0.theidd, iddV6_0.commdct, 'BRANCH', 
            "Component %s Name",
            ['Component 1 Name', 'Component 2 Name', 'Component 3 Name', 
            'Component 4 Name', 'Component 5 Name', 'Component 6 Name', 
            'Component 7 Name', 'Component 8 Name', 'Component 9 Name', 
            'Component 10 Name', 'Component 11 Name']
            ), #theidd, commdct, objkey, fld, thefields
    (iddV6_0.theidd, iddV6_0.commdct, 'BRANCH', 
    ["Component %s Object Type", "Component %s Name"],
    ['Component 1 Object Type', 'Component 1 Name', 
    'Component 2 Object Type', 'Component 2 Name', 
    'Component 3 Object Type', 'Component 3 Name', 
    'Component 4 Object Type', 'Component 4 Name', 
    'Component 5 Object Type', 'Component 5 Name', 
    'Component 6 Object Type', 'Component 6 Name', 
    'Component 7 Object Type', 'Component 7 Name', 
    'Component 8 Object Type', 'Component 8 Name', 
    'Component 9 Object Type', 'Component 9 Name', 
    'Component 10 Object Type', 'Component 10 Name', 
    'Component 11 Object Type', 'Component 11 Name']
    ), #theidd, commdct, objkey, fld, thefields
    (iddV6_0.theidd, iddV6_0.commdct, 'BRANCH', 
    [],
    []
    ), #theidd, commdct, objkey, fld, thefields
    )
    
    for theidd, commdct, objkey, fld, thefields in thedata:
        result = loops.repeatingfields(theidd, commdct, objkey, fld)
        print result
        print thefields
        print '=' *36
        assert result == thefields
    # test for multiple repeating fields
        
def test_objectcount():
    """py.test for objectcount"""
    thedata = (("""Output:Variable,*,
Time Heating Setpoint Not Met While Occupied,hourly;
Output:Variable,*,Time Cooling Setpoint Not Met While Occupied,hourly;
Output:Variable,*,VAV Terminal Damper Position,hourly;
Output:VariableDictionary,Regular;
Output:Surfaces:Drawing,dxf;
    """, "Output:Variable", 3), # idftxt, key, thecount
    )
    for idftxt, key, thecount in thedata:
        fname = StringIO(idftxt)
        data, commdct = readidf.readdatacommdct(fname, iddV6_0.theidd,
                                                            iddV6_0.commdct)
        result = loops.objectcount(data, key)
        assert result == thecount
        
def test_getfieldindex():
    """py.test for getfieldindex"""
    thedata = (( "AirTerminal:SingleDuct:VAV:Reheat".upper(), 
        "Air Inlet Node Name", 4),# objkey, fname, theindex
    )
    fname = StringIO("")
    data, commdct = readidf.readdatacommdct(fname, iddV6_0.theidd,
                                                        iddV6_0.commdct)
    for objkey, fname, theindex in thedata:
        result = loops.getfieldindex(data, commdct, objkey, fname)
        assert result == theindex

def test_makeadistu_inlets():
    """py.test for makeadistu_inlets"""
    adistuinlets = {'AirTerminal:SingleDuct:VAV:HeatAndCool:NoReheat': ['Air Inlet Node Name'], 'AirTerminal:DualDuct:VAV': ['Hot Air Inlet Node Name', 'Cold Air Inlet Node Name'], 'AirTerminal:SingleDuct:ParallelPIU:Reheat': ['Supply Air Inlet Node Name', 'Secondary Air Inlet Node Name', 'Reheat Coil Air Inlet Node Name'], 'AirTerminal:SingleDuct:VAV:Reheat:VariableSpeedFan': ['Air Inlet Node Name', 'Heating Coil Air Inlet Node Name'], 'AirTerminal:SingleDuct:VAV:Reheat': ['Air Inlet Node Name'], 'AirTerminal:SingleDuct:VAV:HeatAndCool:Reheat': ['Air Inlet Node Name'], 'AirTerminal:SingleDuct:VAV:NoReheat': ['Air Inlet Node Name'], 'AirTerminal:SingleDuct:ConstantVolume:Reheat': ['Air Inlet Node Name'], 'AirTerminal:SingleDuct:ConstantVolume:FourPipeInduction': ['Supply Air Inlet Node Name', 'Induced Air Inlet Node Name'], 'AirTerminal:SingleDuct:ConstantVolume:CooledBeam': ['Supply Air Inlet Node Name'], 'AirTerminal:SingleDuct:SeriesPIU:Reheat': ['Supply Air Inlet Node Name', 'Secondary Air Inlet Node Name', 'Reheat Coil Air Inlet Node Name'], 'AirTerminal:DualDuct:ConstantVolume': ['Hot Air Inlet Node Name', 'Cold Air Inlet Node Name']}
    fname = StringIO("")
    data, commdct = readidf.readdatacommdct(fname, iddV6_0.theidd,
                                                        iddV6_0.commdct)
    result = loops.makeadistu_inlets(data, commdct)
    assert result == adistuinlets