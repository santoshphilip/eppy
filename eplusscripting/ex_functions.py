"""examples of calling functions attached to energyplus objects

Azimuth, tilt and area of any surface can be calculated using the function API

example:-

    - surface = allobjects['BUILDINGSURFACE:DETAILED'][0] # a surface
    - surface.azimuth # gives azimuth of surface
    - surface.tilt # gives tilt of surface
    - surface.area # gives area of surface
"""


from idfreader import idfreader

iddfile = "../iddfiles/Energy+V7_0_0_036.idd"
fname = "../idffiles/V_7_0/5ZoneSupRetPlenRAB.idf"
 
bunchdt, data, commdct = idfreader(fname, iddfile)
surfaces = bunchdt['BUILDINGSURFACE:DETAILED'.upper()] # all the surfaces

# Let us look at the first surface
surface = surfaces[0]
# WALL-1PF
print surface.azimuth
# 180.0
print surface.tilt
# 0.0
print surface.area
# 18.3

# all the surface names
s_names = [surface.Name for surface in surfaces]
print s_names[:5] # print five of them
# ['WALL-1PF', 'WALL-1PR', 'WALL-1PB', 'WALL-1PL', 'TOP-1']

# surface names and azimuths
s_names_azm = [(sf.Name, sf.azimuth) for sf in surfaces]
print s_names_azm[:5] # print five of them
# [('WALL-1PF', 180.0), ('WALL-1PR', 90.0), ('WALL-1PB', 0.0), 
# ('WALL-1PL', 270.0), ('TOP-1', 0.0)]

# surface names and tilts
s_names_tilt = [(sf.Name, sf.tilt) for sf in surfaces]
print s_names_tilt[:5] # print five of them
# [('WALL-1PF', 0.0), ('WALL-1PR', 0.0), ('WALL-1PB', 0.0), 
# ('WALL-1PL', 0.0), ('TOP-1', 90.0)]

# surface names and areas
s_names_area = [(sf.Name, sf.area) for sf in surfaces]
print s_names_area[:5] # print five of them
# [('WALL-1PF', 18.299999999999997), ('WALL-1PR', 9.1199999999999974), 
# ('WALL-1PB', 18.299999999999997), ('WALL-1PL', 9.1199999999999974), 
# ('TOP-1', 463.59999999999997)]
