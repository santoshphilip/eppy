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
    
    