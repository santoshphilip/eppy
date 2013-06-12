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

"""py.test for s_entireplantloop"""

from StringIO import StringIO
import sys
sys.path.append('../EPlusInputcode')

import iddV6_0
from EPlusCode.EPlusInterfaceFunctions import readidf

# import eplus_functions
# import idd_fields


import s_entireplantloop

def test_makeentireplantloop():
    """py.test for makeentireplantloop"""
    thedata = (("""
    branchname0 -> splitter -> branchname1, branchname2, branchname3
    branchname1, branchname2, branchname3 -> mixer -> branchname4
    """,
    """
    dbranchname0 -> dsplitter -> dbranchname1, dbranchname2, dbranchname3
    dbranchname1, dbranchname2, dbranchname3 -> dmixer -> dbranchname4
    """,
    {'BRANCH': [['BRANCH', 'branchname0', '0', '', 'Pipe:Adiabatic', 'branchname0_pipe', 'plantloop_supply_inlet', 'branchname0_pipe_outlet', 'Bypass'], ['BRANCH', 'branchname1', '0', '', 'Pipe:Adiabatic', 'branchname1_pipe', 'branchname1_pipe_inlet', 'branchname1_pipe_outlet', 'Bypass'], ['BRANCH', 'branchname2', '0', '', 'Pipe:Adiabatic', 'branchname2_pipe', 'branchname2_pipe_inlet', 'branchname2_pipe_outlet', 'Bypass'], ['BRANCH', 'branchname3', '0', '', 'Pipe:Adiabatic', 'branchname3_pipe', 'branchname3_pipe_inlet', 'branchname3_pipe_outlet', 'Bypass'], ['BRANCH', 'branchname4', '0', '', 'Pipe:Adiabatic', 'branchname4_pipe', 'branchname4_pipe_inlet', 'plantloop_supply_outlet', 'Bypass'], ['BRANCH', 'dbranchname0', '0', '', 'Pipe:Adiabatic', 'dbranchname0_pipe', 'plantloop_demand_inlet', 'dbranchname0_pipe_outlet', 'Bypass'], ['BRANCH', 'dbranchname1', '0', '', 'Pipe:Adiabatic', 'dbranchname1_pipe', 'dbranchname1_pipe_inlet', 'dbranchname1_pipe_outlet', 'Bypass'], ['BRANCH', 'dbranchname2', '0', '', 'Pipe:Adiabatic', 'dbranchname2_pipe', 'dbranchname2_pipe_inlet', 'dbranchname2_pipe_outlet', 'Bypass'], ['BRANCH', 'dbranchname3', '0', '', 'Pipe:Adiabatic', 'dbranchname3_pipe', 'dbranchname3_pipe_inlet', 'dbranchname3_pipe_outlet', 'Bypass'], ['BRANCH', 'dbranchname4', '0', '', 'Pipe:Adiabatic', 'dbranchname4_pipe', 'dbranchname4_pipe_inlet', 'plantloop_demand_outlet', 'Bypass']], 'CONNECTORLIST': [['CONNECTORLIST', 'plantloop_supply_Clist', 'Connector:Splitter', 'splitter', 'Connector:Mixer', 'mixer'], ['CONNECTORLIST', 'plantloop_demand_Clist', 'Connector:Splitter', 'dsplitter', 'Connector:Mixer', 'dmixer']], 'CONNECTOR:MIXER': [['CONNECTOR:MIXER', 'mixer', 'branchname4', 'branchname1', 'branchname2', 'branchname3'], ['CONNECTOR:MIXER', 'dmixer', 'dbranchname4', 'dbranchname1', 'dbranchname2', 'dbranchname3']], 'PLANTLOOP': [['PLANTLOOP', 'plantloop', 'Water', '', '', '', '', '', '0.0', 'Autocalculate', 'plantloop_supply_inlet', 'plantloop_supply_outlet', 'plantloop_supply_Blist', 'plantloop_supply_Clist', 'plantloop_demand_inlet', 'plantloop_demand_outlet', 'plantloop_demand_Blist', 'plantloop_demand_Clist', 'Sequential', '', 'SingleSetpoint', 'None', 'None']], 'BRANCHLIST': [['BRANCHLIST', 'plantloop_supply_Blist', 'branchname1', 'branchname2', 'branchname3'], ['BRANCHLIST', 'plantloop_demand_Blist', 'dbranchname1', 'dbranchname2', 'dbranchname3']], 'CONNECTOR:SPLITTER': [['CONNECTOR:SPLITTER', 'splitter', 'branchname0', 'branchname1', 'branchname2', 'branchname3'], ['CONNECTOR:SPLITTER', 'dsplitter', 'dbranchname0', 'dbranchname1', 'dbranchname2', 'dbranchname3']]}), # supplystr, demandstr, loopdata
    )
    fname = StringIO("")
    data, commdct = readidf.readdatacommdct(fname, iddV6_0.theidd,
                                                        iddV6_0.commdct)    
    for supplystr, demandstr, loopdata in thedata:
        sloop = s_entireplantloop.HalfLoop(supplystr, "supply","plantloop")
        dloop = s_entireplantloop.HalfLoop(demandstr, "demand",'plantloop')
        # plantloop = loopdata[0]
        # branch = loopdata[1]
        s_entireplantloop.makeentireplantloop(data, commdct, sloop, dloop,
                                                                'plantloop')
        # objkey = 'plantloop'.upper()
        # rplantloop = data.dt[objkey]    
        akeys = [k for k in data.dt.keys() if len(data.dt[k]) > 0]
        result = {}
        for akey in akeys:
            result[akey] = data.dt[akey]
        assert result == loopdata                                   