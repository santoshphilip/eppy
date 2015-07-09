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

"""sample script - autosize all autosizable fields"""
# email to jason
# Jason,
#   Try out the attached script.
# (you might have to change file pathnames)
#
# I don't think you could have written it on your own :-(
# It became apparent to me that eppy needs functions that allows it to look
# into the idd structure for any object and field
# I'll put some thought into this and see how best to write this.
# If that functionality is done well, hopefully anyone should be able to write
# the equivalent code to what I wrote in the attached file.
#
#
# Santosh

import sys
pathnameto_eplusscripting = "../../"
sys.path.append(pathnameto_eplusscripting)

from eppy import modeleditor
from eppy.modeleditor import IDF
from eppy import bunch_subclass

def autosize_fieldname(idfobject):
    """return autsizeable field names in idfobject"""
    # undocumented stuff in this code
    return [fname for (fname, dct) in zip(idfobject.objls,
                                          idfobject['objidd'])
            if 'autosizable' in dct]

iddfile = "../resources/iddfiles/Energy+V8_0_0.idd"
fname1 = "../resources/idffiles/V8_0_0/5ZoneWaterLoopHeatPump.idf"

IDF.setiddname(iddfile)
idf = IDF(fname1)
idf.saveas("./a.idf")




allidfobjects = idf.idfobjects
for objname in list(allidfobjects.keys()):
    idfobjects = allidfobjects[objname]
    for idfobject in idfobjects:
        autofields = autosize_fieldname(idfobject)
        for autofield in autofields:
            idfobject[autofield] = "autosize"

idf.saveas("./b.idf")
