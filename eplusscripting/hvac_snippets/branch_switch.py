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


"""figure out how to switch branches in a loop."""

import sys
sys.path.append('../')
import copy

import modeleditor
import bunch_subclass
from modeleditor import IDF
import hvacbuilder

from StringIO import StringIO
import iddv7
IDF.setiddname(StringIO(iddv7.iddtxt))

def replacebranch(idf, loop, branch, listofcomponents, fluid=''):
    """It will replace the components in the branch with components in listofcomponents"""
    # join them into a branch
    # -----------------------
    # np1_inlet -> np1 -> np1_np2_node -> np2 -> np2_outlet
        # change the node names in the component
        # empty the old branch
        # fill in the new components with the node names into this branch

    # change the node names in the component so that they connect up. 
    # make the change as a list [oldnode, newnode]
    components = listofcomponents
    hvacbuilder.connectcomponents(idf, components, fluid=fluid)
    idf.saveas("hhh3.idf")

    # empty the old branch
    thebranchname = branch.Name
    thebranch = idf.removeextensibles('BRANCH', thebranchname) # empty the branch
    idf.saveas("hhh4.idf")

    # fill in the new components with the node names into this branch
        # find the first extensible field and fill in the data in obj.
    e_index = idf.getextensibleindex('BRANCH', thebranchname)
    theobj = thebranch.obj
    modeleditor.extendlist(theobj, e_index) # just being careful here
    for comp in components:
        theobj.append(comp.key)
        theobj.append(comp.Name)
        theobj.append(comp.Inlet_Node_Name)
        theobj.append(comp.Outlet_Node_Name)
        theobj.append('')
    idf.saveas("hhh5.idf")

    # # gather all renamed nodes
    # # do the renaming
    hvacbuilder.renamenodes(idf, 'node')
    idf.saveas("hhh7.idf")

    # check for the end nodes of the loop
    plantloop = loop
    supplyconlistname = plantloop.Plant_Side_Connector_List_Name
    supplyconlist = idf.getobject('CONNECTORLIST', supplyconlistname)
    for i in xrange(1, 100000): # large range to hit end
        try:
            fieldname = 'Connector_%s_Object_Type' % (i, )
            ctype = supplyconlist[fieldname]
        except bunch_subclass.BadEPFieldError, e:
            break
        if ctype.strip() == '':
            break
        fieldname = 'Connector_%s_Name' % (i, )
        cname = supplyconlist[fieldname]
        connector = idf.getobject(ctype.upper(), cname)
        if connector.key == 'CONNECTOR:SPLITTER':
            firstbranchname = connector.Inlet_Branch_Name
            cbranchname = firstbranchname
            isfirst = True
        if connector.key == 'CONNECTOR:MIXER':
            lastbranchname = connector.Outlet_Branch_Name
            cbranchname = lastbranchname
            isfirst = False
        # print i, cbranchname, thebranch.Name
        if cbranchname == thebranch.Name:
            # rename end nodes
            comps = hvacbuilder.getbranchcomponents(idf, thebranch)
            if isfirst:
                comp = comps[0]
                comp.Inlet_Node_Name = [comp.Inlet_Node_Name,
                                        plantloop.Plant_Side_Inlet_Node_Name]
            else:
                comp = comps[-1]
                # print comp
                comp.Outlet_Node_Name = [comp.Outlet_Node_Name, 
                                        plantloop.Plant_Side_Outlet_Node_Name]

    demandconlistname = plantloop.Demand_Side_Connector_List_Name
    demandconlist = idf.getobject('CONNECTORLIST', demandconlistname)
    for i in xrange(1, 100000): # large range to hit end
        try:
            fieldname = 'Connector_%s_Object_Type' % (i, )
            ctype = demandconlist[fieldname]
        except bunch_subclass.BadEPFieldError, e:
            break
        if ctype.strip() == '':
            break
        fieldname = 'Connector_%s_Name' % (i, )
        cname = demandconlist[fieldname]
        connector = idf.getobject(ctype.upper(), cname)
        if connector.key == 'CONNECTOR:SPLITTER':
            firstbranchname = connector.Inlet_Branch_Name
            cbranchname = firstbranchname
            isfirst = True
        if connector.key == 'CONNECTOR:MIXER':
            lastbranchname = connector.Outlet_Branch_Name 
            cbranchname = lastbranchname
            isfirst = False
        # print cbranchname, thebranch
        if cbranchname == thebranch.Name:
            # rename end nodes
            comps = hvacbuilder.getbranchcomponents(idf, thebranch)
            if isfirst:
                comp = comps[0]
                comp.Inlet_Node_Name = [comp.Inlet_Node_Name,
                                        plantloop.Demand_Side_Inlet_Node_Name]
            if not isfirst:
                comp = comps[-1]
                comp.Outlet_Node_Name = [comp.Outlet_Node_Name, 
                                    plantloop.Demand_Side_Outlet_Node_Name]


    idf.saveas("hhh8.idf")

    # # gather all renamed nodes
    # # do the renaming
    hvacbuilder.renamenodes(idf, 'node')
    idf.saveas("hhh9.idf")


idf = IDF(StringIO(''))
loopname = "p_loop"
sloop = ['sb0', ['sb1', 'sb2', 'sb3'], 'sb4']
dloop = ['db0', ['db1', 'db2', 'db3'], 'db4']
# sloop = ['sb0', ['sb1',], 'sb4']
# dloop = ['db0', ['db1',], 'db4']
hvacbuilder.makeplantloop(idf, loopname, sloop, dloop)
idf.saveas("hhh1.idf")

# replacebranch(loop, branch, listofcomponents)
# loop = loop of name p_loop
# branch = branch of name sb1

# make pipe components np1, np2
# pipe1 = hvacbuilder.makepipecomponent(idf, 'np1')
# pipe2 = hvacbuilder.makepipecomponent(idf, 'np2')
# idf.saveas("hhh2.idf")
pipe1 = idf.newidfobject("PIPE:ADIABATIC", 'np1')
chiller = idf.newidfobject("Chiller:Electric".upper(), 'Central_Chiller')
pipe2 = idf.newidfobject("PIPE:ADIABATIC", 'np2')
# pipe3 = idf.newidfobject("PIPE:ADIABATIC", 'np4')
# pipe4 = idf.newidfobject("PIPE:ADIABATIC", 'np4')
idf.saveas("hhh2.idf")

loop = idf.getobject('PLANTLOOP', 'p_loop')
branch = idf.getobject('BRANCH', 'sb0')
listofcomponents = [pipe1, chiller, pipe2]

replacebranch(idf, loop, branch, listofcomponents)
