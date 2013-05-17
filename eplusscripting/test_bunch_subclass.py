# Copyright (c) 2012 Santosh Phillip

# This file is part of eppy.

# Eppy is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# Eppy is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with eppy.  If not, see <http://www.gnu.org/licenses/>.

"""py.test for bunch_subclass"""

# This test is ugly because I have to send file names and not able to send file handles
import os
import pytest
from EPlusInterfaceFunctions import readidf
import bunchhelpers
import bunch_subclass
EpBunch = bunch_subclass.EpBunch

# This test is ugly because I have to send file names and not able to send file handles
iddtxt = """!IDD_Version 6.0.0.023
! **************************************************************************

Version,
      \\unique-object
      \\format singleLine
  A1 ; \\field Version Identifier
      \\required-field
      \\default 5.0

BuildingSurface:Detailed,
  \\extensible:3 -- duplicate last set of x,y,z coordinates (last 3 fields), remembering to remove ; from "inner" fields.
  \\format vertices
  A1 , \\field Name
       \\required-field
       \\type alpha
       \\reference SurfaceNames
       \\reference SurfAndSubSurfNames
       \\reference AllHeatTranSurfNames
       \\reference HeatTranBaseSurfNames
       \\reference OutFaceEnvNames
       \\reference AllHeatTranAngFacNames
       \\reference RadGroupAndSurfNames
       \\reference SurfGroupAndHTSurfNames
       \\reference AllShadingAndHTSurfNames
  A2 , \\field Surface Type
       \\required-field
       \\type choice
       \\key Floor
       \\key Wall
       \\key Ceiling
       \\key Roof
  A3 , \\field Construction Name
       \\required-field
       \\note To be matched with a construction in this input file
       \\type object-list
       \\object-list ConstructionNames
  A4 , \\field Zone Name
       \\required-field
       \\note Zone the surface is a part of
       \\type object-list
       \\object-list ZoneNames
  A5 , \\field Outside Boundary Condition
       \\required-field
       \\type choice
       \\key Adiabatic
       \\key Surface
       \\key Zone
       \\key Outdoors
       \\key Ground
       \\key GroundFCfactorMethod
       \\key OtherSideCoefficients
       \\key OtherSideConditionsModel
       \\key GroundSlabPreprocessorAverage
       \\key GroundSlabPreprocessorCore
       \\key GroundSlabPreprocessorPerimeter
       \\key GroundBasementPreprocessorAverageWall
       \\key GroundBasementPreprocessorAverageFloor
       \\key GroundBasementPreprocessorUpperWall
       \\key GroundBasementPreprocessorLowerWall
  A6,  \\field Outside Boundary Condition Object
       \\type object-list
       \\object-list OutFaceEnvNames
       \\note Non-blank only if the field Outside Boundary Condition is Surface,
       \\note Zone, OtherSideCoefficients or OtherSideConditionsModel
       \\note If Surface, specify name of corresponding surface in adjacent zone or
       \\note specify current surface name for internal partition separating like zones
       \\note If Zone, specify the name of the corresponding zone and
       \\note the program will generate the corresponding interzone surface
       \\note If OtherSideCoefficients, specify name of SurfaceProperty:OtherSideCoefficients
       \\note If OtherSideConditionsModel, specify name of SurfaceProperty:OtherSideConditionsModel
  A7 , \\field Sun Exposure
       \\required-field
       \\type choice
       \\key SunExposed
       \\key NoSun
       \\default SunExposed
  A8,  \\field Wind Exposure
       \\required-field
       \\type choice
       \\key WindExposed
       \\key NoWind
       \\default WindExposed
  N1,  \\field View Factor to Ground
       \\type real
       \\note From the exterior of the surface
       \\note Unused if one uses the "reflections" options in Solar Distribution in Building input
       \\note unless a DaylightingDevice:Shelf or DaylightingDevice:Tubular object has been specified.
       \\note autocalculate will automatically calculate this value from the tilt of the surface
       \\autocalculatable
       \\minimum 0.0
       \\maximum 1.0
       \\default autocalculate
  N2 , \\field Number of Vertices
       \\note shown with 120 vertex coordinates -- extensible object
       \\note  "extensible" -- duplicate last set of x,y,z coordinates (last 3 fields),
       \\note remembering to remove ; from "inner" fields.
       \\note for clarity in any error messages, renumber the fields as well.
       \\note (and changing z terminator to a comma "," for all but last one which needs a semi-colon ";")
       \\autocalculatable
       \\minimum 3
       \\default autocalculate
       \\note vertices are given in GlobalGeometryRules coordinates -- if relative, all surface coordinates
       \\note are "relative" to the Zone Origin.  If world, then building and zone origins are used
       \\note for some internal calculations, but all coordinates are given in an "absolute" system.
  N3,  \\field Vertex 1 X-coordinate
       \\begin-extensible
       \\units m
       \\type real
  N4 , \\field Vertex 1 Y-coordinate
       \\units m
       \\type real
  N5 , \\field Vertex 1 Z-coordinate
       \\units m
       \\type real
  N6,  \\field Vertex 2 X-coordinate
       \\units m
       \\type real
  N7,  \\field Vertex 2 Y-coordinate
       \\units m
       \\type real
  N8,  \\field Vertex 2 Z-coordinate
       \\units m
       \\type real
  N9,  \\field Vertex 3 X-coordinate
       \\units m
       \\type real
  N10, \\field Vertex 3 Y-coordinate
       \\units m
       \\type real
  N11, \\field Vertex 3 Z-coordinate
       \\units m
       \\type real
  N12, \\field Vertex 4 X-coordinate
       \\units m
       \\type real
  N13, \\field Vertex 4 Y-coordinate
       \\type real
       \\units m
  N14; \\field Vertex 4 Z-coordinate
       \\units m
       \\type real

FenestrationSurface:Detailed,
       \\min-fields 19
       \\memo Used for windows, doors, glass doors, tubular daylighting devices
       \\format vertices
  A1 , \\field Name
       \\required-field
       \\type alpha
       \\reference SubSurfNames
       \\reference SurfAndSubSurfNames
       \\reference AllHeatTranSurfNames
       \\reference OutFaceEnvNames
       \\reference AllHeatTranAngFacNames
       \\reference RadGroupAndSurfNames
       \\reference SurfGroupAndHTSurfNames
       \\reference AllShadingAndHTSurfNames
  A2 , \\field Surface Type
       \\required-field
       \\type choice
       \\key Window
       \\key Door
       \\key GlassDoor
       \\key TubularDaylightDome
       \\key TubularDaylightDiffuser
  A3 , \\field Construction Name
       \\required-field
       \\note To be matched with a construction in this input file
       \\type object-list
       \\object-list ConstructionNames
  A4 , \\field Building Surface Name
       \\required-field
       \\type object-list
       \\object-list SurfaceNames
  A5,  \\field Outside Boundary Condition Object
       \\type object-list
       \\object-list OutFaceEnvNames
       \\note Non-blank only if base surface field Outside Boundary Condition is
       \\note Surface or OtherSideCoefficients
       \\note If Base Surface's Surface, specify name of corresponding subsurface in adjacent zone or
       \\note specify current subsurface name for internal partition separating like zones
       \\note If OtherSideCoefficients, specify name of SurfaceProperty:OtherSideCoefficients
       \\note  or leave blank to inherit Base Surface's OtherSide Coefficients
  N1, \\field View Factor to Ground
       \\type real
       \\note From the exterior of the surface
       \\note Unused if one uses the "reflections" options in Solar Distribution in Building input
       \\note unless a DaylightingDevice:Shelf or DaylightingDevice:Tubular object has been specified.
       \\note autocalculate will automatically calculate this value from the tilt of the surface
       \\autocalculatable
       \\minimum 0.0
       \\maximum 1.0
       \\default autocalculate
  A6, \\field Shading Control Name
       \\note enter the name of a WindowProperty:ShadingControl object
       \\type object-list
       \\object-list WindowShadeControlNames
       \\note used for windows and glass doors only
       \\note If not specified, window or glass door has no shading (blind, roller shade, etc.)
  A7, \\field Frame and Divider Name
       \\note Enter the name of a WindowProperty:FrameAndDivider object
       \\type object-list
       \\object-list WindowFrameAndDividerNames
       \\note Used only for exterior windows (rectangular) and glass doors.
       \\note Unused for triangular windows.
       \\note If not specified (blank), window or glass door has no frame or divider
       \\note and no beam solar reflection from reveal surfaces.
  N2 , \\field Multiplier
       \\note Used only for Surface Type = WINDOW, GLASSDOOR or DOOR
       \\note Non-integer values will be truncated to integer
       \\default 1.0
       \\minimum 1.0
  N3 , \\field Number of Vertices
       \\minimum 3
       \\maximum 4
       \\autocalculatable
       \\default autocalculate
       \\note vertices are given in GlobalGeometryRules coordinates -- if relative, all surface coordinates
       \\note are "relative" to the Zone Origin.  If world, then building and zone origins are used
       \\note for some internal calculations, but all coordinates are given in an "absolute" system.
  N4,  \\field Vertex 1 X-coordinate
       \\units m
       \\type real
  N5 , \\field Vertex 1 Y-coordinate
       \\units m
       \\type real
  N6 , \\field Vertex 1 Z-coordinate
       \\units m
       \\type real
  N7,  \\field Vertex 2 X-coordinate
       \\units m
       \\type real
  N8,  \\field Vertex 2 Y-coordinate
       \\units m
       \\type real
  N9,  \\field Vertex 2 Z-coordinate
       \\units m
       \\type real
  N10,  \\field Vertex 3 X-coordinate
       \\units m
       \\type real
  N11, \\field Vertex 3 Y-coordinate
       \\units m
       \\type real
  N12, \\field Vertex 3 Z-coordinate
       \\units m
       \\type real
  N13, \\field Vertex 4 X-coordinate
       \\units m
       \\type real
       \\note Not used for triangles
  N14, \\field Vertex 4 Y-coordinate
       \\type real
       \\units m
       \\note Not used for triangles
  N15; \\field Vertex 4 Z-coordinate
       \\units m
       \\type real
       \\note Not used for triangles

Construction,
       \\memo Start with outside layer and work your way to the inside layer
       \\memo Up to 10 layers total, 8 for windows
       \\memo Enter the material name for each layer
  A1 , \\field Name
       \\required-field
       \\type alpha
       \\reference ConstructionNames
  A2 , \\field Outside Layer
       \\required-field
       \\type object-list
       \\object-list MaterialName
  A3 , \\field Layer 2
       \\type object-list
       \\object-list MaterialName
  A4 , \\field Layer 3
       \\type object-list
       \\object-list MaterialName
  A5 , \\field Layer 4
       \\type object-list
       \\object-list MaterialName
  A6 , \\field Layer 5
       \\type object-list
       \\object-list MaterialName
  A7 , \\field Layer 6
       \\type object-list
       \\object-list MaterialName
  A8 , \\field Layer 7
       \\type object-list
       \\object-list MaterialName
  A9 , \\field Layer 8
       \\type object-list
       \\object-list MaterialName
  A10, \\field Layer 9
       \\type object-list
       \\object-list MaterialName
  A11; \\field Layer 10
       \\type object-list
       \\object-list MaterialName

"""

