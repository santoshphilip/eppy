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
from modeleditor import IDF
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
dloop = ['db0', ['zone1', 'zone2', 'zone3'], 'db4']
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

# make the branch lists for this condenser loop    
sbranchlist = idf.newidfobject("BRANCHLIST",
                newairloop[flnames[0]])
dbranchlist = idf.newidfobject("BRANCHLIST",
                newcondenserloop.Condenser_Demand_Side_Branch_List_Name)

# add branch names to the branchlist
sbranchnames = flattencopy(sloop)
# sbranchnames = sloop[1]
for branchname in sloop[1]:
    sbranchlist.obj.append(branchname)
dbranchnames = flattencopy(dloop)
# dbranchnames = dloop[1]
for branchname in dloop[1]:
    dbranchlist.obj.append(branchname)
# 
# # make a pipe branch for all branches in the loop
# 
# # supply side
# sbranchs = []
# for bname in sbranchnames:
#     branch = makepipebranch(idf, bname)
#     sbranchs.append(branch)
# # rename inlet outlet of endpoints of loop
# anode = "Component_1_Inlet_Node_Name"
# sameinnode = "Condenser_Side_Inlet_Node_Name" # TODO : change ?
# sbranchs[0][anode] =  newcondenserloop[sameinnode]
# anode = "Component_1_Outlet_Node_Name"
# sameoutnode = "Condenser_Side_Outlet_Node_Name" # TODO : change ?
# sbranchs[-1][anode] =  newcondenserloop[sameoutnode]
# # rename inlet outlet of endpoints of loop - rename in pipe
# pname = sbranchs[0]['Component_1_Name'] # get the pipe name
# apipe = idf.getobject('Pipe:Adiabatic'.upper(), pname) # get pipe
# apipe.Inlet_Node_Name = newcondenserloop[sameinnode]
# pname = sbranchs[-1]['Component_1_Name'] # get the pipe name
# apipe = idf.getobject('Pipe:Adiabatic'.upper(), pname) # get pipe
# apipe.Outlet_Node_Name = newcondenserloop[sameoutnode]
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
# # make the connectorlist an fill fields
# sconnlist = idf.newidfobject("CONNECTORLIST",
#                 newcondenserloop.Condenser_Side_Connector_List_Name)
# sconnlist.Connector_1_Object_Type = "Connector:Splitter"
# sconnlist.Connector_1_Name = "%s_supply_splitter" % (loopname, )
# sconnlist.Connector_2_Object_Type = "Connector:Mixer"
# sconnlist.Connector_2_Name = "%s_supply_mixer" % (loopname, )
# dconnlist = idf.newidfobject("CONNECTORLIST",
#     newcondenserloop.Condenser_Demand_Side_Connector_List_Name)
# dconnlist.Connector_1_Object_Type = "Connector:Splitter"
# dconnlist.Connector_1_Name = "%s_demand_splitter" % (loopname, )
# dconnlist.Connector_2_Object_Type = "Connector:Mixer"
# dconnlist.Connector_2_Name = "%s_demand_mixer" % (loopname, )
# 
# # make splitters and mixers
# s_splitter = idf.newidfobject("CONNECTOR:SPLITTER", 
#     sconnlist.Connector_1_Name)
# s_splitter.obj.extend([sloop[0]] + sloop[1])
# s_mixer = idf.newidfobject("CONNECTOR:MIXER", 
#     sconnlist.Connector_2_Name)
# s_mixer.obj.extend([sloop[-1]] + sloop[1])
# # -
# d_splitter = idf.newidfobject("CONNECTOR:SPLITTER", 
#     dconnlist.Connector_1_Name)
# d_splitter.obj.extend([dloop[0]] + dloop[1])
# d_mixer = idf.newidfobject("CONNECTOR:MIXER", 
#     dconnlist.Connector_2_Name)
# d_mixer.obj.extend([dloop[-1]] + dloop[1])
# return newcondenserloop
