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