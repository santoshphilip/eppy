# Copyright (c) 2012, 2020 Santosh Philip
# =======================================================================
#  Distributed under the MIT License.
#  (See accompanying file LICENSE or copy at
#  http://opensource.org/licenses/MIT)
# =======================================================================

"""py.test for bunch_subclass"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import pytest
from io import StringIO

from eppy.EPlusInterfaceFunctions import readidf
import eppy.bunch_subclass as bunch_subclass
import eppy.bunchhelpers as bunchhelpers
from eppy.iddcurrent import iddcurrent
import eppy.idfreader as idfreader
from eppy.modeleditor import IDF
from eppy.pytest_helpers import almostequal


# This test is ugly because I have to send file names and not able to send file handles
EpBunch = bunch_subclass.EpBunch

iddtxt = iddcurrent.iddtxt

# idd is read only once in this test
# if it has already been read from some other test, it will continue with
# the old reading
iddfhandle = StringIO(iddcurrent.iddtxt)
if IDF.getiddname() == None:
    IDF.setiddname(iddfhandle)

# This test is ugly because I have to send file names and not able to send file handles
idftxt = """Version,6.0;

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


def test_EpBunch():
    """py.test for EpBunch"""

    iddfile = StringIO(iddtxt)
    fname = StringIO(idftxt)
    block, data, commdct, idd_index = readidf.readdatacommdct1(fname, iddfile=iddfile)

    # setup code walls - can be generic for any object
    ddtt = data.dt
    dtls = data.dtls
    wall_i = dtls.index("BuildingSurface:Detailed".upper())
    wallkey = "BuildingSurface:Detailed".upper()
    wallidd = commdct[wall_i]

    dwalls = ddtt[wallkey]
    dwall = dwalls[0]

    wallfields = [comm.get("field") for comm in commdct[wall_i]]
    wallfields[0] = ["key"]
    wallfields = [field[0] for field in wallfields]
    wall_fields = [bunchhelpers.makefieldname(field) for field in wallfields]
    assert wall_fields[:20] == [
        "key",
        "Name",
        "Surface_Type",
        "Construction_Name",
        "Zone_Name",
        "Outside_Boundary_Condition",
        "Outside_Boundary_Condition_Object",
        "Sun_Exposure",
        "Wind_Exposure",
        "View_Factor_to_Ground",
        "Number_of_Vertices",
        "Vertex_1_Xcoordinate",
        "Vertex_1_Ycoordinate",
        "Vertex_1_Zcoordinate",
        "Vertex_2_Xcoordinate",
        "Vertex_2_Ycoordinate",
        "Vertex_2_Zcoordinate",
        "Vertex_3_Xcoordinate",
        "Vertex_3_Ycoordinate",
        "Vertex_3_Zcoordinate",
    ]

    bwall = EpBunch(dwall, wall_fields, wallidd)

    # print bwall.Name
    # print data.dt[wallkey][0][1]
    assert bwall.Name == data.dt[wallkey][0][1]
    bwall.Name = "Gumby"
    # print bwall.Name
    # print data.dt[wallkey][0][1]
    # print
    assert bwall.Name == data.dt[wallkey][0][1]

    # set aliases
    bwall.__aliases = {"Constr": "Construction_Name"}

    # print "wall.Construction_Name = %s" % (bwall.Construction_Name, )
    # print "wall.Constr = %s" % (bwall.Constr, )
    # print
    assert bwall.Construction_Name == bwall.Constr
    # print "change wall.Constr"
    bwall.Constr = "AnewConstr"
    # print "wall.Constr = %s" % (bwall.Constr, )
    # print "wall.Constr = %s" % (data.dt[wallkey][0][3], )
    # print
    assert bwall.Constr == data.dt[wallkey][0][3]

    # add functions
    bwall.__functions = {"svalues": bunch_subclass.somevalues}
    assert "svalues" in bwall.__functions

    # print bwall.svalues
    assert bwall.svalues == (
        "Gumby",
        "AnewConstr",
        [
            "BuildingSurface:Detailed",
            "Gumby",
            "Wall",
            "AnewConstr",
            "West Zone",
            "Outdoors",
            "",
            "SunExposed",
            "WindExposed",
            "0.5000000",
            "4",
            "0",
            "0",
            "3.048000",
            "0",
            "0",
            "0",
            "6.096000",
            "0",
            "0",
            "6.096000",
            "0",
            "3.048000",
        ],
    )

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
    assert bwall.svalues == (
        newname,
        "AnewConstr",
        [
            "BuildingSurface:Detailed",
            newname,
            "Wall",
            "AnewConstr",
            "West Zone",
            "Outdoors",
            "",
            "SunExposed",
            "WindExposed",
            "0.5000000",
            "4",
            "0",
            "0",
            "3.048000",
            "0",
            "0",
            "0",
            "6.096000",
            "0",
            "0",
            "6.096000",
            "0",
            "3.048000",
        ],
    )
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
    constr_i = dtls.index("Construction".upper())
    constrkey = "Construction".upper()
    constridd = commdct[constr_i]
    dconstrs = ddtt[constrkey]
    dconstr = dconstrs[0]
    constrfields = [comm.get("field") for comm in commdct[constr_i]]
    constrfields[0] = ["key"]
    constrfields = [field[0] for field in constrfields]
    constr_fields = [bunchhelpers.makefieldname(field) for field in constrfields]
    bconstr = EpBunch(dconstr, constr_fields, constridd)
    assert bconstr.Name == "Dbl Clr 3mm/13mm Air"
    bconstr.Layer_4 = "butter"
    assert bconstr.obj == [
        "Construction",
        "Dbl Clr 3mm/13mm Air",
        "CLEAR 3MM",
        "AIR 13MM",
        "CLEAR 3MM",
        "butter",
    ]
    bconstr.Layer_7 = "cheese"
    assert bconstr.obj == [
        "Construction",
        "Dbl Clr 3mm/13mm Air",
        "CLEAR 3MM",
        "AIR 13MM",
        "CLEAR 3MM",
        "butter",
        "",
        "",
        "cheese",
    ]
    bconstr["Layer_8"] = "jam"
    assert bconstr.obj == [
        "Construction",
        "Dbl Clr 3mm/13mm Air",
        "CLEAR 3MM",
        "AIR 13MM",
        "CLEAR 3MM",
        "butter",
        "",
        "",
        "cheese",
        "jam",
    ]

    # retrieve a valid field that has no value
    assert bconstr.Layer_10 == ""
    assert bconstr["Layer_10"] == ""


