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

# from idfreader import idfreader
import modeleditor
from modeleditor import IDF
# 
iddfile = "../iddfiles/Energy+V7_0_0_036.idd"
fname = "../idffiles/V_7_0/5ZoneSupRetPlenRAB.idf"
IDF.setiddname(iddfile)
idf = IDF(fname)
# give easy to remember names to objects that you are working on
zones = idf.idfobjects['zone'.upper()] # all the zones
surfaces = idf.idfobjects['BUILDINGSURFACE:DETAILED'.upper()] # all the surfaces

# 
# first zone - zone0
zone0 = zones[0]

# name of zone0
print zone0.Name

# allzone names
zonenames = [zone.Name for zone in zones]
print zonenames


zonevolumes = [zone.Volume for zone in zones]
print zonevolumes

# filter to get zones less than 150 m3
smallzones = [zn for zn in zones if float(zn.Volume) < 150]
#name and volume of small zones
namevolume = [(zn.Name, zn.Volume) for zn in smallzones]
print namevolume

# number of small zones
print len(smallzones)
print smallzones[0].Name
print smallzones[1].Name
#We could rename the small zones by saying
# smallzones[0].Name = "FIRST-SMALL-ZONE"
# smallzones[1].Name = "SECOND-SMALL-ZONE"
# now we have a problem
# surfaces still refer to the old zone names

# to safely change the name of an idfobject so that all the references are 
# updated, we do the following:

modeleditor.rename(idf, smallzones[0], "FIRST-SMALL-ZONE")
modeleditor.rename(idf, smallzones[1], "SECOND-SMALL-ZONE")



# now the zone names are:
zonenames = [zone.Name for zone in zones]
print zonenames

# 
# save to disk and look at the file
idf.saveas('bfile.idf')
# open the idf file and search for the string "SMALL"
# You will find all the places where the name was changed