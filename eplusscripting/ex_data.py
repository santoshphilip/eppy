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
print azone
# as you can see azone is the idf data as a list


# dtls 
print dtls[:10]
# dtls is a list of all object names

zone_i = dtls.index("zone".upper())
print zone_i
# zone_i = 76. So zone is the 76th object in dtls 
# (actually 77th since it is zeroindexed)

# take a look at the commdct[zone_i]
iddofzone = commdct[zone_i]
for i, field in enumerate(iddofzone):
    print "field %s" % (i, )
    print "-" * len( "field %s" % (i, ))
    for key in field.keys():
        print key
        print "\t", field[key]
# it contains all the idd information of the zone        
        
        