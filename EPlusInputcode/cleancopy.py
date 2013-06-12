# Copyright (c) 2012 Santosh Philip

# This file is part of eplusinterface_diagrams.

# Eplusinterface_diagrams is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# Eplusinterface_diagrams is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with eplusinterface_diagrams.  If not, see <http://www.gnu.org/licenses/>.

"""clean file with no comments"""
from EPlusCode.EPlusInterfaceFunctions import readidf


fname = '../idffiles/a.idf'
outfile = '../idffiles/a_clean.idf'
iddfile = '../iddfiles/Energy+V6_0.idd'
data, commdct = readidf.readdatacommdct(fname, iddfile)
# - 
# move surfaces and shades    
# surfacekey = 'BuildingSurface:Detailed'.upper()
# shadekey = 'Shading:Building:Detailed'.upper()

open(outfile, 'w').write(`data`)

