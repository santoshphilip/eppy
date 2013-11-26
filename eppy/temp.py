# import sys
# pathnameto_eppy = '../'
# sys.path.append(pathnameto_eppy)
# from eppy import modeleditor
# from eppy.modeleditor import IDF
# iddfile = "./resources/iddfiles/Energy+V7_2_0.idd"
# fname1 = "./resources/idffiles/V_7_2/smallfile.idf"
# IDF.setiddname(iddfile)
# idf1 = IDF(fname1)
# idf1.newidfobject('BUILDINGSURFACE:DETAILED')
# idf1.newidfobject('FENESTRATIONSURFACE:DETAILED')
# idf1.newidfobject('WALL:EXTERIOR')
# bsd = idf1.newidfobject('BUILDINGSURFACE:DETAILED')
# bsd = idf1.newidfobject('BUILDINGSURFACE:DETAILED')
# print bsd
# fname1 = "./resources/idffiles/V_7_0/5ZoneSupRetPlenRAB.idf"
# idf1 = IDF(fname1)
# surfaces = idf1.idfobjects['BUILDINGSURFACE:DETAILED']
# surface = surfaces[0]
# print surface.__functions
# # print "surface azimuth =",  surface.azimuth, "degrees"
# # print "surface tilt =", surface.tilt, "degrees"
# # print "surface area =", surface.area, "m2"
# # surface.width
# # surface.height

from copy import copy
import sys
pathnameto_eppy = '../'
sys.path.append(pathnameto_eppy)
from eppy import modeleditor
from eppy.modeleditor import IDF
from eppy import simplesurface
iddfile = "./resources/iddfiles/Energy+V7_2_0.idd"
fname1 = "./resources/idffiles/V_7_2/smallfile.idf"
IDF.setiddname(iddfile)
fname1 = "./resources/idffiles/V_7_0/5ZoneSupRetPlenRAB.idf"
fname1 = "/Volumes/Server/Staff/Santosh/mike_eplus/working/5ZoneSupRetPlenRAB.idf"
idf1 = IDF(fname1)

zones = idf1.idfobjects['ZONE']
for zone in zones:
    # print zone.Floor_Area, zone.Volume, zone.Ceiling_Height
    try:
        area = modeleditor.zonearea(idf1, zone.Name)
        volume =  modeleditor.zonevolume(idf1, zone.Name)
        height = modeleditor.zoneheight(idf1, zone.Name)
        zone.Floor_Area = area
        zone.Volume = volume
        zone.Ceiling_Height = height
        print zone.Name, area, height, volume
    except ValueError, e:
        print zone.Name, " - messed up"
# 
# 
# 
surfaces = idf1.idfobjects['BUILDINGSURFACE:DETAILED']
csurfaces = copy(surfaces)

count = 0
print len(surfaces)
for surface in csurfaces:
    s = simplesurface.simplesufrace(idf1, surface, deletebsd=True, setto000=True)
    if not s:
        print surface.Name
    count += 1
print count
print len(csurfaces)    
print len(surfaces)    

fens = idf1.idfobjects['FENESTRATIONSURFACE:DETAILED']
cfens = copy(fens)
print len(fens)  
count = 0
for fen in cfens:
    f = simplesurface.simplefenestration(idf1, fen, deletebsd=True, setto000=True)
    if not f:
        print fen.Name
    count += 1
print count 
print len(cfens) 
print len(fens) 

newfname1 = "/Volumes/Server/Staff/Santosh/mike_eplus/working/5ZoneSupRetPlenRAB_flat.idf"

idf1.saveas(newfname1)