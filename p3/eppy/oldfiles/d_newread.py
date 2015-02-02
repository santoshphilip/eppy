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

"""build a new reader that will read idd only once"""
import datetime
import idfreader
from modeleditor import IDF

d0 = datetime.datetime.now()
iddfilef = "../iddfiles/Energy+V7_0_0_036.idd"
iddfile = open(iddfilef, 'r')
# print iddfile.next()
# print iddfile
fname = "../idffiles/V_7_0/5ZoneSupRetPlenRAB.idf"



 
# bunchdt, data, commdct = idfreader.idfreader(fname, iddfile)

# reading idd
# -----------
# idf = IDF(fname)
# idfreader1(fname, iddfile) -> 
# readidf.readdatacommdct1(fname, iddfile) ->
# parse_idd.extractidddata(idfname, iddfile) 
# and eplusdata.eplusdata(theidd,)


IDF.setiddname(iddfile)
idf = IDF(fname)
iddfile.close()

d1 = datetime.datetime.now()
print(d1 -d0)
# idf.printidf()

d0 = d1
idf1 = IDF(fname)
d1 = datetime.datetime.now()
print(d1 -d0)

d0 = d1
idf1 = IDF(fname)
d1 = datetime.datetime.now()
print(d1 -d0)

d0 = d1
idf1 = IDF(fname)
d1 = datetime.datetime.now()
print(d1 -d0)

d0 = d1
idf1 = IDF(fname)
d1 = datetime.datetime.now()
print(d1 -d0)

d0 = d1
fhandle = open(fname, 'r')
idf1 = IDF(fhandle)
d1 = datetime.datetime.now()
print(d1 -d0)
