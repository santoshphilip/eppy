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

from modeleditor import IDF
import hvacbuilder
import iddv7
from StringIO import StringIO
IDF.setiddname(StringIO(iddv7.iddtxt))
idf = IDF('hh1.idf')
# idf.outputtype = 'compressed'
# idf.saveas('gumby.idf')

pipe1 = idf.newidfobject("PIPE:ADIABATIC", 'np1')
chiller = idf.newidfobject("Chiller:Electric".upper(), 'Central_Chiller')
pipe2 = idf.newidfobject("PIPE:ADIABATIC", 'np2')

loop = idf.getobject('CONDENSERLOOP', 'c_loop')
print loop
branch = idf.getobject('BRANCH', 'sb0')
listofcomponents = [chiller, pipe1, pipe2]

newbr = hvacbuilder.replacebranch(idf, loop, branch, listofcomponents, 'Water', False)
idf.saveas("hhh_new.idf")