idftxt = """Version,
    6.0;

BuildingSurface:Detailed,
  Zn001:Wall001,           !- Name
  Wall,                    !- Surface Type
  EXTWALL80,               !- Construction Name
  West Zone,               !- Zone Name
  Outdoors,                !- Outside Boundary Condition
  ,                        !- Outside Boundary Condition Object
  SunExposed,              !- Sun Exposure
  WindExposed,             !- Wind Exposure
  0.5000000,               !- View Factor to Ground
  4,                       !- Number of Vertices
  0,0,3.048000,  !- X,Y,Z ==> Vertex 1 {m}
  0,0,0,  !- X,Y,Z ==> Vertex 2 {m}
  6.096000,0,0,  !- X,Y,Z ==> Vertex 3 {m}
  6.096000,0,3.048000;  !- X,Y,Z ==> Vertex 4 {m}

FenestrationSurface:Detailed,
  Zn001:Wall001:Win001,    !- Name
  Window,                  !- Surface Type
  WIN-CON-LIGHT,           !- Construction Name
  Zn001:Wall001,           !- Building Surface Name
  ,                        !- Outside Boundary Condition Object
  0.5000000,               !- View Factor to Ground
  ,                        !- Shading Control Name
  ,                        !- Frame and Divider Name
  1.0,                     !- Multiplier
  4,                       !- Number of Vertices
  0.548000,0,2.5000,  !- X,Y,Z ==> Vertex 1 {m}
  0.548000,0,0.5000,  !- X,Y,Z ==> Vertex 2 {m}
  5.548000,0,0.5000,  !- X,Y,Z ==> Vertex 3 {m}
  5.548000,0,2.5000;  !- X,Y,Z ==> Vertex 4 {m}

BuildingSurface:Detailed,
  Zn001:Wall002,           !- Name
  Wall,                    !- Surface Type
  EXTWALL80,               !- Construction Name
  West Zone,               !- Zone Name
  Outdoors,                !- Outside Boundary Condition
  ,                        !- Outside Boundary Condition Object
  SunExposed,              !- Sun Exposure
  WindExposed,             !- Wind Exposure
  0.5000000,               !- View Factor to Ground
  4,                       !- Number of Vertices
  0,6.096000,3.048000,  !- X,Y,Z ==> Vertex 1 {m}
  0,6.096000,0,  !- X,Y,Z ==> Vertex 2 {m}
  0,0,0,  !- X,Y,Z ==> Vertex 3 {m}
  0,0,3.048000;  !- X,Y,Z ==> Vertex 4 {m}

BuildingSurface:Detailed,
  Zn001:Wall003,           !- Name
  Wall,                    !- Surface Type
  PARTITION06,             !- Construction Name
  West Zone,               !- Zone Name
  Surface,                 !- Outside Boundary Condition
  Zn003:Wall004,           !- Outside Boundary Condition Object
  NoSun,                   !- Sun Exposure
  NoWind,                  !- Wind Exposure
  0.5000000,               !- View Factor to Ground
  4,                       !- Number of Vertices
  6.096000,6.096000,3.048000,  !- X,Y,Z ==> Vertex 1 {m}
  6.096000,6.096000,0,  !- X,Y,Z ==> Vertex 2 {m}
  0,6.096000,0,  !- X,Y,Z ==> Vertex 3 {m}
  0,6.096000,3.048000;  !- X,Y,Z ==> Vertex 4 {m}

BuildingSurface:Detailed,
  Zn001:Wall004,           !- Name
  Wall,                    !- Surface Type
  PARTITION06,             !- Construction Name
  West Zone,               !- Zone Name
  Surface,                 !- Outside Boundary Condition
  Zn002:Wall004,           !- Outside Boundary Condition Object
  NoSun,                   !- Sun Exposure
  NoWind,                  !- Wind Exposure
  0.5000000,               !- View Factor to Ground
  4,                       !- Number of Vertices
  6.096000,0,3.048000,  !- X,Y,Z ==> Vertex 1 {m}
  6.096000,0,0,  !- X,Y,Z ==> Vertex 2 {m}
  6.096000,6.096000,0,  !- X,Y,Z ==> Vertex 3 {m}
  6.096000,6.096000,3.048000;  !- X,Y,Z ==> Vertex 4 {m}

BuildingSurface:Detailed,
  Zn001:Flr001,            !- Name
  Floor,                   !- Surface Type
  FLOOR SLAB 8 IN,         !- Construction Name
  West Zone,               !- Zone Name
  Surface,                 !- Outside Boundary Condition
  Zn001:Flr001,            !- Outside Boundary Condition Object
  NoSun,                   !- Sun Exposure
  NoWind,                  !- Wind Exposure
  1.000000,                !- View Factor to Ground
  4,                       !- Number of Vertices
  0,0,0,  !- X,Y,Z ==> Vertex 1 {m}
  0,6.096000,0,  !- X,Y,Z ==> Vertex 2 {m}
  6.096000,6.096000,0,  !- X,Y,Z ==> Vertex 3 {m}
  6.096000,0,0;  !- X,Y,Z ==> Vertex 4 {m}

BuildingSurface:Detailed,
  Zn001:Roof001,           !- Name
  Roof,                    !- Surface Type
  ROOF34,                  !- Construction Name
  West Zone,               !- Zone Name
  Outdoors,                !- Outside Boundary Condition
  ,                        !- Outside Boundary Condition Object
  SunExposed,              !- Sun Exposure
  WindExposed,             !- Wind Exposure
  0,                       !- View Factor to Ground
  4,                       !- Number of Vertices
  0,6.096000,3.048000,  !- X,Y,Z ==> Vertex 1 {m}
  0,0,3.048000,  !- X,Y,Z ==> Vertex 2 {m}
  6.096000,0,3.048000,  !- X,Y,Z ==> Vertex 3 {m}
  6.096000,6.096000,3.048000;  !- X,Y,Z ==> Vertex 4 {m}

BuildingSurface:Detailed,
  Zn002:Wall001,           !- Name
  Wall,                    !- Surface Type
  EXTWALL80,               !- Construction Name
  EAST ZONE,               !- Zone Name
  Outdoors,                !- Outside Boundary Condition
  ,                        !- Outside Boundary Condition Object
  SunExposed,              !- Sun Exposure
  WindExposed,             !- Wind Exposure
  0.5000000,               !- View Factor to Ground
  4,                       !- Number of Vertices
  12.19200,6.096000,3.048000,  !- X,Y,Z ==> Vertex 1 {m}
  12.19200,6.096000,0,  !- X,Y,Z ==> Vertex 2 {m}
  9.144000,6.096000,0,  !- X,Y,Z ==> Vertex 3 {m}
  9.144000,6.096000,3.048000;  !- X,Y,Z ==> Vertex 4 {m}

BuildingSurface:Detailed,
  Zn002:Wall002,           !- Name
  Wall,                    !- Surface Type
  EXTWALL80,               !- Construction Name
  EAST ZONE,               !- Zone Name
  Outdoors,                !- Outside Boundary Condition
  ,                        !- Outside Boundary Condition Object
  SunExposed,              !- Sun Exposure
  WindExposed,             !- Wind Exposure
  0.5000000,               !- View Factor to Ground
  4,                       !- Number of Vertices
  6.096000,0,3.048000,  !- X,Y,Z ==> Vertex 1 {m}
  6.096000,0,0,  !- X,Y,Z ==> Vertex 2 {m}
  12.19200,0,0,  !- X,Y,Z ==> Vertex 3 {m}
  12.19200,0,3.048000;  !- X,Y,Z ==> Vertex 4 {m}

BuildingSurface:Detailed,
  Zn002:Wall003,           !- Name
  Wall,                    !- Surface Type
  EXTWALL80,               !- Construction Name
  EAST ZONE,               !- Zone Name
  Outdoors,                !- Outside Boundary Condition
  ,                        !- Outside Boundary Condition Object
  SunExposed,              !- Sun Exposure
  WindExposed,             !- Wind Exposure
  0.5000000,               !- View Factor to Ground
  4,                       !- Number of Vertices
  12.19200,0,3.048000,  !- X,Y,Z ==> Vertex 1 {m}
  12.19200,0,0,  !- X,Y,Z ==> Vertex 2 {m}
  12.19200,6.096000,0,  !- X,Y,Z ==> Vertex 3 {m}
  12.19200,6.096000,3.048000;  !- X,Y,Z ==> Vertex 4 {m}

BuildingSurface:Detailed,
  Zn002:Wall004,           !- Name
  Wall,                    !- Surface Type
  PARTITION06,             !- Construction Name
  EAST ZONE,               !- Zone Name
  Surface,                 !- Outside Boundary Condition
  Zn001:Wall004,           !- Outside Boundary Condition Object
  NoSun,                   !- Sun Exposure
  NoWind,                  !- Wind Exposure
  0.5000000,               !- View Factor to Ground
  4,                       !- Number of Vertices
  6.096000,6.096000,3.048000,  !- X,Y,Z ==> Vertex 1 {m}
  6.096000,6.096000,0,  !- X,Y,Z ==> Vertex 2 {m}
  6.096000,0,0,  !- X,Y,Z ==> Vertex 3 {m}
  6.096000,0,3.048000;  !- X,Y,Z ==> Vertex 4 {m}

BuildingSurface:Detailed,
  Zn002:Wall005,           !- Name
  Wall,                    !- Surface Type
  PARTITION06,             !- Construction Name
  EAST ZONE,               !- Zone Name
  Surface,                 !- Outside Boundary Condition
  Zn003:Wall005,           !- Outside Boundary Condition Object
  NoSun,                   !- Sun Exposure
  NoWind,                  !- Wind Exposure
  0.5000000,               !- View Factor to Ground
  4,                       !- Number of Vertices
  9.144000,6.096000,3.048000,  !- X,Y,Z ==> Vertex 1 {m}
  9.144000,6.096000,0,  !- X,Y,Z ==> Vertex 2 {m}
  6.096000,6.096000,0,  !- X,Y,Z ==> Vertex 3 {m}
  6.096000,6.096000,3.048000;  !- X,Y,Z ==> Vertex 4 {m}

BuildingSurface:Detailed,
  Zn002:Flr001,            !- Name
  Floor,                   !- Surface Type
  FLOOR SLAB 8 IN,         !- Construction Name
  EAST ZONE,               !- Zone Name
  Surface,                 !- Outside Boundary Condition
  Zn002:Flr001,            !- Outside Boundary Condition Object
  NoSun,                   !- Sun Exposure
  NoWind,                  !- Wind Exposure
  1.000000,                !- View Factor to Ground
  4,                       !- Number of Vertices
  6.096000,0,0,  !- X,Y,Z ==> Vertex 1 {m}
  6.096000,6.096000,0,  !- X,Y,Z ==> Vertex 2 {m}
  12.19200,6.096000,0,  !- X,Y,Z ==> Vertex 3 {m}
  12.19200,0,0;  !- X,Y,Z ==> Vertex 4 {m}

BuildingSurface:Detailed,
  Zn002:Roof001,           !- Name
  Roof,                    !- Surface Type
  ROOF34,                  !- Construction Name
  EAST ZONE,               !- Zone Name
  Outdoors,                !- Outside Boundary Condition
  ,                        !- Outside Boundary Condition Object
  SunExposed,              !- Sun Exposure
  WindExposed,             !- Wind Exposure
  0,                       !- View Factor to Ground
  4,                       !- Number of Vertices
  6.096000,6.096000,3.048000,  !- X,Y,Z ==> Vertex 1 {m}
  6.096000,0,3.048000,  !- X,Y,Z ==> Vertex 2 {m}
  12.19200,0,3.048000,  !- X,Y,Z ==> Vertex 3 {m}
  12.19200,6.096000,3.048000;  !- X,Y,Z ==> Vertex 4 {m}

BuildingSurface:Detailed,
  Zn003:Wall001,           !- Name
  Wall,                    !- Surface Type
  EXTWALL80,               !- Construction Name
  NORTH ZONE,              !- Zone Name
  Outdoors,                !- Outside Boundary Condition
  ,                        !- Outside Boundary Condition Object
  SunExposed,              !- Sun Exposure
  WindExposed,             !- Wind Exposure
  0.5000000,               !- View Factor to Ground
  4,                       !- Number of Vertices
  0,12.19200,3.048000,  !- X,Y,Z ==> Vertex 1 {m}
  0,12.19200,0,  !- X,Y,Z ==> Vertex 2 {m}
  0,6.096000,0,  !- X,Y,Z ==> Vertex 3 {m}
  0,6.096000,3.048000;  !- X,Y,Z ==> Vertex 4 {m}

BuildingSurface:Detailed,
  Zn003:Wall002,           !- Name
  Wall,                    !- Surface Type
  EXTWALL80,               !- Construction Name
  NORTH ZONE,              !- Zone Name
  Outdoors,                !- Outside Boundary Condition
  ,                        !- Outside Boundary Condition Object
  SunExposed,              !- Sun Exposure
  WindExposed,             !- Wind Exposure
  0.5000000,               !- View Factor to Ground
  4,                       !- Number of Vertices
  9.144000,12.19200,3.048000,  !- X,Y,Z ==> Vertex 1 {m}
  9.144000,12.19200,0,  !- X,Y,Z ==> Vertex 2 {m}
  0,12.19200,0,  !- X,Y,Z ==> Vertex 3 {m}
  0,12.19200,3.048000;  !- X,Y,Z ==> Vertex 4 {m}

BuildingSurface:Detailed,
  Zn003:Wall003,           !- Name
  Wall,                    !- Surface Type
  EXTWALL80,               !- Construction Name
  NORTH ZONE,              !- Zone Name
  Outdoors,                !- Outside Boundary Condition
  ,                        !- Outside Boundary Condition Object
  SunExposed,              !- Sun Exposure
  WindExposed,             !- Wind Exposure
  0.5000000,               !- View Factor to Ground
  4,                       !- Number of Vertices
  9.144000,6.096000,3.048000,  !- X,Y,Z ==> Vertex 1 {m}
  9.144000,6.096000,0,  !- X,Y,Z ==> Vertex 2 {m}
  9.144000,12.19200,0,  !- X,Y,Z ==> Vertex 3 {m}
  9.144000,12.19200,3.048000;  !- X,Y,Z ==> Vertex 4 {m}

BuildingSurface:Detailed,
  Zn003:Wall004,           !- Name
  Wall,                    !- Surface Type
  PARTITION06,             !- Construction Name
  NORTH ZONE,              !- Zone Name
  Surface,                 !- Outside Boundary Condition
  Zn001:Wall003,           !- Outside Boundary Condition Object
  NoSun,                   !- Sun Exposure
  NoWind,                  !- Wind Exposure
  0.5000000,               !- View Factor to Ground
  4,                       !- Number of Vertices
  0,6.096000,3.048000,  !- X,Y,Z ==> Vertex 1 {m}
  0,6.096000,0,  !- X,Y,Z ==> Vertex 2 {m}
  6.096000,6.096000,0,  !- X,Y,Z ==> Vertex 3 {m}
  6.096000,6.096000,3.048000;  !- X,Y,Z ==> Vertex 4 {m}

BuildingSurface:Detailed,
  Zn003:Wall005,           !- Name
  Wall,                    !- Surface Type
  PARTITION06,             !- Construction Name
  NORTH ZONE,              !- Zone Name
  Surface,                 !- Outside Boundary Condition
  Zn002:Wall005,           !- Outside Boundary Condition Object
  NoSun,                   !- Sun Exposure
  NoWind,                  !- Wind Exposure
  0.5000000,               !- View Factor to Ground
  4,                       !- Number of Vertices
  6.096000,6.096000,3.048000,  !- X,Y,Z ==> Vertex 1 {m}
  6.096000,6.096000,0,  !- X,Y,Z ==> Vertex 2 {m}
  9.144000,6.096000,0,  !- X,Y,Z ==> Vertex 3 {m}
  9.144000,6.096000,3.048000;  !- X,Y,Z ==> Vertex 4 {m}

BuildingSurface:Detailed,
  Zn003:Flr001,            !- Name
  Floor,                   !- Surface Type
  FLOOR SLAB 8 IN,         !- Construction Name
  NORTH ZONE,              !- Zone Name
  Surface,                 !- Outside Boundary Condition
  Zn003:Flr001,            !- Outside Boundary Condition Object
  NoSun,                   !- Sun Exposure
  NoWind,                  !- Wind Exposure
  1.000000,                !- View Factor to Ground
  4,                       !- Number of Vertices
  0,6.096000,0,  !- X,Y,Z ==> Vertex 1 {m}
  0,12.19200,0,  !- X,Y,Z ==> Vertex 2 {m}
  9.144000,12.19200,0,  !- X,Y,Z ==> Vertex 3 {m}
  9.144000,6.096000,0;  !- X,Y,Z ==> Vertex 4 {m}

BuildingSurface:Detailed,
  Zn003:Roof001,           !- Name
  Roof,                    !- Surface Type
  ROOF34,                  !- Construction Name
  NORTH ZONE,              !- Zone Name
  Outdoors,                !- Outside Boundary Condition
  ,                        !- Outside Boundary Condition Object
  SunExposed,              !- Sun Exposure
  WindExposed,             !- Wind Exposure
  0,                       !- View Factor to Ground
  4,                       !- Number of Vertices
  0,12.19200,3.048000,  !- X,Y,Z ==> Vertex 1 {m}
  0,6.096000,3.048000,  !- X,Y,Z ==> Vertex 2 {m}
  9.144000,6.096000,3.048000,  !- X,Y,Z ==> Vertex 3 {m}
  9.144000,12.19200,3.048000;  !- X,Y,Z ==> Vertex 4 {m}

  Construction,
    Dbl Clr 3mm/13mm Air,    !- Name
    CLEAR 3MM,               !- Outside Layer
    AIR 13MM,                !- Layer 2
    CLEAR 3MM;               !- Layer 3
"""

