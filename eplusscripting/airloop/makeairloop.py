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


"""make an airloop"""
import copy
import sys
sys.path.append('../')
import modeleditor
from modeleditor import IDF
import hvacbuilder

class SomeFields(object):
    c_fields = ['Condenser Side Inlet Node Name',
    'Condenser Side Outlet Node Name',
    'Condenser Side Branch List Name',
    'Condenser Side Connector List Name',
    'Demand Side Inlet Node Name',
    'Demand Side Outlet Node Name',
    'Condenser Demand Side Branch List Name',
    'Condenser Demand Side Connector List Name']
    p_fields = ['Plant Side Inlet Node Name',
    'Plant Side Outlet Node Name',
    'Plant Side Branch List Name',
    'Plant Side Connector List Name',
    'Demand Side Inlet Node Name',
    'Demand Side Outlet Node Name',
    'Demand Side Branch List Name',
    'Demand Side Connector List Name']
    a_fields = ['Branch List Name',
    'Connector List Name',
    'Supply Side Inlet Node Name',
    'Demand Side Outlet Node Name',
    'Demand Side Inlet Node Names',
    'Supply Side Outlet Node Names']

def flattencopy(lst):
    """flatten and return a copy of the list
    indefficient on large lists"""
    # modified from http://stackoverflow.com/questions/2158395/flatten-an-irregular-list-of-lists-in-python
    TheList = copy.deepcopy(lst)
    listIsNested = True
    while listIsNested:                 #outer loop
        keepChecking = False
        Temp = []
        for element in TheList:         #inner loop
            if isinstance(element,list):
                Temp.extend(element)
                keepChecking = True
            else:
                Temp.append(element)
        listIsNested = keepChecking     #determine if outer loop exits
        TheList = Temp[:]
    return TheList
    

loopname = "a_loop"
sloop = ['sb0', ['sb1', 'sb2', 'sb3'], 'sb4']
# dloop = ['db0', ['zone1', 'zone2', 'zone3'], 'db4']
dloop = ['zone1', 'zone2', 'zone3']
# makeairloop(idf1, loopname, sloop, dloop)
# idf1.saveas("hh1.idf")

from StringIO import StringIO
import iddv7
IDF.setiddname(StringIO(iddv7.iddtxt))
idf = IDF(StringIO(''))

newairloop = idf.newidfobject("AirLoopHVAC".upper(), loopname)



fields = SomeFields.a_fields

# for use in bunch
flnames = [field.replace(' ', '_') for field in fields]

# TODO : check if these change too.
# simplify naming
a_fields = ['Branch List Name',
 'Connector List Name',
 'Supply Side Inlet Node Name',
 'Demand Side Outlet Node Name',
 'Demand Side Inlet Node Names',
 'Supply Side Outlet Node Names']
# changesnames to
# from
# ['Branch List Name',
#  'Connector List Name',
#  'Supply Side Inlet Node Name',
#  'Demand Side Outlet Node Name',
#  'Demand Side Inlet Node Names',
#  'Supply Side Outlet Node Names']
# to (airloop=a_loop)
# ['Branches',
#  'Connectors',
#  'Supply Inlet',
#  'Demand Outlet',
#  'Demand Inlet',
#  'Supply Outlet'] 
fields1 = ['Branches',
 'Connectors',
 'Supply Inlet',
 'Demand Outlet',
 'Demand Inlet',
 'Supply Outlet'] 

# old TODO : pop connectors if no parallel branches
# make fieldnames in the air loop
fieldnames = ['%s %s' % (loopname, field) for field in fields1]
for fieldname, thefield in zip(fieldnames, flnames):
    newairloop[thefield] = fieldname

# make the branch lists for this air loop    
sbranchlist = idf.newidfobject("BRANCHLIST",
                newairloop[flnames[0]])

# not needed in airloop                
# dbranchlist = idf.newidfobject("BRANCHLIST",
#                 newcondenserloop.Condenser_Demand_Side_Branch_List_Name)

# add branch names to the branchlist
sbranchnames = flattencopy(sloop)
# sbranchnames = sloop[1]
for branchname in sbranchnames:
    sbranchlist.obj.append(branchname)
# dbranchnames = flattencopy(dloop)
# # dbranchnames = dloop[1]
# for branchname in dloop[1]:
#     dbranchlist.obj.append(branchname)
# 
# # make a duct branch for all branches in the loop
# 
# supply side
sbranchs = []
for bname in sbranchnames:
    branch = hvacbuilder.makeductbranch(idf, bname)
    sbranchs.append(branch)
