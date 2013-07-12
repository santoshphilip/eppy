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
# along with Eppy.  If not, see <http://www.gnu.org/licenses/>.

"""do a diff between two idf files"""

from modeleditor import IDF

iddfile = "../iddfiles/Energy+V6_0.idd"
fname1 = "../idffiles/V_6_0/ASHRAE30pct.PI.Final11_Hospital_STD2010_Chicago.idf"
fname2 = "../idffiles/V_6_0/ASHRAE30pct.PI.Final11_Hospital_STD2010_Miami.idf"
# fname1 = "../idffiles/V_7_2/smallfile.idf"
 
IDF.setiddname(iddfile)
idf1 = IDF(fname1)
idf2 = IDF(fname2)

keys = idf1.model.dtls # undocumented variable

for akey in keys:
    idfobjs1 = idf1.idfobjects[akey]
    idfobjs2 = idf2.idfobjects[akey]
    for idfobj1, idfobj2 in zip(idfobjs1, idfobjs2):
        for i, (f1, f2) in enumerate(zip(idfobj1.obj, idfobj2.obj)):
            if f1 != f2:
                print '%s, %s, %s, %s' % (akey, idfobj1.objidd[i]['field'][0], 
                        f1, f2, )
        



# bunchdt, data, commdct = idfreader(fname, iddfile)
# 
# outfilename = "afile.idf"
# txt = str(data)
# open(outfilename, 'w').write(txt)
