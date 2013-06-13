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
from modeleditor import IDF
import hvacbuilder



def replacebranch(loop, branch, listofcomponents):
    """It will replace the components in the branch with components in listofcomponents"""
    pass
    
from StringIO import StringIO
import iddv7
IDF.setiddname(StringIO(iddv7.iddtxt))
idf = IDF(StringIO(''))
loopname = "p_loop"
sloop = ['sb0', ['sb1', 'sb2', 'sb3'], 'sb4']
dloop = ['db0', ['db1', 'db2', 'db3'], 'db4']
hvacbuilder.makeplantloop(idf, loopname, sloop, dloop)
idf.saveas("hh1.idf")

# replacebranch(loop, branch, listofcomponents)
# loop = loop of name p_loop
# branch = branch of name sb1

# make pipe components np1, np2
pipe1 = hvacbuilder.makepipecomponent(idf, 'np1')
pipe2 = hvacbuilder.makepipecomponent(idf, 'np2')
idf.saveas("hh2.idf")

# join them into a branch
# -----------------------
# np1_inlet -> np1 -> np1_np2_node -> np2 -> np2_outlet
    # change the node names in the component
    # empty the old branch
    # fill in the new components with the node names into this branch

# change the node names in the component so that they connect up. 
# make the change as a list [oldnode, newnode]
components = [pipe1, pipe2]
for i in range(len(components) - 1):
    thiscomp = components[i]
    nextcomp = components[i + 1]
    betweennodename = "%s_%s_node" % (thiscomp.Name, nextcomp.Name)
    thiscomp.Outlet_Node_Name = [thiscomp.Outlet_Node_Name, betweennodename]
    nextcomp.Inlet_Node_Name = [nextcomp.Inlet_Node_Name, betweennodename]
idf.saveas("hh3.idf")

# empty the old branch
    # function to get idd_comments of an object.
    # iddofobject(key) 
    # get the first extensible field
    # empty all extensible field
thebranch = idf.getobject('BRANCH', 'sb1') # don't need this line
thebranch = idf.removeextensibles('BRANCH', 'sb1')
idf.saveas("hh4.idf")

# fill in the new components with the node names into this branch
    # find the first extensible field and fill in the data in obj.
e_index = idf.getextensibleindex('BRANCH', 'sb1')
# pipe.Name, 
# in idd_info, insert the field name that EPbunch uses, and put in the input and output nodes
theobj = thebranch.obj
modeleditor.extendlist(theobj, e_index) # just being careful here
for comp in components:
    theobj.append(comp.key)
    theobj.append(comp.Name)
    theobj.append(comp.Inlet_Node_Name)
    theobj.append(comp.Outlet_Node_Name)
    theobj.append('')
idf.saveas("hh5.idf")

# rename a random node to the name of a renamed node
# abranch = idf.idfobjects['BRANCH'][0]
# abranch.Component_1_Inlet_Node_Name = 'np1_outlet'
# idf.saveas("hh6.idf")
    
# gather all renamed nodes
renameds = []
for key in idf.model.dtls:
    for idfobject in idf.idfobjects[key]:
        for fieldvalue in idfobject.obj:
            if type(fieldvalue) is list:
                if fieldvalue not in renameds:
                    cpvalue = copy.copy(fieldvalue)
                    renameds.append(cpvalue)

# do the renaming
for key in idf.model.dtls:
    for idfobject in idf.idfobjects[key]:
        for i, fieldvalue in enumerate(idfobject.obj):
            itsidd = idfobject.objidd[i]
            if itsidd.has_key('type'):
                if itsidd['type'][0] == 'node':
                    tempdct = dict(renameds)
                    if type(fieldvalue) is list:
                        fieldvalue = fieldvalue[-1]
                        idfobject.obj[i] = fieldvalue
                    else:
                        if tempdct.has_key(fieldvalue):
                            fieldvalue = tempdct[fieldvalue]
                            idfobject.obj[i] = fieldvalue
idf.saveas("hh7.idf")
print idf.idfobjects['PLANTLOOP'][0]

# check for the end nodes of the loop
