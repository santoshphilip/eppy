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

"""access object that are referenced by other objects"""

from idfreader import idfreader

iddfile = "../iddfiles/Energy+V7_0_0_036.idd"
fname = "../idffiles/V_7_0/5ZoneSupRetPlenRAB.idf"
 
bunchdt, data, commdct = idfreader(fname, iddfile)

# give easy to remember names to objects that you are working on
zones = bunchdt['zone'.upper()] # all the zones
surfaces = bunchdt['BUILDINGSURFACE:DETAILED'.upper()] # all the surfaces

# change the name of the first zone
oldname = zones[0].Name
newname = "NEW-NAME"
zones[0].Name = newname

# find all the surfaces that belong to this zone and update
for surface in surfaces:
    if surface.Zone_Name == oldname:
        surface.Zone_Name = newname


# there may be other objects that refer to this zone.
# it would be good to have afunction that can update all of them
# renameobject(bunchdt, obj, newname)
# this shoule update all the references