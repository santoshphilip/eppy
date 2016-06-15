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
    3.000000000000;  !- Vertex 1 Z-coordinate {m}""",
    'Box',
    ['N_Wall']), # idftxt, zname, surfnamelst
    )
    for idftxt, zname, surfnamelst in data:
        idf = IDF(StringIO(idftxt))
        result = idffunctions.getzonesurfaces(idf, zname)
        assert result == surfnamelst