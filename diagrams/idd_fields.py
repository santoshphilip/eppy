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

"""idd object field names used by EPlusInterface. 
Used to facilitate changes when E+ comes with new versions"""

class ObjectName(object):
    """holds the field description for the name of any object"""
    name = "Name"
    variablename = "Variable Name"
    uniqueobject = "unique-object"

class PlantLoop(object):
    """Holds the field descriptions of the E+ object"""
    plantinlet = "Plant Side Inlet Node Name"
    plantoutlet = "Plant Side Outlet Node Name"
    plantbranchlist = "Plant Side Branch List Name"
    plantconnectorlist = "Plant Side Connector List Name"
    demandinlet = "Demand Side Inlet Node Name"
    demandoutlet = "Demand Side Outlet Node Name"
    demandbranchlist = "Demand Side Branch List Name"
    demandconnectorlist = "Demand Side Connector List Name"
    
class BranchList(object):
    """holds the field descriptions of the E+ object BranchList"""
    firstbranch = "Branch 1 Name"
        
class ConnectorList(object):
    """holds the field descriptions of the E+ object ConnectorList"""
    connectortype1 = "Connector 1 Object Type"
    connector1= "Connector 1 Name"
    connectortype2 = "Connector 2 Object Type"
    connector2= "Connector 2 Name"
    # -
    splitter = "Connector:Splitter"
    mixer = "Connector:Mixer"
    
class Branch(object):
    """holds the field descriptions of the E+ object Branch"""
    name = "Name"
    componenttype1= "Component 1 Object Type"
    component1 = "Component 1 Name"
    inlet1 = "Component 1 Inlet Node Name"
    outlet1 = "Component 1 Outlet Node Name"
    controltype1 = "Component 1 Branch Control Type"
    # - 
    active = "Active"
    passive = "Passive"
    seriesactive = "SeriesActive"
    bypass = "Bypass"
    
class Connector_Splitter(object):
    """holds the field descriptions of the E+ object Connector_Splitter"""
    inlet = "Inlet Branch Name"
    firstoutlet = "Outlet Branch 1 Name"

class Connector_Mixer(object):
    """holds the field descriptions of the E+ object Connector_Mixer"""
    outlet = "Outlet Branch Name"
    firstinlet = "Inlet Branch 1 Name"