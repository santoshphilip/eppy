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


"""figure out how to switch branches in a loop."""

import sys
sys.path.append('../')
import copy

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

# make pipe components np1, np2
pipe1 = hvacbuilder.makepipecomponent(idf, 'np1')
pipe2 = hvacbuilder.makepipecomponent(idf, 'np2')
idf.saveas("hh2.idf")

# join them into a branch
# -----------------------
# np1_inlet -> np1 -> np1_np2_node -> np2 -> np2_outlet
# change the node names in the component
# empty the old branch
# fill in the new components with the node names

# change the node names in the component
components = [pipe1, pipe2]
for i in range(len(components) - 1):
    thiscomp = components[i]
    nextcomp = components[i + 1]
    betweennodename = "%s_%s_node" % (thiscomp.Name, nextcomp.Name)
    thiscomp.Outlet_Node_Name = betweennodename
    nextcomp.Inlet_Node_Name = betweennodename
idf.saveas("hh3.idf")

# empty the old branch