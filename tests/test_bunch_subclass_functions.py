# Copyright (c) 2020 Cheng Cui
# =======================================================================
#  Distributed under the MIT License.
#  (See accompanying file LICENSE or copy at
#  http://opensource.org/licenses/MIT)
# =======================================================================

"""py.test for bunch_subclass_functions"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from io import StringIO

from eppy.iddcurrent import iddcurrent
from eppy.modeleditor import IDF
from eppy.pytest_helpers import almostequal


iddtxt = iddcurrent.iddtxt
iddfhandle = StringIO(iddcurrent.iddtxt)
if IDF.getiddname() == None:
    IDF.setiddname(iddfhandle)

idftxt = """Version,8.0;

    Building,
        building,                !- Name
        45;                      !- North Axis {deg} 

    Zone,
        West Zone,               !- Name
        30,                      !- Direction of Relative North {deg}
        0, 0, 0;                            !- X,Y,Z  {m}

    GlobalGeometryRules,
        UpperLeftCorner,         !- Starting Vertex Position
        CounterClockWise,        !- Vertex Entry Direction
        Relative;                !- Coordinate System

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

"""


def test_surface_function():
    fhandle = StringIO(idftxt)
    idf = IDF(fhandle)
    surface = idf.idfobjects["BuildingSurface:Detailed"][0]

    # test the azimuth
    assert almostequal(surface.azimuth, 180, places=3) == True

    # test the true azimuth
    assert almostequal(surface.true_azimuth, 255, places=3) == True
