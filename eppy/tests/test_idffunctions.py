# Copyright (c) 2016 Santosh Philip
# =======================================================================
#  Distributed under the MIT License.
#  (See accompanying file LICENSE or copy at
#  http://opensource.org/licenses/MIT)
# =======================================================================
"""py.test for idffunctions"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from StringIO import StringIO
from eppy.iddcurrent import iddcurrent
from eppy.modeleditor import IDF
import eppy.idffunctions as idffunctions

# idd is read only once in this test
# if it has already been read from some other test, it will continue with
# the old reading
iddfhandle = StringIO(iddcurrent.iddtxt)
if IDF.getiddname() == None:
    IDF.setiddname(iddfhandle)

def test_getzonesurfaces():
    """py.test for getzonesurfaces"""
    data = ((
    """  Zone,
    Box,  !- Name
    0.0,  !- Direction of Relative North {deg}
    0.288184,  !- X Origin {m}
    0.756604,  !- Y Origin {m}
    0.0,  !- Z Origin {m}
    ,  !- Type
    1;  !- Multiplier

  BuildingSurface:Detailed,
    N_Wall,  !- Name
    Wall,  !- Surface Type
    Exterior Wall,  !- Construction Name
    Box,  !- Zone Name
    Outdoors,  !- Outside Boundary Condition
    ,  !- Outside Boundary Condition Object
    SunExposed,  !- Sun Exposure
    WindExposed,  !- Wind Exposure
    ,  !- View Factor to Ground
    1,  !- Number of Vertices
    5.000000000000,  !- Vertex 1 X-coordinate {m}
    6.000000000000,  !- Vertex 1 Y-coordinate {m}
    3.000000000000;  !- Vertex 1 Z-coordinate {m}
    
  WALL:EXTERIOR,            
      WallExterior,                    !- Name
      ,                         !- Construction Name
      Box,                         !- Zone Name
      ,                         !- Azimuth Angle
      90;                       !- Tilt Angle

    BUILDINGSURFACE:DETAILED, 
        EWall,                    !- Name
        ,                         !- Surface Type
        ,                         !- Construction Name
        BOX,                         !- Zone Name
        OtherBox,                         !- Outside Boundary Condition
        ,                         !- Outside Boundary Condition Object
        SunExposed,               !- Sun Exposure
        WindExposed,              !- Wind Exposure
        autocalculate,            !- View Factor to Ground
        autocalculate;            !- Number of Vertices

    BUILDINGSURFACE:DETAILED, 
        EWall1,                    !- Name
        ,                         !- Surface Type
        ,                         !- Construction Name
        BOX_other,                         !- Zone Name
        OtherBox,                         !- Outside Boundary Condition
        ,                         !- Outside Boundary Condition Object
        SunExposed,               !- Sun Exposure
        WindExposed,              !- Wind Exposure
        autocalculate,            !- View Factor to Ground
        autocalculate;            !- Number of Vertices
  """,
    'Box',
    ['N_Wall', 'EWall', 'WallExterior']), # idftxt, zname, surfnamelst
    )
    for idftxt, zname, surfnamelst in data:
        idf = IDF(StringIO(idftxt))
        zone = idf.getobject('zone'.upper(), zname)
        result = idffunctions.getzonesurfaces(idf, zone)
        rnames = [item.Name for item in result]
        rnames.sort()
        surfnamelst.sort()
        assert rnames == surfnamelst