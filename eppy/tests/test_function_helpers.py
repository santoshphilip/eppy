# Copyright (c) 2020 Cheng Cui
# =======================================================================
#  Distributed under the MIT License.
#  (See accompanying file LICENSE or copy at
#  http://opensource.org/licenses/MIT)
# =======================================================================

"""py.test for function_helpers"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from six import StringIO

import eppy.function_helpers as fh
from eppy.iddcurrent import iddcurrent
from eppy.modeleditor import IDF
from eppy.pytest_helpers import almostequal

iddtxt = iddcurrent.iddtxt
iddfhandle = StringIO(iddcurrent.iddtxt)
if IDF.getiddname() == None:
    IDF.setiddname(iddfhandle)

idftxt = """
    Version,8.0;

    Building,
        Simple One Zone,         !- Name
        ;                        !- North Axis {deg} 

    Zone,
        ZONE ONE,                !- Name
        ,                        !- Direction of Relative North {deg}
        0, 0, 0;                            !- X,Y,Z  {m}

    GlobalGeometryRules,
        UpperLeftCorner,         !- Starting Vertex Position
        CounterClockWise,        !- Vertex Entry Direction
        World;                   !- Coordinate System

    BuildingSurface:Detailed,
        Zn001:Wall001,           !- Name
        Wall,                    !- Surface Type
        R13WALL,                 !- Construction Name
        ZONE ONE,                !- Zone Name
        Outdoors,                !- Outside Boundary Condition
        ,                        !- Outside Boundary Condition Object
        SunExposed,              !- Sun Exposure
        WindExposed,             !- Wind Exposure
        0.5000000,               !- View Factor to Ground
        4,                       !- Number of Vertices
        0, 0, 4.572000,                     !- X,Y,Z  1 {m}
        0, 0, 0,                            !- X,Y,Z  2 {m}
        15.24000, 0, 0,                     !- X,Y,Z  3 {m}
        15.24000, 0, 4.572000;              !- X,Y,Z  4 {m}

    BuildingSurface:Detailed,
        Zn001:Wall002,           !- Name
        Wall,                    !- Surface Type
        R13WALL,                 !- Construction Name
        ZONE ONE,                !- Zone Name
        Outdoors,                !- Outside Boundary Condition
        ,                        !- Outside Boundary Condition Object
        SunExposed,              !- Sun Exposure
        WindExposed,             !- Wind Exposure
        0.5000000,               !- View Factor to Ground
        4,                       !- Number of Vertices
        15.24000, 0, 4.572000,              !- X,Y,Z  1 {m}
        15.24000, 0, 0,                     !- X,Y,Z  2 {m}
        15.24000, 15.24000, 0,              !- X,Y,Z  3 {m}
        15.24000, 15.24000, 4.572000;       !- X,Y,Z  4 {m}

    BuildingSurface:Detailed,
        Zn001:Wall003,           !- Name
        Wall,                    !- Surface Type
        R13WALL,                 !- Construction Name
        ZONE ONE,                !- Zone Name
        Outdoors,                !- Outside Boundary Condition
        ,                        !- Outside Boundary Condition Object
        SunExposed,              !- Sun Exposure
        WindExposed,             !- Wind Exposure
        0.5000000,               !- View Factor to Ground
        4,                       !- Number of Vertices
        15.24000, 15.24000, 4.572000,       !- X,Y,Z  1 {m}
        15.24000, 15.24000, 0,              !- X,Y,Z  2 {m}
        0, 15.24000, 0,                     !- X,Y,Z  3 {m}
        0, 15.24000, 4.572000;              !- X,Y,Z  4 {m}

    BuildingSurface:Detailed,
        Zn001:Wall004,           !- Name
        Wall,                    !- Surface Type
        R13WALL,                 !- Construction Name
        ZONE ONE,                !- Zone Name
        Outdoors,                !- Outside Boundary Condition
        ,                        !- Outside Boundary Condition Object
        SunExposed,              !- Sun Exposure
        WindExposed,             !- Wind Exposure
        0.5000000,               !- View Factor to Ground
        4,                       !- Number of Vertices
        0, 15.24000, 4.572000,              !- X,Y,Z  1 {m}
        0, 15.24000, 0,                     !- X,Y,Z  2 {m}
        0, 0, 0,                            !- X,Y,Z  3 {m}
        0, 0, 4.572000;                     !- X,Y,Z  4 {m}

    BuildingSurface:Detailed,
        Zn001:Flr001,            !- Name
        Floor,                   !- Surface Type
        FLOOR,                   !- Construction Name
        ZONE ONE,                !- Zone Name
        Adiabatic,               !- Outside Boundary Condition
        ,                        !- Outside Boundary Condition Object
        NoSun,                   !- Sun Exposure
        NoWind,                  !- Wind Exposure
        1.000000,                !- View Factor to Ground
        4,                       !- Number of Vertices
        15.24000, 0.000000, 0.0,            !- X,Y,Z  1 {m}
        0.000000, 0.000000, 0.0,            !- X,Y,Z  2 {m}
        0.000000, 15.24000, 0.0,            !- X,Y,Z  3 {m}
        15.24000, 15.24000, 0.0;            !- X,Y,Z  4 {m}

    BuildingSurface:Detailed,
        Zn001:Roof001,           !- Name
        Roof,                    !- Surface Type
        ROOF31,                  !- Construction Name
        ZONE ONE,                !- Zone Name
        Outdoors,                !- Outside Boundary Condition
        ,                        !- Outside Boundary Condition Object
        SunExposed,              !- Sun Exposure
        WindExposed,             !- Wind Exposure
        0,                       !- View Factor to Ground
        4,                       !- Number of Vertices
        0.000000, 15.24000, 4.572,          !- X,Y,Z  1 {m}
        0.000000, 0.000000, 4.572,          !- X,Y,Z  2 {m}
        15.24000, 0.000000, 4.572,          !- X,Y,Z  3 {m}
        15.24000, 15.24000, 4.572;          !- X,Y,Z  4 {m}
"""


def test_true_azimuth():
    """py.test for true_azimuth"""
    data = (
        (45, 30, 255),
        # building_north_axis, zone_direction_of_relative_north, answer,
        ("", 0, 180),
        (20, "", 200),
        (240, 90, 150),
    )

    fhandle = StringIO(idftxt)
    idf = IDF(fhandle)
    building = idf.idfobjects["Building"][0]
    zone = idf.idfobjects["Zone"][0]
    surface = idf.idfobjects["BuildingSurface:Detailed"][0]

    for building_north_axis, zone_direction_of_relative_north, answer in data:
        building.North_Axis = building_north_axis
        zone.Direction_of_Relative_North = zone_direction_of_relative_north
        result = fh.true_azimuth(surface)
        assert almostequal(answer, result, places=3) == True
