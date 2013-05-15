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

"""read the idf file using a file handle"""
# tested and works now

from idfreader import idfreader
import modeleditor
from modeleditor import IDF

iddfile = "../iddfiles/Energy+V7_0_0_036.idd"
fname = "../idffiles/V_7_0/5ZoneSupRetPlenRAB.idf"


 
# bunchdt, data, commdct = idfreader(fname, iddfile)
# s = str(data)
# open("f.idf", 'w').write(s)



# reading idd
# -----------
# idfreader -> 
# readidf.readdatacommdct ->
# parse_idd.extractidddata ->
# DONE

# reading idf
# -----------
# idfreader -> 
# readidf.readdatacommdct ->
# eplusdata.eplusdata(theidd,idfname)

iddhandle = open(iddfile, 'r')
fhandle = open(fname, 'r')

bunchdt, data, commdct = idfreader(fname, iddhandle)
s = str(data)
open("fh.idf", 'w').write(s)

iddhandle.close()
fhandle.close()
# -----------

iddhandle = open(iddfile, 'r')
fhandle = open(fname, 'r')

# bunchdt, data, commdct = idfreader(fhandle, iddhandle)
# s = str(data)
# open("fhfh.idf", 'w').write(s)

iddhandle.close()
fhandle.close()
# -----------

from StringIO import StringIO
iddtxt = """Version,
      \\unique-object
      \\format singleLine
  A1 ; \\field Version Identifier
      \\required-field
      \\default 5.0

"""

idftxt = """Version,6.0;
"""
iddhandle = StringIO(iddtxt)
# iddhandle = open(iddfile, 'r')
fhandle = StringIO(idftxt)

bunchdt, data, commdct = idfreader(fhandle, iddhandle)
s = str(data)
open("fsfs.idf", 'w').write(s)

iddhandle.close()
fhandle.close()
# -----------
# open using IDF
iddhandle = open(iddfile, 'r')
fhandle = open(fname, 'r')

IDF.setiddname(iddhandle)

idf1 = IDF(fhandle)
idf1.saveas("isis.idf")
# idf1.printidf()
s = idf1.asstring()
print s
iddhandle.close()
fhandle.close()