# rename inlet outlet of endpoints of loop
anode = "Component_1_Inlet_Node_Name"
sameinnode = "Supply_Side_Inlet_Node_Name" # TODO : change ?
sbranchs[0][anode] =  newairloop[sameinnode]
anode = "Component_1_Outlet_Node_Name"
sameoutnode = "Supply_Side_Outlet_Node_Names" # TODO : change ?
sbranchs[-1][anode] =  newairloop[sameoutnode]
# rename inlet outlet of endpoints of loop - rename in pipe
dname = sbranchs[0]['Component_1_Name'] # get the duct name
aduct = idf.getobject('duct'.upper(), dname) # get duct
aduct.Inlet_Node_Name = newairloop[sameinnode]
dname = sbranchs[-1]['Component_1_Name'] # get the duct name
aduct = idf.getobject('duct'.upper(), dname) # get duct
aduct.Outlet_Node_Name = newairloop[sameoutnode]
# 
# # demand side
# dbranchs = []
# for bname in dbranchnames:
#     branch = makepipebranch(idf, bname)
#     dbranchs.append(branch)
# # rename inlet outlet of endpoints of loop - rename in branch
# anode = "Component_1_Inlet_Node_Name"
# sameinnode = "Demand_Side_Inlet_Node_Name" # TODO : change ?
# dbranchs[0][anode] =  newcondenserloop[sameinnode]
# anode = "Component_1_Outlet_Node_Name"
# sameoutnode = "Demand_Side_Outlet_Node_Name" # TODO : change ?
# dbranchs[-1][anode] =  newcondenserloop[sameoutnode]
# # rename inlet outlet of endpoints of loop - rename in pipe
# pname = dbranchs[0]['Component_1_Name'] # get the pipe name
# apipe = idf.getobject('Pipe:Adiabatic'.upper(), pname) # get pipe
# apipe.Inlet_Node_Name = newcondenserloop[sameinnode]
# pname = dbranchs[-1]['Component_1_Name'] # get the pipe name
# apipe = idf.getobject('Pipe:Adiabatic'.upper(), pname) # get pipe
# apipe.Outlet_Node_Name = newcondenserloop[sameoutnode]
# 
# 
# # TODO : test if there are parallel branches
# make the connectorlist an fill fields
sconnlist = idf.newidfobject("CONNECTORLIST",
                newairloop.Connector_List_Name)
sconnlist.Connector_1_Object_Type = "Connector:Splitter"
sconnlist.Connector_1_Name = "%s_supply_splitter" % (loopname, )
sconnlist.Connector_2_Object_Type = "Connector:Mixer"
sconnlist.Connector_2_Name = "%s_supply_mixer" % (loopname, )
# dconnlist = idf.newidfobject("CONNECTORLIST",
#     newcondenserloop.Condenser_Demand_Side_Connector_List_Name)
# dconnlist.Connector_1_Object_Type = "Connector:Splitter"
# dconnlist.Connector_1_Name = "%s_demand_splitter" % (loopname, )
# dconnlist.Connector_2_Object_Type = "Connector:Mixer"
# dconnlist.Connector_2_Name = "%s_demand_mixer" % (loopname, )
# 
# make splitters and mixers
s_splitter = idf.newidfobject("CONNECTOR:SPLITTER", 
    sconnlist.Connector_1_Name)
s_splitter.obj.extend([sloop[0]] + sloop[1])
s_mixer = idf.newidfobject("CONNECTOR:MIXER", 
    sconnlist.Connector_2_Name)
s_mixer.obj.extend([sloop[-1]] + sloop[1])
# # -
# d_splitter = idf.newidfobject("CONNECTOR:SPLITTER", 
#     dconnlist.Connector_1_Name)
# d_splitter.obj.extend([dloop[0]] + dloop[1])
# d_mixer = idf.newidfobject("CONNECTOR:MIXER", 
#     dconnlist.Connector_2_Name)
# d_mixer.obj.extend([dloop[-1]] + dloop[1])
# return newcondenserloop

# demand side loop for airloop is made below 
#ZoneHVAC:EquipmentConnections
for zone in dloop:
    equipconn = idf.newidfobject("ZoneHVAC:EquipmentConnections".upper())
    equipconn.Zone_Name = zone
    fldname = "Zone_Conditioning_Equipment_List_Name"
    equipconn[fldname] = "%s equip list" % (zone, )
    fldname = "Zone_Air_Inlet_Node_or_NodeList_Name"
    equipconn[fldname] = "%s Inlet Node" % (zone, )
    fldname = "Zone_Air_Node_Name"
    equipconn[fldname] = "%s Node" % (zone, )
    fldname = "Zone_Return_Air_Node_Name"
    equipconn[fldname] = "%s Outlet Node" % (zone, )
    
