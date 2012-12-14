"""how to add an energyplus object
needs a better interface. This is a placeholder until then.
"""

from idfreader import makebunches
from idfreader import idfreader

iddfile = "../iddfiles/Energy+V7_0_0_036.idd"
fname = "../idffiles/V_7_0/5ZoneSupRetPlenRAB.idf"
 
bunchdt, data, commdct = idfreader(fname, iddfile)

# give easy to remember names to objects that you are working on
zones = bunchdt['zone'.upper()] # all the zones
surfaces = bunchdt['BUILDINGSURFACE:DETAILED'.upper()] # all the surfaces


# make a copy of the first zone

# we are working directly with data to do this.
# see ex_data.py for more details on working with data

# bunchdt is syntactic sugar for data
# tha actual idf file is contained in data

# how to add an object using just data
dt = data.dt
zn = dt['zone'.upper()][0] # first zone
copyofzn = list(zn) # copies a list
dt['zone'.upper()].append(copyofzn)
bunchdt = makebunches(data, commdct) # push data into bunchdt
zones = bunchdt['zone'.upper()] # list of all the zones

# bunchdt can help in doing this
zones = bunchdt['zone'.upper()] # all the zones
# bunchdt has a specail filed called obj
print zone[0].obj
# note that zone[0].obj is the list from data.dt['zone'.upper()][0]
if data.dt['zone'.upper()][0] is zone.obj[0]:
    print "data.dt['zone'.upper()][0] is same as zone.obj[0]"
# so we can do this
dt['zone'.upper()].append(list(zone.obj))
# and then
bunchdt = makebunches(data, commdct) # push data into bunchdt
zones = bunchdt['zone'.upper()] # list of all the zones

# what if you don't want to copy a zone, but want to make a new zone
# you have to handcraft a list
# we really need a function to do this
zoneaslist = ['Zone', 'ANEWZONE', '0', '0', '0', '0', '1', '1', '0.609600067', '283.2']
dt['zone'.upper()].append(zoneaslist) # append an empty list
bunchdt = makebunches(data, commdct) # push data into bunchdt
zones = bunchdt['zone'.upper()] # list of all the new zones
lastzone = zones[-1]