def test_extendlist():
    """py.test for extendlist"""
    data = (
        ([1, 2, 3], 2, 0, [1, 2, 3]),  # lst, i, value, nlst
        ([1, 2, 3], 3, 0, [1, 2, 3, 0]),  # lst, i, value, nlst
        ([1, 2, 3], 5, 0, [1, 2, 3, 0, 0, 0]),  # lst, i, value, nlst
        ([1, 2, 3], 7, 0, [1, 2, 3, 0, 0, 0, 0, 0]),  # lst, i, value, nlst
    )
    for lst, i, value, nlst in data:
        bunch_subclass.extendlist(lst, i, value=value)
        assert lst == nlst


class TestEpBunch(object):
    """
    py.test for EpBunch.getrange, EpBunch.checkrange, EpBunch.fieldnames,
    EpBunch.fieldvalues, EpBunch.getidd.

    """

    def initdata(self):
        obj, objls, objidd = (
            [
                "BUILDING",
                "Empire State Building",
                30.0,
                "City",
                0.04,
                0.4,
                "FullExterior",
                25,
                6,
            ],  # obj
            [
                "key",
                "Name",
                "North_Axis",
                "Terrain",
                "Loads_Convergence_Tolerance_Value",
                "Temperature_Convergence_Tolerance_Value",
                "Solar_Distribution",
                "Maximum_Number_of_Warmup_Days",
                "Minimum_Number_of_Warmup_Days",
            ],
            # the following objidd are made up
            [
                {},
                {
                    "default": ["NONE"],
                    "field": ["Name"],
                    "required-field": [""],
                    "retaincase": [""],
                },
                {"type": ["real"]},
                {
                    "default": ["Suburbs"],
                    "field": ["Terrain"],
                    "key": ["Country", "Suburbs", "City", "Ocean", "Urban"],
                    "note": [
                        "Country=FlatOpenCountry | Suburbs=CountryTownsSuburbs | City=CityCenter | Ocean=body of water (5km) | Urban=Urban-Industrial-Forest"
                    ],
                    "type": ["choice"],
                },
                {"maximum": [".5"], "minimum>": ["0.0"], "type": ["real"]},
                {"maximum": [".5"], "minimum>": ["0.0"], "type": ["real"]},
                {"type": ["choice"]},
                {
                    "maximum": None,
                    "minimum": None,
                    "maximum<": ["5"],
                    "minimum>": ["-3"],
                    "type": ["integer"],
                },
                {
                    "maximum": ["5"],
                    "minimum": ["-3"],
                    "maximum<": None,
                    "minimum>": None,
                    "type": ["real"],
                },
            ],
        )
        return obj, objls, objidd

    def test_fieldnames(self):
        """
        Test that the contents of idfobject.fieldnames are the same as those
        of objls.

        """
        obj, objls, objidd = self.initdata()
        idfobject = EpBunch(obj, objls, objidd)
        for fn_item, objls_item in zip(idfobject.fieldnames, idfobject.objls):
            assert fn_item == objls_item

    def test_fieldvalues(self):
        """
        Test that the contents of idfobject.fieldvalues are the same as those
        of obj.

        """
        obj, objls, objidd = self.initdata()
        idfobject = EpBunch(obj, objls, objidd)
        for fv_item, objls_item in zip(idfobject.fieldvalues, idfobject.obj):
            assert fv_item == objls_item

    def test_getrange(self):
        data = (
            (
                "Loads_Convergence_Tolerance_Value",
                {
                    "maximum": 0.5,
                    "minimum>": 0.0,
                    "maximum<": None,
                    "minimum": None,
                    "type": "real",
                },
            ),  # fieldname, theranges
            (
                "Maximum_Number_of_Warmup_Days",
                {
                    "maximum": None,
                    "minimum>": -3,
                    "maximum<": 5,
                    "minimum": None,
                    "type": "integer",
                },
            ),  # fieldname, theranges
        )
        obj, objls, objidd = self.initdata()
        idfobject = EpBunch(obj, objls, objidd)
        for fieldname, theranges in data:
            result = idfobject.getrange(fieldname)
            assert result == theranges

    def test_checkrange(self):
        data = (
            ("Minimum_Number_of_Warmup_Days", 4, False, None),
            # fieldname, fieldvalue, isexception, theexception
            ("Minimum_Number_of_Warmup_Days", 6, True, bunch_subclass.RangeError),
            # fieldname, fieldvalue, isexception, theexception
            ("Minimum_Number_of_Warmup_Days", 5, False, None),
            # fieldname, fieldvalue, isexception, theexception
            ("Minimum_Number_of_Warmup_Days", -3, False, None),
            # fieldname, fieldvalue, isexception, theexception
            ("Minimum_Number_of_Warmup_Days", -4, True, bunch_subclass.RangeError),
            # fieldname, fieldvalue, isexception, theexception
            # -
            ("Maximum_Number_of_Warmup_Days", 4, False, None),
            # fieldname, fieldvalue, isexception, theexception
            ("Maximum_Number_of_Warmup_Days", 5, True, bunch_subclass.RangeError),
            # fieldname, fieldvalue, isexception, theexception
            ("Maximum_Number_of_Warmup_Days", -3, True, bunch_subclass.RangeError),
            # fieldname, fieldvalue, isexception, theexception
            (
                "Loads_Convergence_Tolerance_Value",
                0.3,
                False,
                bunch_subclass.RangeError,
            ),
            # fieldname, fieldvalue, isexception, theexception
            ("Loads_Convergence_Tolerance_Value", 0, True, bunch_subclass.RangeError),
            # fieldname, fieldvalue, isexception, theexception
            # -
            ("North_Axis", 0, False, None),
            # fieldname, fieldvalue, isexception, theexception
            ("Name", "Empire State Building", False, None),
            # fieldname, fieldvalue, isexception, theexception
            ("key", "BUILDING", False, None),
            # fieldname, fieldvalue, isexception, theexception
        )
        obj, objls, objidd = self.initdata()
        idfobject = EpBunch(obj, objls, objidd)
        for fieldname, fieldvalue, isexception, theexception in data:
            idfobject[fieldname] = fieldvalue
            if not isexception:
                result = idfobject.checkrange(fieldname)
                assert result == fieldvalue
            else:
                with pytest.raises(theexception):
                    result = idfobject.checkrange(fieldname)

    def test_getfieldidd(self):
        """py.test for getfieldidd"""
        obj, objls, objidd = self.initdata()
        idfobject = EpBunch(obj, objls, objidd)
        result = idfobject.getfieldidd("North_Axis")
        assert result == {"type": ["real"]}
        result = idfobject.getfieldidd("No_such_field")
        assert result == {}

    def test_getfieldidd_item(self):
        """py.test for test_getfieldidd_item"""
        obj, objls, objidd = self.initdata()
        idfobject = EpBunch(obj, objls, objidd)
        result = idfobject.getfieldidd_item("North_Axis", "type")
        assert result == ["real"]
        result = idfobject.getfieldidd_item("North_Axis", "no_such_key")
        assert result == []
        result = idfobject.getfieldidd_item("no_such_field", "type")
        assert result == []

    def test_get_retaincase(self):
        """py.test for get_retaincase"""
        obj, objls, objidd = self.initdata()
        idfobject = EpBunch(obj, objls, objidd)
        result = idfobject.get_retaincase("Name")
        assert result == True
        result = idfobject.get_retaincase("Terrain")
        assert result == False

    def test_isequal(self):
        """py.test for isequal"""
        obj, objls, objidd = self.initdata()
        idfobject = EpBunch(obj, objls, objidd)
        # test Terrain -> Alphanumeric, no retaincase
        result = idfobject.isequal("Terrain", "City")
        assert result == True
        result = idfobject.isequal("Terrain", "Rural")
        assert result == False
        result = idfobject.isequal("Terrain", "CITY")
        assert result == True
        # test Name -> Alphanumeric, retaincase
        result = idfobject.isequal("Name", "Empire State Building")
        assert result == True
        result = idfobject.isequal("Name", "Empire State Building".upper())
        assert result == False
        # test North_Axis -> real
        result = idfobject.isequal("North_Axis", 30)
        assert result == True
        result = idfobject.isequal("North_Axis", "30")
        assert result == True
        # test North_Axis -> real
        result = idfobject.isequal("North_Axis", 30.02)
        assert result == False
        result = idfobject.isequal("North_Axis", 30.02, places=1)
        assert result == True
        # test Maximum_Number_of_Warmup_Days -> integer
        result = idfobject.isequal("Maximum_Number_of_Warmup_Days", 25)
        assert result == True
        result = idfobject.isequal("Maximum_Number_of_Warmup_Days", 25.0000)
        assert result == True
        result = idfobject.isequal("Maximum_Number_of_Warmup_Days", 25.00001)
        assert result == False

    def test_getreferingobjs(self):
        """py.test for getreferingobjs"""
        thedata = (
            (
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
      HVACTemplate:Thermostat,
        Constant Setpoint Thermostat,  !- Name
        ,                        !- Heating Setpoint Schedule Name
        20,                      !- Constant Heating Setpoint {C}
        ,                        !- Cooling Setpoint Schedule Name
        25;                      !- Constant Cooling Setpoint {C}

    FENESTRATIONSURFACE:DETAILED,
        Window1,                  !- Name
        ,                         !- Surface Type
        ,                         !- Construction Name
        EWall1,                         !- Building Surface Name
        ,                         !- Outside Boundary Condition Object
        autocalculate,            !- View Factor to Ground
        ,                         !- Shading Control Name
        ,                         !- Frame and Divider Name
        1.0,                      !- Multiplier
        autocalculate;            !- Number of Vertices
      """,
                "Box",
                ["N_Wall", "EWall", "WallExterior"],
            ),  # idftxt, zname, surfnamelst
        )
        for idftxt, zname, surfnamelst in thedata:
            # import pdb; pdb.set_trace()
            idf = IDF(StringIO(idftxt))
            zone = idf.getobject("zone", zname)
            kwargs = {}
            result = zone.getreferingobjs(**kwargs)
            rnames = [item.Name for item in result]
            rnames.sort()
            surfnamelst.sort()
            assert rnames == surfnamelst
        for idftxt, zname, surfnamelst in thedata:
            idf = IDF(StringIO(idftxt))
            zone = idf.getobject("zone", zname)
            kwargs = {"iddgroups": ["Thermal Zones and Surfaces"]}
            result = zone.getreferingobjs(**kwargs)
            rnames = [item.Name for item in result]
            rnames.sort()
            surfnamelst.sort()
            assert rnames == surfnamelst
        for idftxt, zname, surfnamelst in thedata:
            idf = IDF(StringIO(idftxt))
            zone = idf.getobject("zone", zname)
            kwargs = {"fields": ["Zone_Name"]}
            result = zone.getreferingobjs(**kwargs)
            rnames = [item.Name for item in result]
            rnames.sort()
            surfnamelst.sort()
            assert rnames == surfnamelst
        for idftxt, zname, surfnamelst in thedata:
            idf = IDF(StringIO(idftxt))
            zone = idf.getobject("zone", zname)
            kwargs = {
                "fields": ["Zone_Name"],
                "iddgroups": ["Thermal Zones and Surfaces"],
            }
            result = zone.getreferingobjs(**kwargs)
            rnames = [item.Name for item in result]
            rnames.sort()
            surfnamelst.sort()
            assert rnames == surfnamelst
        # use the above idftxt and try other to get other references.
        for idftxt, zname, surfnamelst in thedata:
            idf = IDF(StringIO(idftxt))
            wname = "EWall1"
            windownamelist = ["Window1"]
            wall = idf.getobject("BUILDINGSURFACE:DETAILED", wname)
            kwargs = {
                "fields": ["Building_Surface_Name"],
                "iddgroups": ["Thermal Zones and Surfaces"],
            }
            result = wall.getreferingobjs(**kwargs)
            rnames = [item.Name for item in result]
            rnames.sort()
            surfnamelst.sort()
            assert rnames == windownamelist

    def test_get_referenced_object(self):
        """py.test for get_referenced_object"""
        idf = IDF()
        idf.initnew("test.idf")
        idf.newidfobject("VERSION")  # does not have a field "Name"

        # construction material
        construction = idf.newidfobject("CONSTRUCTION", Name="construction")
        construction.Outside_Layer = "TestMaterial"

        expected = idf.newidfobject("MATERIAL", Name="TestMaterial")

        fetched = idf.getobject("MATERIAL", "TestMaterial")
        assert fetched == expected

        material = construction.get_referenced_object("Outside_Layer")
        assert material == expected

        # window material
        glazing_group = idf.newidfobject(
            "WINDOWMATERIAL:GLAZINGGROUP:THERMOCHROMIC", Name="glazing_group"
        )
        glazing_group.Window_Material_Glazing_Name_1 = "TestWindowMaterial"

        expected = idf.newidfobject(
            "WINDOWMATERIAL:GLAZING", Name="TestWindowMaterial"
        )  # has several \references

        fetched = idf.getobject("WINDOWMATERIAL:GLAZING", "TestWindowMaterial")
        assert fetched == expected

        material = glazing_group.get_referenced_object("Window_Material_Glazing_Name_1")
        assert material == expected


bldfidf = """
Version,
    6.0;

BUILDING,
    Empire State Building,    !- Name
    30.0,                     !- North Axis
    City,                     !- Terrain
    0.04,                     !- Loads Convergence Tolerance Value
    0.4,                      !- Temperature Convergence Tolerance Value
    FullExterior,             !- Solar Distribution
    25,                       !- Maximum Number of Warmup Days
    6;                        !- Minimum Number of Warmup Days

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
# test_EpBunch1()
# import idfreader


def test_EpBunch1():
    """py.test for EpBunch1"""
    iddfile = StringIO(iddtxt)
    idffile = StringIO(bldfidf)
    block, data, commdct, idd_index = readidf.readdatacommdct1(idffile, iddfile=iddfile)
    key = "BUILDING"
    objs = data.dt[key]
    obj = objs[0]
    obj_i = data.dtls.index(key)
    bunchobj = idfreader.makeabunch(commdct, obj, obj_i)

    # assertions
    assert bunchobj.Name == "Empire State Building"
    bunchobj.Name = "Kutub Minar"
    assert bunchobj.Name == "Kutub Minar"
    prnt = bunchobj.__repr__()
    result = """
BUILDING,
    Kutub Minar,              !- Name
    30.0,                     !- North Axis
    City,                     !- Terrain
    0.04,                     !- Loads Convergence Tolerance Value
    0.4,                      !- Temperature Convergence Tolerance Value
    FullExterior,             !- Solar Distribution
    25,                       !- Maximum Number of Warmup Days
    6;                        !- Minimum Number of Warmup Days
"""
    assert prnt == result
    # print bunchobj.objidd
    # assert 1 == 0


def test_scientificnotation():
    """py.test to check if __repr__ for epbunch is printing scientific notation"""
    idftxt = """ScheduleTypeLimits,
    AnyValue,                !- Name
    -1e+019,                 !- Lower Limit Value
    1e+019,                  !- Upper Limit Value
    Continuous;              !- Numeric Type
"""
    expected = """
ScheduleTypeLimits,
    AnyValue,                 !- Name
    -1.000000e+19,            !- Lower Limit Value
    1.000000e+19,             !- Upper Limit Value
    Continuous;               !- Numeric Type
"""
    idffile = StringIO(idftxt)
    idf = IDF(idffile)
    sch = idf.idfobjects["ScheduleTypeLimits"][0]
    result = sch.__repr__()
    assert result == expected
