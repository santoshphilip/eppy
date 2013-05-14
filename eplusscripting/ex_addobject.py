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
# along with Eppy.  If not, see <http://www.gnu.org/licenses/>.

"""how to add an energyplus object
"""

from idfreader import makebunches
from idfreader import idfreader
import modeleditor

iddfile = "../iddfiles/Energy+V7_0_0_036.idd"
fname = "../idffiles/V_7_0/5ZoneSupRetPlenRAB.idf"
 
bunchdt, data, commdct = idfreader(fname, iddfile)

# give easy to remember names to objects that you are working on
zones = bunchdt['zone'.upper()] # all the zones

# print number of zones
print len(zones)
# 7
# We have 7 zones

# Let us add a new zone
modeleditor.addobject(bunchdt, data, commdct, "Zone".upper(), aname="NewZone")

# let print number of zones again
print len(zones)
# 8
# we have 8 zones

# the new zone will be the last one in the list
# let us take a look at it
print zones[-1]


# TODO : make a function ot copy an object.