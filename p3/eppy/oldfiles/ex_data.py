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

"""working directly with data without bunchdt"""

from idfreader import idfreader

iddfile = "../iddfiles/Energy+V7_0_0_036.idd"
fname = "../idffiles/V_7_0/5ZoneSupRetPlenRAB.idf"
 
bunchdt, data, commdct = idfreader(fname, iddfile)

# bunchdt is syntactic sugar for data and commdct
# any operation on bunchdt changes information in data

# The objective of this development is to never work directly with data
# bunchdt should give a pythonic interface to do all operations

# as yet not all functions are avaliable in bunchdt
# so one may have to directly work with data
# as explained below.

dt = data.dt
dtls = data.dtls

# let us work only on zones
zones = dt["zone".upper()]
azone = zones[0]
print(azone)
# as you can see azone is the idf data as a list


# dtls 
print(dtls[:10])
# dtls is a list of all object names

zone_i = dtls.index("zone".upper())
print(zone_i)
# zone_i = 76. So zone is the 76th object in dtls 
# (actually 77th since it is zeroindexed)

# take a look at the commdct[zone_i]
iddofzone = commdct[zone_i]
for i, field in enumerate(iddofzone):
    print("field %s" % (i, ))
    print("-" * len( "field %s" % (i, )))
    for key in list(field.keys()):
        print(key)
        print("\t", field[key])
# it contains all the idd information of the zone        
        
        