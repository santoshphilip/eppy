import sys
pathnameto_eppy = '../'
sys.path.append(pathnameto_eppy)
from eppy import modeleditor
from eppy.modeleditor import IDF
iddfile = "./resources/iddfiles/Energy+V7_2_0.idd"
fname1 = "./resources/idffiles/V_7_2/smallfile.idf"
IDF.setiddname(iddfile)
idf1 = IDF(fname1)
idf1.newidfobject('BUILDINGSURFACE:DETAILED')
idf1.newidfobject('FENESTRATIONSURFACE:DETAILED')
idf1.newidfobject('WALL:EXTERIOR')
bsd = idf1.newidfobject('BUILDINGSURFACE:DETAILED')
bsd = idf1.newidfobject('BUILDINGSURFACE:DETAILED')
print bsd
fname1 = "./resources/idffiles/V_7_0/5ZoneSupRetPlenRAB.idf"
idf1 = IDF(fname1)
surfaces = idf1.idfobjects['BUILDINGSURFACE:DETAILED']
surface = surfaces[0]
print surface.__functions
# print "surface azimuth =",  surface.azimuth, "degrees"
# print "surface tilt =", surface.tilt, "degrees"
# print "surface area =", surface.area, "m2"
# surface.width
# surface.height