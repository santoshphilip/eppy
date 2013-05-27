# Copyright (c) 2012 Santosh Phillip

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

"""make plant loop snippets"""
import sys
sys.path.append('../')
import copy

from modeleditor import IDF


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

def test_flattencopy():
    """py.test for flattencopy"""
    tdata = (([1,2], [1,2]), #lst , nlst
    ([1,2,[3,4]], [1,2,3,4]), #lst , nlst
    ([1,2,[3,[4,5,6],7,8]], [1,2,3,4,5,6,7,8]), #lst , nlst
    ([1,2,[3,[4,5,[6,7],8],9]], [1,2,3,4,5,6,7,8,9]), #lst , nlst
    )
    for lst , nlst in tdata:
        result = flattencopy(lst)
        assert result == nlst
        
def makepipecomponent(idf, pname):
    """todo"""
    apipe = idf.newidfobject("Pipe:Adiabatic".upper(), pname)
    apipe.Inlet_Node_Name = "%s_inlet" % (pname, )
    apipe.Outlet_Node_Name = "%s_outlet" % (pname, )
    return apipe
    
def makepipebranch(idf ,bname):
    """make a branch with a pipe
    use standard inlet outlet names"""
    # make the pipe component first
    pname = "%s_pipe" % (bname, )
    apipe = makepipecomponent(idf, pname)
    # now make the branch with the pipe in it
    abranch = idf.newidfobject("BRANCH", bname)    
    abranch.Component_1_Object_Type = 'Pipe:Adiabatic'
    abranch.Component_1_Name = pname
    abranch.Component_1_Inlet_Node_Name = apipe.Inlet_Node_Name
    abranch.Component_1_Outlet_Node_Name = apipe.Outlet_Node_Name
    abranch.Component_1_Branch_Control_Type = "Bypass"
    return abranch

