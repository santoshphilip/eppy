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

"""examples of pythonic operations on energyplus objects"""
# try these out line by line in the python interpreter or in ipython

from idfreader import idfreader

iddfile = "../iddfiles/Energy+V7_0_0_036.idd"
fname = "../idffiles/V_7_0/5ZoneSupRetPlenRAB.idf"
 
bunchdt, data, commdct = idfreader(fname, iddfile)

# give easy to remember names to objects that you are working on
zones = bunchdt['zone'.upper()] # all the zones
surfaces = bunchdt['BUILDINGSURFACE:DETAILED'.upper()] # all the surfaces

# first zone - zone0
zone0 = zones[0]

# name of zone0
print zone0.Name

# allzone names
zonenames = [zone.Name for zone in zones]
print zonenames


zonevolumes = [zone.Volume for zone in zones]
print zonevolumes
# note that zone volumes are strings, not floats
# future version will automatically have them as floats

# filter to get zones less than 150 m3
smallzones = [zn for zn in zones if float(zn.Volume) < 150]
#name and volume of small zones
namevolume = [(zn.Name, zn.Volume) for zn in smallzones]
print namevolume

# number of small zones
print len(smallzones)
#let us rename the small zones
smallzones[0].Name = "FIRST-SMALL-ZONE"
smallzones[1].Name = "SECOND-SMALL-ZONE"
# now the zone names are:
zonenames = [zone.Name for zone in zones]
print zonenames

# now we have a problem
# surfaces still refer to the old zone names
# see ex_referenced.py to see how to change those references

# future version will have a function that will automatically update the references.

# save to disk and look at the file
txt = str(data) # bunchdt is actually changing values in data
open("bfile.idf", 'w').write(txt)
# open the idf file and search for the string "SMALL"


