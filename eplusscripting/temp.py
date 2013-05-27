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

from modeleditor import IDF

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