def makeplantloop(idf, loopname, sloop, dloop):
    """make plant loop with pip components"""

    newplantloop = idf.newidfobject("PLANTLOOP", loopname)

    fields = ['Plant Side Inlet Node Name',
    'Plant Side Outlet Node Name',
    'Plant Side Branch List Name',
    'Plant Side Connector List Name',
    'Demand Side Inlet Node Name',
    'Demand Side Outlet Node Name',
    'Demand Side Branch List Name',
    'Demand Side Connector List Name']

    # for use in bunch
    flnames = [field.replace(' ', '_') for field in fields]

    # implify naming
    fields1 = [field.replace('Plant Side', 'Supply') for field in fields]
    fields1 = [field.replace('Demand Side', 'Demand') for field in fields1]
    fields1 = [field[:field.find('Name') - 1] for field in fields1]
    fields1 = [field.replace(' Node', '') for field in fields1]
    fields1 = [field.replace(' List', 's') for field in fields1]
    # changesnames to 
    # ['Supply Inlet',
    #  'Supply Outlet',
    #  'Supply Branchs',
    #  'Supply Connectors',
    #  'Demand Inlet',
    #  'Demand Outlet',
    #  'Demand Branchs',
    #  'Demand Connectors']

    # TODO : pop connectors if no parallel branches
    # make fieldnames in the plant loop
    fieldnames = ['%s %s' % (loopname, field) for field in fields1]
    for fieldname, thefield in zip(fieldnames, flnames):
        newplantloop[thefield] = fieldname
    
    # make the branch lists for this plant loop    
    sbranchlist = idf.newidfobject("BRANCHLIST",
                    newplantloop.Plant_Side_Branch_List_Name)
    dbranchlist = idf.newidfobject("BRANCHLIST",
                    newplantloop.Demand_Side_Branch_List_Name)

    # add branch names to the branchlist
    sbranchnames = flattencopy(sloop)
    # sbranchnames = sloop[1]
    for branchname in sloop[1]:
        sbranchlist.obj.append(branchname)
    dbranchnames = flattencopy(dloop)
    # dbranchnames = dloop[1]
    for branchname in dloop[1]:
        dbranchlist.obj.append(branchname)

    # make a pipe branch for all branches in the loop

    # supply side
    sbranchs = []
    for bname in sbranchnames:
        branch = makepipebranch(idf, bname)
        sbranchs.append(branch)
    # rename inlet outlet of endpoints of loop
    anode = "Component_1_Inlet_Node_Name"
    sameinnode = "Plant_Side_Inlet_Node_Name"
    sbranchs[0][anode] =  newplantloop[sameinnode]
    anode = "Component_1_Outlet_Node_Name"
    sameoutnode = "Plant_Side_Outlet_Node_Name"
    sbranchs[-1][anode] =  newplantloop[sameoutnode]
    # rename inlet outlet of endpoints of loop - rename in pipe
    pname = sbranchs[0]['Component_1_Name'] # get the pipe name
    apipe = idf.getobject('Pipe:Adiabatic'.upper(), pname) # get pipe
    apipe.Inlet_Node_Name = newplantloop[sameinnode]
    pname = sbranchs[-1]['Component_1_Name'] # get the pipe name
    apipe = idf.getobject('Pipe:Adiabatic'.upper(), pname) # get pipe
    apipe.Outlet_Node_Name = newplantloop[sameoutnode]

    # demand side
    dbranchs = []
    for bname in dbranchnames:
        branch = makepipebranch(idf, bname)
        dbranchs.append(branch)
    # rename inlet outlet of endpoints of loop - rename in branch
    anode = "Component_1_Inlet_Node_Name"
    sameinnode = "Demand_Side_Inlet_Node_Name"
    dbranchs[0][anode] =  newplantloop[sameinnode]
    anode = "Component_1_Outlet_Node_Name"
    sameoutnode = "Demand_Side_Outlet_Node_Name"
    dbranchs[-1][anode] =  newplantloop[sameoutnode]
    # rename inlet outlet of endpoints of loop - rename in pipe
    pname = dbranchs[0]['Component_1_Name'] # get the pipe name
    apipe = idf.getobject('Pipe:Adiabatic'.upper(), pname) # get pipe
    apipe.Inlet_Node_Name = newplantloop[sameinnode]
    pname = dbranchs[-1]['Component_1_Name'] # get the pipe name
    apipe = idf.getobject('Pipe:Adiabatic'.upper(), pname) # get pipe
    apipe.Outlet_Node_Name = newplantloop[sameoutnode]


    # TODO : test if there are parallel branches
    # make the connectorlist an fill fields
    sconnlist = idf.newidfobject("CONNECTORLIST",
                    newplantloop.Plant_Side_Connector_List_Name)
    sconnlist.Connector_1_Object_Type = "Connector:Splitter"
    sconnlist.Connector_1_Name = "%s_supply_splitter" % (loopname, )
    sconnlist.Connector_2_Object_Type = "Connector:Mixer"
    sconnlist.Connector_2_Name = "%s_supply_mixer" % (loopname, )
    dconnlist = idf.newidfobject("CONNECTORLIST",
                    newplantloop.Demand_Side_Connector_List_Name)
    dconnlist.Connector_1_Object_Type = "Connector:Splitter"
    dconnlist.Connector_1_Name = "%s_demand_splitter" % (loopname, )
    dconnlist.Connector_2_Object_Type = "Connector:Mixer"
    dconnlist.Connector_2_Name = "%s_demand_mixer" % (loopname, )

    # make splitters and mixers
    s_splitter = idf.newidfobject("CONNECTOR:SPLITTER", 
        sconnlist.Connector_1_Name)
    s_splitter.obj.extend([sloop[0]] + sloop[1])
    s_mixer = idf.newidfobject("CONNECTOR:MIXER", 
        sconnlist.Connector_2_Name)
    s_mixer.obj.extend([sloop[-1]] + sloop[1])
    # -
    d_splitter = idf.newidfobject("CONNECTOR:SPLITTER", 
        dconnlist.Connector_1_Name)
    d_splitter.obj.extend([dloop[0]] + dloop[1])
    d_mixer = idf.newidfobject("CONNECTOR:MIXER", 
        dconnlist.Connector_2_Name)
    d_mixer.obj.extend([dloop[-1]] + dloop[1])

# from StringIO import StringIO
# import iddv7
# IDF.setiddname(StringIO(iddv7.iddtxt))
# idf1 = IDF(StringIO(''))
# loopname = "p_loop"
# sloop = ['sb0', ['sb1', 'sb2', 'sb3'], 'sb4']
# dloop = ['db0', ['db1', 'db2', 'db3'], 'db4']
# makeplantloop(idf1, loopname, sloop, dloop)
# idf1.saveas("hh1.idf")
