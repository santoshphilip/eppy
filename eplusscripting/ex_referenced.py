"""access object that are referenced by other objects"""

from idfreader import idfreader

iddfile = "../iddfiles/Energy+V7_0_0_036.idd"
fname = "../idffiles/V_7_0/5ZoneSupRetPlenRAB.idf"
 
bunchdt, data, commdct = idfreader(fname, iddfile)

# give easy to remember names to objects that you are working on
zones = bunchdt['zone'.upper()] # all the zones
surfaces = bunchdt['BUILDINGSURFACE:DETAILED'.upper()] # all the surfaces

# change the name of the first zone
oldname = zones[0].Name
newname = "NEW-NAME"
zones[0].Name = newname

# find all the surfaces that belong to this zone and update
for surface in surfaces:
    if surface.Zone_Name == oldname:
        surface.Zone_Name = newname


# there may be other objects that refer to this zone.
# it would be good to have afunction that can update all of them
# renameobject(bunchdt, obj, newname)
# this shoule update all the references