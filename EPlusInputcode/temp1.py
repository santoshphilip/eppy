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

"""make names of objects inot single words, so that they can be selected with a double click."""
# usage below
from EPlusCode.EPlusInterfaceFunctions import readidf


fname = "../template/HVACTemplate-5ZoneFanCoil2.idf"
outname = "../template/a.idf"
data, commdct = readidf.readdatacommdct(fname)

changes = {}
for j, key in enumerate(data.dtls):
    items = data.dt[key]
    for item in items:
        name = item[1]
        newname = name.replace(' ', '_')
        newname = newname.replace('-', '__')
        if (name.count(' ') > 0) or (name.count('-') > 0):
            if commdct[j][1]['field'][0] == 'Name': # only name fields are changed
                changes[name] = newname
                item[1] = newname
# TODO : if changes.values() has duplicate names -> abort with message - not needed.

for key in data.dtls:
    items = data.dt[key]        
    for item in items:
        for i, field in enumerate(item):
            try:
                item[i] = changes[field]
            except KeyError, e:
                pass

open(outname, 'w').write(`data`)
