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

from io import StringIO
import pytest

import eppy.function_helpers as fh
from eppy.iddcurrent import iddcurrent
from eppy.modeleditor import IDF
from eppy.pytest_helpers import almostequal

iddtxt = iddcurrent.iddtxt
iddfhandle = StringIO(iddcurrent.iddtxt)
if IDF.getiddname() == None:
    IDF.setiddname(iddfhandle)

idftxt = """Version,8.0;

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

"""


# original test_true_azimuth() - done using a loop
# def test_true_azimuth():
#     """py.test for true_azimuth"""
#     data = (
#         ("Relative", 45, 30, 180 + 75),
#         # coord_system, bldg_north, zone_rel_north, expected,
#         ("Relative", "", 0, 180 + 0),
#         ("World", 45, "", 180),
#         ("Relative", 240, 90, 180 + 330 - 360),
#     )
#
#     fhandle = StringIO(idftxt)
#     idf = IDF(fhandle)
#     geom_rules = idf.idfobjects["GlobalGeometryRules"][0]
#     building = idf.idfobjects["Building"][0]
#     zone = idf.idfobjects["Zone"][0]
#     surface = idf.idfobjects["BuildingSurface:Detailed"][0]
#
#     for coord_system, bldg_north, zone_rel_north, expected in data:
#         geom_rules.Coordinate_System = coord_system
#         building.North_Axis = bldg_north
#         zone.Direction_of_Relative_North = zone_rel_north
#         result = fh.true_azimuth(surface)
#         assert almostequal(expected, result, places=3) == True

# test_true_azimuth() - done using @pytest.mark.parametrize
# see https://docs.pytest.org/en/stable/parametrize.html
@pytest.mark.parametrize(
    "coord_system, bldg_north, zone_rel_north, expected",
    [
        ("Relative", 45, 30, 180 + 75),
        # coord_system, bldg_north, zone_rel_north, expected,
        ("Relative", "", 0, 180 + 0),
        ("World", 45, "", 180),
        ("Relative", 240, 90, 180 + 330 - 360),
    ],
)
def test_true_azimuth(coord_system, bldg_north, zone_rel_north, expected):
    """py.test for true_azimuth"""
    fhandle = StringIO(idftxt)
    idf = IDF(fhandle)
    geom_rules = idf.idfobjects["GlobalGeometryRules"][0]
    building = idf.idfobjects["Building"][0]
    zone = idf.idfobjects["Zone"][0]
    surface = idf.idfobjects["BuildingSurface:Detailed"][0]

    geom_rules.Coordinate_System = coord_system
    building.North_Axis = bldg_north
    zone.Direction_of_Relative_North = zone_rel_north
    result = fh.true_azimuth(surface)
    assert almostequal(expected, result, places=3) == True


def test_true_azimuth_exception():
    """py.test for true_azimuth exception"""
    coord_system, bldg_north, zone_rel_north = (
        "Global",
        0,
        0,
    )

    fhandle = StringIO(idftxt)
    idf = IDF(fhandle)
    geom_rules = idf.idfobjects["GlobalGeometryRules"][0]
    building = idf.idfobjects["Building"][0]
    zone = idf.idfobjects["Zone"][0]
    surface = idf.idfobjects["BuildingSurface:Detailed"][0]

    geom_rules.Coordinate_System = coord_system
    building.North_Axis = bldg_north
    zone.Direction_of_Relative_North = zone_rel_north

    with pytest.raises(ValueError):
        result = fh.true_azimuth(surface)
