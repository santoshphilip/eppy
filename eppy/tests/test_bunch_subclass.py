# Copyright (c) 2012 Santosh Philip

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
from eppy.EPlusInterfaceFunctions import readidf
import eppy.bunchhelpers as bunchhelpers
import eppy.bunch_subclass as bunch_subclass
EpBunch = bunch_subclass.EpBunch

from eppy.iddcurrent import iddcurrent
iddtxt = iddcurrent.iddtxt

# This test is ugly because I have to send file names and not able to send file handles
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
    wallidd = commdct[wall_i]

    dwalls = dt[wallkey]
    dwall = dwalls[0]


    wallfields = [comm.get('field') for comm in commdct[wall_i]]
    wallfields[0] = ['key']
    wallfields = [field[0] for field in wallfields]
    wall_fields = [bunchhelpers.makefieldname(field) for field in wallfields]
    # print wall_fields[:20]
    assert wall_fields[:20] == ['key', 'Name', 'Surface_Type', 'Construction_Name', 'Zone_Name', 'Outside_Boundary_Condition', 'Outside_Boundary_Condition_Object', 'Sun_Exposure', 'Wind_Exposure', 'View_Factor_to_Ground', 'Number_of_Vertices', 'Vertex_1_Xcoordinate', 'Vertex_1_Ycoordinate', 'Vertex_1_Zcoordinate', 'Vertex_2_Xcoordinate', 'Vertex_2_Ycoordinate', 'Vertex_2_Zcoordinate', 'Vertex_3_Xcoordinate', 'Vertex_3_Ycoordinate', 'Vertex_3_Zcoordinate']
    

    bwall = EpBunch(dwall, wall_fields, wallidd)

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
    constridd = commdct[constr_i]
    dconstrs = dt[constrkey]
    dconstr = dconstrs[0]
    constrfields = [comm.get('field') for comm in commdct[constr_i]]
    constrfields[0] = ['key']
    constrfields = [field[0] for field in constrfields]
    constr_fields = [bunchhelpers.makefieldname(field) for field in constrfields]
    bconstr = EpBunch(dconstr, constr_fields, constridd)
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
    
class TestEpBunch:
    """py.test for EpBunch.getrange, EpBunch.checkrange"""
    def test_getrange(self):
        data = ((
            ['BUILDING',
            'Empire State Building',
            30.0,
            'City',
            0.04,
            0.4,
            'FullExterior',
            25,
            6], #obj
            
            ['key',
            'Name',
            'North_Axis',
            'Terrain',
            'Loads_Convergence_Tolerance_Value',
            'Temperature_Convergence_Tolerance_Value',
            'Solar_Distribution',
            'Maximum_Number_of_Warmup_Days',
            'Minimum_Number_of_Warmup_Days'],
            
            [{},
            {},
            {},
            {},
            
            {'maximum': ['.5'],
            'minimum>': ['0.0'],},
            
            {'maximum': ['.5'],
            'minimum>': ['0.0'],},
            
            {},

            {'minimum>': ['0'],},
            
            {'minimum>': ['0'],},
            ],
            
         ), # obj, objls, objidd
        )
        
        for obj, objls, objidd in data:
            assert 1 == 1
            
            
# test_EpBunch()