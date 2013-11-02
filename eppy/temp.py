from eppy import modeleditor
from eppy.modeleditor import IDF



def zoneareavolume(idf, zonename):
    zone = idf.getobject('ZONE', zonename)
    surfs = idf.idfobjects['BuildingSurface:Detailed'.upper()]
    zone_surfs = [s for s in surfs if s.Zone_Name == zone.Name]
    floors = [s for s in zone_surfs if s.Surface_Type.upper() == 'FLOOR']
    area = sum([floor.area for floor in floors])
    roofs = [s for s in zone_surfs if s.Surface_Type.upper() == 'ROOF']
    ceilings = [s for s in zone_surfs if s.Surface_Type.upper() == 'CEILING']
    topsurfaces = roofs + ceilings

    topz = []
    for topsurface in topsurfaces:
        for coord in topsurface.coords:
            topz.append(coord[-1])
    topz = max(topz)
        
    botz = []
    for floor in floors:
        for coord in floor.coords:
            botz.append(coord[-1])
    botz = min(botz)

    height = topz - botz
    volume = area * height

    return area, volume
    
def zonearea(idf, zonename):
    zone = idf.getobject('ZONE', zonename)
    surfs = idf.idfobjects['BuildingSurface:Detailed'.upper()]
    zone_surfs = [s for s in surfs if s.Zone_Name == zone.Name]
    floors = [s for s in zone_surfs if s.Surface_Type.upper() == 'FLOOR']
    area = sum([floor.area for floor in floors])
    return area
    
def zonevolume(idf, zonename):
    zone = idf.getobject('ZONE', zonename)
    surfs = idf.idfobjects['BuildingSurface:Detailed'.upper()]
    zone_surfs = [s for s in surfs if s.Zone_Name == zone.Name]
    floors = [s for s in zone_surfs if s.Surface_Type.upper() == 'FLOOR']
    area = sum([floor.area for floor in floors])
    roofs = [s for s in zone_surfs if s.Surface_Type.upper() == 'ROOF']
    ceilings = [s for s in zone_surfs if s.Surface_Type.upper() == 'CEILING']
    topsurfaces = roofs + ceilings

    topz = []
    for topsurface in topsurfaces:
        for coord in topsurface.coords:
            topz.append(coord[-1])
    topz = max(topz)
        
    botz = []
    for floor in floors:
        for coord in floor.coords:
            botz.append(coord[-1])
    botz = min(botz)

    height = topz - botz
    volume = area * height

    return volume
        
fname = "./eppy/resources/idffiles/V8_0_0/5ZoneSupRetPlenRAB.idf"
iddname = "./eppy/resources/iddfiles/Energy+V8_0_0.idd"

IDF.setiddname(iddname)
idf = IDF(fname)

zonename = 'SPACE1-1'
print zoneareavolume(idf, zonename)
print zonearea(idf, zonename)    
print zonevolume(idf, zonename)