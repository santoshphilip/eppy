"""from BUILDINGSURFACE:DETAILED and FENESTRATIONSURFACE:DETAILED make a wall floor, celiling etc or a window"""

# key fields:
# Name
# Surface Type
#     key Floor
#     key Wall
#     key Ceiling
#     key Roof
# Construction Name
# Zone Name
# Outside Boundary Condition
#     key Adiabatic
#     key Surface
#     key Zone
#     key Outdoors
#     key Ground
#     key GroundFCfactorMethod
#     key OtherSideCoefficients
#     key OtherSideConditionsModel
#     key GroundSlabPreprocessorAverage
#     key GroundSlabPreprocessorCore
#     key GroundSlabPreprocessorPerimeter
#     key GroundBasementPreprocessorAverageWall
#     key GroundBasementPreprocessorAverageFloor
#     key GroundBasementPreprocessorUpperWall
#     key GroundBasementPreprocessorLowerWall
# Outside Boundary Condition Object
# 
# 'FENESTRATIONSURFACE:DETAILED',
# Surface_Type
#        key Window
#        key Door
#        key GlassDoor
#        key TubularDaylightDome
#        key TubularDaylightDiffuser
# 
# 
# 'BUILDINGSURFACE:DETAILED',
# (simple_surface, Surface_Type, Outside_Boundary_Condition)
# ----------------------------------------------------------
# ('WALL:EXTERIOR', Wall, Outdoors)
# ('WALL:ADIABATIC',Wall, Adiabatic)
# ('WALL:UNDERGROUND', Wall, s.startswith('Ground'))
# ('WALL:INTERZONE', Wall, Surface OR Zone)
# ('ROOF', Roof, None or Outdoor)
# ('CEILING:ADIABATIC', Ceiling, Adiabatic)
# ('CEILING:INTERZONE', Ceiling, Surface OR Zone)
# ('FLOOR:GROUNDCONTACT', Floor, s.startswith('Ground'))
# ('FLOOR:ADIABATIC', Floor, Adiabatic)
# ('FLOOR:INTERZONE', Floor, Surface OR Zone)
# 
# 'FENESTRATIONSURFACE:DETAILED',
# (simple_surface, Surface_Type, Outside_Boundary_Condition)
# ----------------------------------------------------------
# ('WINDOW',  Window, None)
# ('DOOR', Door, None)

class NotImplementedError(object):
    pass

def add(a, b):
    return a + b

def bsdorigin(bsdobject, setto000=False):
    """return the origin of the surface"""
    # not yet implemented
    raise NotImplementedError
    return (0, 0, 0)

def wallexterior(idf, bsdobject, setto000=False):
    """return an wall:exterior object if the bsd is an exterior wall"""
    # test if it is an exterior wall
    if bsdobject.Surface_Type.upper() == 'WALL': # Surface_Type == wall
        if bsdobject.Outside_Boundary_Condition.upper() == 'OUTDOORS': # Outside_Boundary_Condition == Outdoor
            # return wallexterior
            wallext = idf.newidfobject('WALL:EXTERIOR')
            wallext.Name = bsdobject.Name
            wallext.Construction_Name = bsdobject.Construction_Name
            wallext.Zone_Name = bsdobject.Zone_Name
            wallext.Azimuth_Angle = bsdobject.azimuth
            wallext.Tilt_Angle = bsdobject.tilt
            surforigin = bsdorigin(bsdobject, setto000=setto000)
            wallext.Starting_X_Coordinate = surforigin[0]
            wallext.Starting_Y_Coordinate = surforigin[1]
            wallext.Starting_Z_Coordinate = surforigin[2]
            wallext.Length = bsdobject.width
            wallext.Height = bsdobject.height
            return wallext
    return None
            
        
    
    