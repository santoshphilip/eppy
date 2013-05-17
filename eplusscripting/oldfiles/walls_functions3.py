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

"""do just walls in eplusinterface"""

from idfreader import idfreader


iddfile = "../iddfiles/Energy+V7_0_0_036.idd"
fname = "../idffiles/V_7_0/5ZoneSupRetPlenRAB.idf"
 
bunchdt, data, commdct = idfreader(fname, iddfile)
surfaces = bunchdt['BUILDINGSURFACE:DETAILED'.upper()] # all the surfaces

for surface in surfaces:
    name = surface.Name
    area = surface.area
    height = surface.height
    width = surface.width
    azimuth = surface.azimuth
    tilt = surface.tilt
    print name, area, height, width, azimuth, tilt

# print wall.Name
# print wall.obj[10]
# print wall.obj[11]
# print wall.obj[12]
# print wall.plus
# print wall.__functions
# for surface in surfaces:
#     name, construction = surface.plus
#     n1, c1 = surface.Name, surface.Construction_Name
#     assert name == n1
#     assert construction == c1

# lst = range(12)
# coords = []
# for i in range(len(lst)):
#     i % 3
#     # coord = []
#     # for j in range(3):
#     #     coord.append(lst[i])
#     # coords.append(coord)
#     #     
# two = [(lst[i], i % 3) for i in range(len(pts))]    
# coords = []
# coord = []
# for i, j in two:
#     if j < 2:
#         coord.append(i)
#         continue
#     else:
#         coord.append(i)
#         coords.append(coord)
#         coord = []
    
    