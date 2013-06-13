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

"""dev work on using IDF class"""
import modeleditor
from modeleditor import IDF

iddfile = "../iddfiles/Energy+V7_2_0.idd"
IDF.setiddname(iddfile)

fname1 = "../idffiles/V_7_2/smallfile.idf"
idf1 = IDF(fname1)

# print idf1

fname2 = "../idffiles/V_7_2/constructions.idf"
idf2 = IDF(fname2)

# # test addidfobject
# constr = idf2.idfobjects["construction".upper()][0]
# print constr
# idf1.addidfobject(constr)
# print idf1

# # test newidfobject
idf1.newidfobject("ZONE")
idf1.printidf()
idf1.newidfobject("ZONE", "gumby")
idf1.printidf()
 
# for objname in dtls:
#     for obj in idf.idfobjects[objname]:
#         print obj
