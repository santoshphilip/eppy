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