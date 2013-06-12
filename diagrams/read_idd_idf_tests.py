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

import sys
sys.path.append('../EPlusInputcode')
from EPlusCode.EPlusInterfaceFunctions import readidf

# # just read a file and dump the text out.

iddfile = "../iddfiles/Energy+V6_0.idd"
fname = "../idffiles/a.idf"
data1, commdct1 = readidf.readdatacommdct(fname, iddfile=iddfile)
txt1 = `data1`
# print txt1[:100]

iddfile = "../iddfiles/Energy+V6_0.idd"
iddfobject = open(iddfile, 'r')
fname = "../idffiles/a.idf"
fnamefobject = open(fname, 'r')
data2, commdct2 = readidf.readdatacommdct(fnamefobject, iddfile=iddfile)
txt2 = `data2`
# print txt2[:100]

print "txt1 == txt2"
print txt1 == txt2


iddfile = "../iddfiles/Energy+V6_0.idd"
iddfobject = open(iddfile, 'r')
fname = "../idffiles/a.idf"
fnamefobject = open(fname, 'r')
data3, commdct3 = readidf.readdatacommdct(fname, iddfile=iddfobject)
txt3 = `data3`
# print txt2[:100]

print "txt1 == txt3"
print txt1 == txt3


iddfile = "../iddfiles/Energy+V6_0.idd"
iddfobject = open(iddfile, 'r')
fname = "../idffiles/a.idf"
fnamefobject = open(fname, 'r')
data3, commdct3 = readidf.readdatacommdct(fnamefobject, iddfile=iddfobject)
txt4 = `data3`
# print txt2[:100]

print "txt1 == txt4"
print txt1 == txt4

# read the idd thru an import
import iddV6_0
theiddd = iddV6_0.theidd
commdct = iddV6_0.commdct
iddfile = "../iddfiles/Energy+V6_0.idd"
iddfobject = open(iddfile, 'r')
fname = "../idffiles/a.idf"
fnamefobject = open(fname, 'r')
data3, commdct3 = readidf.readdatacommdct(fnamefobject, 
                            iddfile=theiddd, commdct=commdct)
txt5 = `data3`
# print txt2[:100]

print "txt1 == txt5"
print txt1 == txt5
