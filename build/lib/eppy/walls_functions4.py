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

"""do just walls in eplusinterface"""

from idfreader import idfreader


iddfile = "../iddfiles/Energy+V7_2_0.idd"
fname = "../idffiles/V_7_2/box_tiltrot.idf"
 
bunchdt, data, commdct = idfreader(fname, iddfile)
surfaces = bunchdt['BUILDINGSURFACE:DETAILED'.upper()]
# surfaces = bunchdt['FenestrationSurface:Detailed'.upper()]

wall = surfaces[0]
# n_vertices = 'Number_of_Vertices'
# n_vertices_i = wall.objls.index(n_vertices)


for surface in surfaces:
    name = surface.Name
    area = surface.area
    # height = surface.height
    # width = surface.width
    azimuth = surface.azimuth
    tilt = surface.tilt
    # coords = surface.coords
    # print name, area, height, width, azimuth, tilt
    # print name, azimuth
    print name, area, azimuth, tilt


