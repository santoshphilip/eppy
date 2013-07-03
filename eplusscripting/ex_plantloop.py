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


from modeleditor import IDF
import hvacbuilder

from StringIO import StringIO
iddfile = "../iddfiles/Energy+V7_0_0_036.idd"
IDF.setiddname(iddfile)



# make the topology of the loop
idf = IDF(StringIO(''))
loopname = "p_loop"
sloop = ['sb0', ['sb1', 'sb2', 'sb3'], 'sb4']
dloop = ['db0', ['db1', 'db2', 'db3'], 'db4']
hvacbuilder.makeplantloop(idf, loopname, sloop, dloop)
idf.saveas("hhh1.idf")

# replacebranch(loop, branch, listofcomponents)
# loop = loop of name p_loop
# branch = branch of name sb1

# make pipe components np1, np2
# pipe1 = hvacbuilder.makepipecomponent(idf, 'np1')
# pipe2 = hvacbuilder.makepipecomponent(idf, 'np2')
# idf.saveas("hhh2.idf")
# make a new branch chiller->pipe1-> pipe2
pipe1 = idf.newidfobject("PIPE:ADIABATIC", 'np1')
chiller = idf.newidfobject("Chiller:Electric".upper(), 'Central_Chiller')
pipe2 = idf.newidfobject("PIPE:ADIABATIC", 'np2')
# pipe3 = idf.newidfobject("PIPE:ADIABATIC", 'np4')
# pipe4 = idf.newidfobject("PIPE:ADIABATIC", 'np4')
# idf.saveas("hhh2.idf")

loop = idf.getobject('PLANTLOOP', 'p_loop')
branch = idf.getobject('BRANCH', 'sb0')
# listofcomponents = [pipe1, chiller, pipe2]
listofcomponents = [chiller, pipe1, pipe2]

newbr = hvacbuilder.replacebranch(idf, loop, branch, listofcomponents, 
                                    'Water', False)
# print newbr.obj 
# print branch
idf.saveas("hhh_new.idf")