# make ZoneHVAC:EquipmentList
for zone in dloop:
    z_equiplst = idf.newidfobject("ZoneHVAC:EquipmentList".upper())
    z_equipconn = modeleditor.getobjects(idf.idfobjects, 
        idf.model, idf.idd_info, 
        "ZoneHVAC:EquipmentConnections".upper(), #places=7,
        **dict(Zone_Name=zone))[0]
    z_equiplst.Name = z_equipconn.Zone_Conditioning_Equipment_List_Name
    fld = "Zone_Equipment_1_Object_Type"
    z_equiplst[fld] = "AirTerminal:SingleDuct:Uncontrolled"
    z_equiplst.Zone_Equipment_1_Name = "%sDirectAir" % (zone, )
    z_equiplst.Zone_Equipment_1_Cooling_Sequence = 1
    z_equiplst.Zone_Equipment_1_Heating_or_NoLoad_Sequence = 1
    
# make AirTerminal:SingleDuct:Uncontrolled
for zone in dloop:
    z_equipconn = modeleditor.getobjects(idf.idfobjects, 
        idf.model, idf.idd_info, 
        "ZoneHVAC:EquipmentConnections".upper(), #places=7,
        **dict(Zone_Name=zone))[0]
    key = "AirTerminal:SingleDuct:Uncontrolled".upper()
    z_airterm = idf.newidfobject(key)
    z_airterm.Name = "%sDirectAir" % (zone, )
    fld1 = "Zone_Supply_Air_Node_Name"
    fld2 = "Zone_Air_Inlet_Node_or_NodeList_Name"
    z_airterm[fld1] = z_equipconn[fld2]
    z_airterm.Maximum_Air_Flow_Rate = 'autosize'

# MAKE AirLoopHVAC:ZoneSplitter
# zone = dloop[0]
key = "AirLoopHVAC:ZoneSplitter".upper()
z_splitter = idf.newidfobject(key)
z_splitter.Name = "%s Demand Side Splitter" % (loopname, )
z_splitter.Inlet_Node_Name = newairloop.Demand_Side_Inlet_Node_Names
for i, zone in enumerate(dloop):
    z_equipconn = modeleditor.getobjects(idf.idfobjects, 
        idf.model, idf.idd_info, 
        "ZoneHVAC:EquipmentConnections".upper(), #places=7,
        **dict(Zone_Name=zone))[0]
    fld = "Outlet_%s_Node_Name" % (i + 1, )
    z_splitter[fld] = z_equipconn.Zone_Air_Inlet_Node_or_NodeList_Name

# make AirLoopHVAC:SupplyPath
key = "AirLoopHVAC:SupplyPath".upper()
z_supplypth = idf.newidfobject(key)
z_supplypth.Name = "%sSupplyPath" % (loopname, )
fld1 = "Supply_Air_Path_Inlet_Node_Name"
fld2 = "Demand_Side_Inlet_Node_Names"
z_supplypth[fld1] = newairloop[fld2]
z_supplypth.Component_1_Object_Type = "AirLoopHVAC:ZoneSplitter"
z_supplypth.Component_1_Name = z_splitter.Name

# make AirLoopHVAC:ZoneMixer
key = "AirLoopHVAC:ZoneMixer".upper()
z_mixer = idf.newidfobject(key)
z_mixer.Name = "%s Demand Side Mixer" % (loopname, )
z_mixer.Outlet_Node_Name = newairloop.Demand_Side_Outlet_Node_Name
for i, zone in enumerate(dloop):
    z_equipconn = modeleditor.getobjects(idf.idfobjects, 
        idf.model, idf.idd_info, 
        "ZoneHVAC:EquipmentConnections".upper(), #places=7,
        **dict(Zone_Name=zone))[0]
    fld = "Inlet_%s_Node_Name" % (i + 1, )
    z_mixer[fld] = z_equipconn.Zone_Return_Air_Node_Name

# make AirLoopHVAC:ReturnPath
key = "AirLoopHVAC:ReturnPath".upper()
z_returnpth = idf.newidfobject(key)
z_returnpth.Name = "%sReturnPath" % (loopname, )
z_returnpth.Return_Air_Path_Outlet_Node_Name = newairloop.Demand_Side_Outlet_Node_Name
z_returnpth.Component_1_Object_Type = "AirLoopHVAC:ZoneMixer"
z_returnpth.Component_1_Name = z_mixer.Name



idf.saveas('b.idf')