# Copyright (c) 2012 Santosh Philip
# =======================================================================
#  Distributed under the MIT License.
#  (See accompanying file LICENSE or copy at
#  http://opensource.org/licenses/MIT)
# =======================================================================
"""from BUILDINGSURFACE:DETAILED and FENESTRATIONSURFACE:DETAILED make a wall
floor, celiling etc or a window"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

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
# ('CEILING:INTERZONE', Ceiling, Surface OR Zone or OtherSideCoefficients)
# ('FLOOR:GROUNDCONTACT', Floor, s.startswith('Ground'))
# ('FLOOR:ADIABATIC', Floor, Adiabatic)
# ('FLOOR:INTERZONE', Floor, Surface OR Zone or OtherSideCoefficients)
#
# 'FENESTRATIONSURFACE:DETAILED',
# (simple_surface, Surface_Type, Outside_Boundary_Condition)
# ----------------------------------------------------------
# ('WINDOW',  Window, None)
# ('DOOR', Door, None)


class NotImplementedError(Exception):
    """Exception Object"""

    pass


def bsdorigin(bsdobject, setto000=False):
    """return the origin of the surface"""
    # not yet implemented
    if setto000:
        return (0, 0, 0)
    else:
        raise NotImplementedError


def fsdorigin(fsdobject, setto000=False):
    """return the origin of the surface"""
    # not yet implemented
    if setto000:
        return (0, 0)
    else:
        raise NotImplementedError


def wallexterior(idf, bsdobject, deletebsd=True, setto000=False):
    """return an wall:exterior object if the  (buildingsurface:detailed) is
    an exterior wall"""
    # ('WALL:EXTERIOR', Wall, Outdoors)
    # test if it is an exterior wall
    if bsdobject.Surface_Type.upper() == "WALL":  # Surface_Type == wall
        if (
            bsdobject.Outside_Boundary_Condition.upper() == "OUTDOORS"
        ):  # Outside_Boundary_Condition == Outdoor
            simpleobject = idf.newidfobject("WALL:EXTERIOR")
            simpleobject.Name = bsdobject.Name
            simpleobject.Construction_Name = bsdobject.Construction_Name
            simpleobject.Zone_Name = bsdobject.Zone_Name
            simpleobject.Azimuth_Angle = bsdobject.azimuth
            simpleobject.Tilt_Angle = bsdobject.tilt
            surforigin = bsdorigin(bsdobject, setto000=setto000)
            simpleobject.Starting_X_Coordinate = surforigin[0]
            simpleobject.Starting_Y_Coordinate = surforigin[1]
            simpleobject.Starting_Z_Coordinate = surforigin[2]
            simpleobject.Length = bsdobject.width
            simpleobject.Height = bsdobject.height
            if deletebsd:
                idf.removeidfobject(bsdobject)
            return simpleobject
    return None


def walladiabatic(idf, bsdobject, deletebsd=True, setto000=False):
    """return a wall:adiabatic if bsdobject (buildingsurface:detailed) is an
    adibatic wall"""
    # ('WALL:ADIABATIC',Wall, Adiabatic)
    # test if it is an adiabatic wall
    if bsdobject.Surface_Type.upper() == "WALL":  # Surface_Type == wall
        if (
            bsdobject.Outside_Boundary_Condition.upper() == "ADIABATIC"
        ):  # Outside_Boundary_Condition == Adiabatic
            simpleobject = idf.newidfobject("WALL:ADIABATIC")
            simpleobject.Name = bsdobject.Name
            simpleobject.Construction_Name = bsdobject.Construction_Name
            simpleobject.Zone_Name = bsdobject.Zone_Name
            simpleobject.Azimuth_Angle = bsdobject.azimuth
            simpleobject.Tilt_Angle = bsdobject.tilt
            surforigin = bsdorigin(bsdobject, setto000=setto000)
            simpleobject.Starting_X_Coordinate = surforigin[0]
            simpleobject.Starting_Y_Coordinate = surforigin[1]
            simpleobject.Starting_Z_Coordinate = surforigin[2]
            simpleobject.Length = bsdobject.width
            simpleobject.Height = bsdobject.height
            if deletebsd:
                idf.removeidfobject(bsdobject)
            return simpleobject
    return None


def wallunderground(idf, bsdobject, deletebsd=True, setto000=False):
    """return a wall:underground if bsdobject (buildingsurface:detailed) is an
    underground wall"""
    # ('WALL:UNDERGROUND', Wall, s.startswith('Ground'))
    # test if it is an underground wall
    if bsdobject.Surface_Type.upper() == "WALL":  # Surface_Type == wall
        if bsdobject.Outside_Boundary_Condition.upper().startswith(
            "GROUND"
        ):  # Outside_Boundary_Condition startswith 'ground'
            simpleobject = idf.newidfobject("WALL:UNDERGROUND")
            simpleobject.Name = bsdobject.Name
            simpleobject.Construction_Name = bsdobject.Construction_Name
            simpleobject.Zone_Name = bsdobject.Zone_Name
            simpleobject.Azimuth_Angle = bsdobject.azimuth
            simpleobject.Tilt_Angle = bsdobject.tilt
            surforigin = bsdorigin(bsdobject, setto000=setto000)
            simpleobject.Starting_X_Coordinate = surforigin[0]
            simpleobject.Starting_Y_Coordinate = surforigin[1]
            simpleobject.Starting_Z_Coordinate = surforigin[2]
            simpleobject.Length = bsdobject.width
            simpleobject.Height = bsdobject.height
            if deletebsd:
                idf.removeidfobject(bsdobject)
            return simpleobject
    return None


def wallinterzone(idf, bsdobject, deletebsd=True, setto000=False):
    """return an wall:interzone object if the bsd (buildingsurface:detailed)
    is an interaone wall"""
    # ('WALL:INTERZONE', Wall, Surface OR Zone OR OtherSideCoefficients)
    # test if it is an exterior wall
    if bsdobject.Surface_Type.upper() == "WALL":  # Surface_Type == wall
        if bsdobject.Outside_Boundary_Condition.upper() in (
            "SURFACE",
            "ZONE",
            "OtherSideCoefficients".upper(),
        ):
            simpleobject = idf.newidfobject("WALL:INTERZONE")
            simpleobject.Name = bsdobject.Name
            simpleobject.Construction_Name = bsdobject.Construction_Name
            simpleobject.Zone_Name = bsdobject.Zone_Name
            obco = "Outside_Boundary_Condition_Object"
            simpleobject[obco] = bsdobject[obco]
            simpleobject.Azimuth_Angle = bsdobject.azimuth
            simpleobject.Tilt_Angle = bsdobject.tilt
            surforigin = bsdorigin(bsdobject, setto000=setto000)
            simpleobject.Starting_X_Coordinate = surforigin[0]
            simpleobject.Starting_Y_Coordinate = surforigin[1]
            simpleobject.Starting_Z_Coordinate = surforigin[2]
            simpleobject.Length = bsdobject.width
            simpleobject.Height = bsdobject.height
            if deletebsd:
                idf.removeidfobject(bsdobject)
            return simpleobject
    return None


def roof(idf, bsdobject, deletebsd=True, setto000=False):
    """return an roof object if the bsd (buildingsurface:detailed) is
    a roof"""
    # ('ROOF', Roof, None or Outdoor)
    # test if it is aroof
    if bsdobject.Surface_Type.upper() == "ROOF":  # Surface_Type == roof
        if bsdobject.Outside_Boundary_Condition.upper() in (
            "OUTDOORS",
            "",
        ):  # Outside_Boundary_Condition == Outdoor
            simpleobject = idf.newidfobject("ROOF")
            simpleobject.Name = bsdobject.Name
            simpleobject.Construction_Name = bsdobject.Construction_Name
            simpleobject.Zone_Name = bsdobject.Zone_Name
            simpleobject.Azimuth_Angle = bsdobject.azimuth
            simpleobject.Tilt_Angle = bsdobject.tilt
            surforigin = bsdorigin(bsdobject, setto000=setto000)
            simpleobject.Starting_X_Coordinate = surforigin[0]
            simpleobject.Starting_Y_Coordinate = surforigin[1]
            simpleobject.Starting_Z_Coordinate = surforigin[2]
            simpleobject.Length = bsdobject.width
            simpleobject.Width = bsdobject.height
            if deletebsd:
                idf.removeidfobject(bsdobject)
            return simpleobject
    return None


def ceilingadiabatic(idf, bsdobject, deletebsd=True, setto000=False):
    """return a ceiling:adiabatic if bsdobject (buildingsurface:detailed) is an
    adiabatic ceiling"""
    # ('CEILING:ADIABATIC', Ceiling, Adiabatic)
    # test if it is an adiabatic ceiling
    if bsdobject.Surface_Type.upper() == "CEILING":  # Surface_Type == ceiling
        if (
            bsdobject.Outside_Boundary_Condition.upper() == "ADIABATIC"
        ):  # Outside_Boundary_Condition == Adiabatic
            simpleobject = idf.newidfobject("CEILING:ADIABATIC")
            simpleobject.Name = bsdobject.Name
            simpleobject.Construction_Name = bsdobject.Construction_Name
            simpleobject.Zone_Name = bsdobject.Zone_Name
            simpleobject.Azimuth_Angle = bsdobject.azimuth
            simpleobject.Tilt_Angle = bsdobject.tilt
            surforigin = bsdorigin(bsdobject, setto000=setto000)
            simpleobject.Starting_X_Coordinate = surforigin[0]
            simpleobject.Starting_Y_Coordinate = surforigin[1]
            simpleobject.Starting_Z_Coordinate = surforigin[2]
            simpleobject.Length = bsdobject.width
            simpleobject.Width = bsdobject.height
            if deletebsd:
                idf.removeidfobject(bsdobject)
            return simpleobject
    return None


# ('CEILING:INTERZONE', Ceiling, Surface OR Zone)
def ceilinginterzone(idf, bsdobject, deletebsd=True, setto000=False):
    """return an ceiling:interzone object if the bsd (buildingsurface:detailed)
    is an interzone ceiling"""
    # ('WALL:INTERZONE', Wall, Surface OR Zone OR OtherSideCoefficients)
    # test if it is an exterior wall
    if bsdobject.Surface_Type.upper() == "CEILING":  # Surface_Type == ceiling
        if bsdobject.Outside_Boundary_Condition.upper() in (
            "SURFACE",
            "ZONE",
            "OtherSideCoefficients".upper(),
        ):
            simpleobject = idf.newidfobject("CEILING:INTERZONE")
            simpleobject.Name = bsdobject.Name
            simpleobject.Construction_Name = bsdobject.Construction_Name
            simpleobject.Zone_Name = bsdobject.Zone_Name
            obco = "Outside_Boundary_Condition_Object"
            simpleobject[obco] = bsdobject[obco]
            simpleobject.Azimuth_Angle = bsdobject.azimuth
            simpleobject.Tilt_Angle = bsdobject.tilt
            surforigin = bsdorigin(bsdobject, setto000=setto000)
            simpleobject.Starting_X_Coordinate = surforigin[0]
            simpleobject.Starting_Y_Coordinate = surforigin[1]
            simpleobject.Starting_Z_Coordinate = surforigin[2]
            simpleobject.Length = bsdobject.width
            simpleobject.Width = bsdobject.height
            if deletebsd:
                idf.removeidfobject(bsdobject)
            return simpleobject
    return None


def floorgroundcontact(idf, bsdobject, deletebsd=True, setto000=False):
    """return a wall:adiabatic if bsdobject (buildingsurface:detailed) is an
    adibatic wall"""
    # ('FLOOR:GROUNDCONTACT', Floor, s.startswith('Ground'))
    # test if it is an underground wall
    if bsdobject.Surface_Type.upper() == "FLOOR":  # Surface_Type == wall
        if bsdobject.Outside_Boundary_Condition.upper().startswith(
            "GROUND"
        ):  # Outside_Boundary_Condition startswith 'ground'
            simpleobject = idf.newidfobject("FLOOR:GROUNDCONTACT")
            simpleobject.Name = bsdobject.Name
            simpleobject.Construction_Name = bsdobject.Construction_Name
            simpleobject.Zone_Name = bsdobject.Zone_Name
            simpleobject.Azimuth_Angle = bsdobject.azimuth
            simpleobject.Tilt_Angle = bsdobject.tilt
            surforigin = bsdorigin(bsdobject, setto000=setto000)
            simpleobject.Starting_X_Coordinate = surforigin[0]
            simpleobject.Starting_Y_Coordinate = surforigin[1]
            simpleobject.Starting_Z_Coordinate = surforigin[2]
            simpleobject.Length = bsdobject.width
            simpleobject.Width = bsdobject.height
            if deletebsd:
                idf.removeidfobject(bsdobject)
            return simpleobject
    return None


def flooradiabatic(idf, bsdobject, deletebsd=True, setto000=False):
    """return a floor:adiabatic if bsdobject (buildingsurface:detailed) is an
    adibatic floor"""
    # ('FLOOR:ADIABATIC', Floor, Adiabatic)
    # test if it is an adiabatic wall
    if bsdobject.Surface_Type.upper() == "FLOOR":  # Surface_Type == wall
        if (
            bsdobject.Outside_Boundary_Condition.upper() == "ADIABATIC"
        ):  # Outside_Boundary_Condition == Adiabatic
            simpleobject = idf.newidfobject("FLOOR:ADIABATIC")
            simpleobject.Name = bsdobject.Name
            simpleobject.Construction_Name = bsdobject.Construction_Name
            simpleobject.Zone_Name = bsdobject.Zone_Name
            simpleobject.Azimuth_Angle = bsdobject.azimuth
            simpleobject.Tilt_Angle = bsdobject.tilt
            surforigin = bsdorigin(bsdobject, setto000=setto000)
            simpleobject.Starting_X_Coordinate = surforigin[0]
            simpleobject.Starting_Y_Coordinate = surforigin[1]
            simpleobject.Starting_Z_Coordinate = surforigin[2]
            simpleobject.Length = bsdobject.width
            simpleobject.Width = bsdobject.height
            if deletebsd:
                idf.removeidfobject(bsdobject)
            return simpleobject
    return None


def floorinterzone(idf, bsdobject, deletebsd=True, setto000=False):
    """return an floor:interzone object if the bsd (buildingsurface:detailed)
    is an interaone floor"""
    # ('FLOOR:INTERZONE', Floor, Surface OR Zone OR OtherSideCoefficients)
    # test if it is an exterior wall
    if bsdobject.Surface_Type.upper() == "FLOOR":  # Surface_Type == wall
        if bsdobject.Outside_Boundary_Condition.upper() in (
            "SURFACE",
            "ZONE",
            "OtherSideCoefficients".upper(),
        ):
            simpleobject = idf.newidfobject("FLOOR:INTERZONE")
            simpleobject.Name = bsdobject.Name
            simpleobject.Construction_Name = bsdobject.Construction_Name
            simpleobject.Zone_Name = bsdobject.Zone_Name
            obco = "Outside_Boundary_Condition_Object"
            simpleobject[obco] = bsdobject[obco]
            simpleobject.Azimuth_Angle = bsdobject.azimuth
            simpleobject.Tilt_Angle = bsdobject.tilt
            surforigin = bsdorigin(bsdobject, setto000=setto000)
            simpleobject.Starting_X_Coordinate = surforigin[0]
            simpleobject.Starting_Y_Coordinate = surforigin[1]
            simpleobject.Starting_Z_Coordinate = surforigin[2]
            simpleobject.Length = bsdobject.width
            simpleobject.Width = bsdobject.height
            if deletebsd:
                idf.removeidfobject(bsdobject)
            return simpleobject
    return None


def window(idf, fsdobject, deletebsd=True, setto000=False):
    """return an window object if the fsd (fenestrationsurface:detailed) is
    a window"""
    # ('WINDOW',  Window, None)
    if fsdobject.Surface_Type.upper() == "WINDOW":  # Surface_Type == w
        simpleobject = idf.newidfobject("WINDOW")
        simpleobject.Name = fsdobject.Name
        simpleobject.Construction_Name = fsdobject.Construction_Name
        simpleobject.Building_Surface_Name = fsdobject.Building_Surface_Name
        simpleobject.Shading_Control_Name = fsdobject.Shading_Control_Name
        simpleobject.Frame_and_Divider_Name = fsdobject.Frame_and_Divider_Name
        simpleobject.Multiplier = fsdobject.Multiplier
        surforigin = fsdorigin(fsdobject, setto000=setto000)
        simpleobject.Starting_X_Coordinate = surforigin[0]
        simpleobject.Starting_Z_Coordinate = surforigin[1]
        simpleobject.Length = fsdobject.width
        simpleobject.Height = fsdobject.height
        if deletebsd:
            idf.removeidfobject(fsdobject)
        return simpleobject
    return None


def door(idf, fsdobject, deletebsd=True, setto000=False):
    """return an door object if the fsd (fenestrationsurface:detailed) is
    a door"""
    # ('DOOR', Door, None)
    # test if it is aroof
    if fsdobject.Surface_Type.upper() == "DOOR":  # Surface_Type == w
        simpleobject = idf.newidfobject("DOOR")
        simpleobject.Name = fsdobject.Name
        simpleobject.Construction_Name = fsdobject.Construction_Name
        simpleobject.Building_Surface_Name = fsdobject.Building_Surface_Name
        simpleobject.Multiplier = fsdobject.Multiplier
        surforigin = fsdorigin(fsdobject, setto000=setto000)
        simpleobject.Starting_X_Coordinate = surforigin[0]
        simpleobject.Starting_Z_Coordinate = surforigin[1]
        simpleobject.Length = fsdobject.width
        simpleobject.Height = fsdobject.height
        if deletebsd:
            idf.removeidfobject(fsdobject)
        return simpleobject
    return None


def glazeddoor(idf, fsdobject, deletebsd=True, setto000=False):
    """return an glazeddoor object if the fsd (fenestrationsurface:detailed) is
    a glassdoor"""
    # ('WINDOW',  glassdoor, None)
    # test if it is glassdoor
    if fsdobject.Surface_Type.upper() == "GLASSDOOR":
        simpleobject = idf.newidfobject("GLAZEDDOOR")
        simpleobject.Name = fsdobject.Name
        simpleobject.Construction_Name = fsdobject.Construction_Name
        simpleobject.Building_Surface_Name = fsdobject.Building_Surface_Name
        simpleobject.Shading_Control_Name = fsdobject.Shading_Control_Name
        simpleobject.Frame_and_Divider_Name = fsdobject.Frame_and_Divider_Name
        simpleobject.Multiplier = fsdobject.Multiplier
        surforigin = fsdorigin(fsdobject, setto000=setto000)
        simpleobject.Starting_X_Coordinate = surforigin[0]
        simpleobject.Starting_Z_Coordinate = surforigin[1]
        simpleobject.Length = fsdobject.width
        simpleobject.Height = fsdobject.height
        if deletebsd:
            idf.removeidfobject(fsdobject)
        return simpleobject
    return None


def simplesurface(idf, bsd, deletebsd=True, setto000=False):
    """convert a bsd (buildingsurface:detailed) into a simple surface"""
    funcs = (
        wallexterior,
        walladiabatic,
        wallunderground,
        wallinterzone,
        roof,
        ceilingadiabatic,
        ceilinginterzone,
        floorgroundcontact,
        flooradiabatic,
        floorinterzone,
    )
    for func in funcs:
        surface = func(idf, bsd, deletebsd=deletebsd, setto000=setto000)
        if surface:
            return surface
    return None


def simplefenestration(idf, fsd, deletebsd=True, setto000=False):
    """convert a bsd (fenestrationsurface:detailed) into a simple
    fenestrations"""
    funcs = (window, door, glazeddoor)
    for func in funcs:
        fenestration = func(idf, fsd, deletebsd=deletebsd, setto000=setto000)
        if fenestration:
            return fenestration
    return None