import random

def test_EpBunch():
    """py.test for EpBunch"""
    iddfile = "./walls%s.idd" % (random.randint(11111, 99999))
    fname = "./walls%s.idf" % (random.randint(11111, 99999))
    open(iddfile, 'wb').write(iddtxt)
    open(fname, 'wb').write(idftxt)
    # iddfile = "./walls.idd"
    # iddfile = "../iddfiles/Energy+V6_0.idd"
    # fname = "./walls.idf" # small file with only surfaces
    data, commdct = readidf.readdatacommdct(fname, iddfile=iddfile)

    # setup code walls - can be generic for any object
    dt = data.dt
    dtls = data.dtls
    wall_i = dtls.index('BuildingSurface:Detailed'.upper())
    wallkey = 'BuildingSurface:Detailed'.upper()

    dwalls = dt[wallkey]
    dwall = dwalls[0]

    wallfields = [comm.get('field') for comm in commdct[wall_i]]
    wallfields[0] = ['key']
    wallfields = [field[0] for field in wallfields]
    wall_fields = [bunchhelpers.makefieldname(field) for field in wallfields]
    # print wall_fields[:20]
    assert wall_fields[:20] == ['key', 'Name', 'Surface_Type', 'Construction_Name', 'Zone_Name', 'Outside_Boundary_Condition', 'Outside_Boundary_Condition_Object', 'Sun_Exposure', 'Wind_Exposure', 'View_Factor_to_Ground', 'Number_of_Vertices', 'Vertex_1_Xcoordinate', 'Vertex_1_Ycoordinate', 'Vertex_1_Zcoordinate', 'Vertex_2_Xcoordinate', 'Vertex_2_Ycoordinate', 'Vertex_2_Zcoordinate', 'Vertex_3_Xcoordinate', 'Vertex_3_Ycoordinate', 'Vertex_3_Zcoordinate']
    

    bwall = EpBunch(dwall, wall_fields)

    # print bwall.Name
    # print data.dt[wallkey][0][1]
    assert bwall.Name == data.dt[wallkey][0][1]
    bwall.Name = 'Gumby'
    # print bwall.Name
    # print data.dt[wallkey][0][1]
    # print
    assert bwall.Name == data.dt[wallkey][0][1]

    # set aliases
    bwall.__aliases = {'Constr':'Construction_Name'} 

    # print "wall.Construction_Name = %s" % (bwall.Construction_Name, )
    # print "wall.Constr = %s" % (bwall.Constr, )
    # print
    assert bwall.Construction_Name == bwall.Constr
    # print "change wall.Constr"
    bwall.Constr = 'AnewConstr'
    # print "wall.Constr = %s" % (bwall.Constr, )
    # print "wall.Constr = %s" % (data.dt[wallkey][0][3], )
    # print
    assert bwall.Constr == data.dt[wallkey][0][3]

    # add functions
    bwall.__functions = {'svalues':bunch_subclass.somevalues} 

    # print bwall.svalues
    assert bwall.svalues == ('Gumby', 'AnewConstr', ['BuildingSurface:Detailed', 'Gumby', 'Wall', 'AnewConstr', 'West Zone', 'Outdoors', '', 'SunExposed', 'WindExposed', '0.5000000', '4', '0', '0', '3.048000', '0', '0', '0', '6.096000', '0', '0', '6.096000', '0', '3.048000'])
    
    # print bwall.__functions
    
    # test __getitem__
    assert bwall["Name"] == data.dt[wallkey][0][1]
    # test __setitem__
    newname = "loofah"
    bwall["Name"] = newname
    assert bwall.Name == newname
    assert bwall["Name"] == newname
    assert data.dt[wallkey][0][1] == newname
    # test functions and alias again
    assert bwall.Constr == data.dt[wallkey][0][3]
    assert bwall.svalues == (newname, 'AnewConstr', ['BuildingSurface:Detailed', newname, 'Wall', 'AnewConstr', 'West Zone', 'Outdoors', '', 'SunExposed', 'WindExposed', '0.5000000', '4', '0', '0', '3.048000', '0', '0', '0', '6.096000', '0', '0', '6.096000', '0', '3.048000'])
    # test bunch_subclass.BadEPFieldError
    with pytest.raises(bunch_subclass.BadEPFieldError):
        bwall.Name_atypo = "newname"
    with pytest.raises(bunch_subclass.BadEPFieldError):
        thename = bwall.Name_atypo
    with pytest.raises(bunch_subclass.BadEPFieldError):
        bwall["Name_atypo"] = "newname"
    with pytest.raises(bunch_subclass.BadEPFieldError):
        thename = bwall["Name_atypo"]

    # test where constr["obj"] has to be extended
    # more items are added to an extendible field
    constr_i = dtls.index('Construction'.upper())
    constrkey = 'Construction'.upper()
    dconstrs = dt[constrkey]
    dconstr = dconstrs[0]
    constrfields = [comm.get('field') for comm in commdct[constr_i]]
    constrfields[0] = ['key']
    constrfields = [field[0] for field in constrfields]
    constr_fields = [bunchhelpers.makefieldname(field) for field in constrfields]
    bconstr = EpBunch(dconstr, constr_fields)
    assert bconstr.Name == "Dbl Clr 3mm/13mm Air"
    bconstr.Layer_4 = "butter"
    assert bconstr.obj == ['Construction', 'Dbl Clr 3mm/13mm Air', 'CLEAR 3MM', 'AIR 13MM', 'CLEAR 3MM', 'butter']
    bconstr.Layer_7 = "cheese"
    assert bconstr.obj == ['Construction', 'Dbl Clr 3mm/13mm Air', 'CLEAR 3MM', 'AIR 13MM', 'CLEAR 3MM', 'butter', '', '', 'cheese']
    bconstr["Layer_8"] = "jam"
    assert bconstr.obj == ['Construction', 'Dbl Clr 3mm/13mm Air', 'CLEAR 3MM', 'AIR 13MM', 'CLEAR 3MM', 'butter', '', '', 'cheese', 'jam']
    
    # retrieve a valid field that has no value
    assert bconstr.Layer_10 == ''
    assert bconstr["Layer_10"] == ''
    os.remove(iddfile)
    os.remove(fname)

def test_extendlist():
    """py.test for extendlist"""
    data = (([1,2,3], 2, 0, [1,2,3]), # lst, i, value, nlst
    ([1,2,3], 3, 0, [1,2,3,0]), # lst, i, value, nlst
    ([1,2,3], 5, 0, [1,2,3,0,0,0]), # lst, i, value, nlst
    ([1,2,3], 7, 0, [1,2,3,0,0,0,0,0]), # lst, i, value, nlst
    )
    for lst, i, value, nlst in data:
        bunch_subclass.extendlist(lst, i, value=value)
        assert lst == nlst
# test_EpBunch()