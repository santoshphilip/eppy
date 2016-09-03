"""py.test for simplesurface.py"""
# =======================================================================
#  Distributed under the MIT License.
#  (See accompanying file LICENSE or copy at
#  http://opensource.org/licenses/MIT)
# =======================================================================

from eppy import simplesurface
from eppy.modeleditor import IDF


def test_wallexterior():
    """py.test for wallexterior"""
    bsdtxt = """BuildingSurface:Detailed, WALL-1PF, WALL, WALL-1, PLENUM-1,
    Outdoors, , SunExposed, WindExposed, 0.5, 4, 0.0, 0.0, 3.0, 0.0, 0.0, 2.4, 
    30.5, 0.0, 2.4, 30.5, 0.0, 3.0;
"""
    simpleobjtxt = """WALL:EXTERIOR, WALL-1PF, WALL-1, PLENUM-1, 180.0, 90.0, 0, 0, 0, 30.5, 0.6;"""
    idf = IDF()
    idf.initreadtxt(bsdtxt)
    bsd = idf.idfobjects["BuildingSurface:Detailed".upper()][0]
    surf = simplesurface.wallexterior(idf, bsd, deletebsd=False, setto000=True)
    newidttxt = bsdtxt + simpleobjtxt
    newidf = IDF()
    newidf.initreadtxt(newidttxt)
    assert idf.__almostequal__(newidf)

    # test  for deletebsd = True
    idf = IDF()
    idf.initreadtxt(bsdtxt)
    bsd = idf.idfobjects["BuildingSurface:Detailed".upper()][0]
    surf = simplesurface.wallexterior(idf, bsd, deletebsd=True, setto000=True)
    newidttxt = simpleobjtxt
    newidf = IDF()
    newidf.initreadtxt(newidttxt)
    assert idf.__almostequal__(newidf)


def test_walladiabatic():
    """py.test for walladiabatic"""
    bsdtxt = """BuildingSurface:Detailed, WALL-1PF, WALL, WALL-1, PLENUM-1,
    Adiabatic, , SunExposed, WindExposed, 0.5, 4, 0.0, 0.0, 3.0, 0.0, 0.0, 2.4,
    30.5, 0.0, 2.4, 30.5, 0.0, 3.0;
"""
    simpleobjtxt = """WALL:ADIABATIC, WALL-1PF, WALL-1, PLENUM-1, 180.0, 90.0,
    0, 0, 0, 30.5, 0.6;"""
    idf = IDF()
    idf.initreadtxt(bsdtxt)
    bsd = idf.idfobjects["BuildingSurface:Detailed".upper()][0]
    surf = simplesurface.walladiabatic(
        idf, bsd, deletebsd=False,
        setto000=True)
    newidttxt = bsdtxt + simpleobjtxt
    newidf = IDF()
    newidf.initreadtxt(newidttxt)
    assert idf.__almostequal__(newidf)

    # test  for deletebsd = True
    idf = IDF()
    idf.initreadtxt(bsdtxt)
    bsd = idf.idfobjects["BuildingSurface:Detailed".upper()][0]
    surf = simplesurface.walladiabatic(idf, bsd, deletebsd=True, setto000=True)
    newidttxt = simpleobjtxt
    newidf = IDF()
    newidf.initreadtxt(newidttxt)
    assert idf.__almostequal__(newidf)


def test_wallunderground():
    """py.test for wallunderground"""
    bsdtxt = """BuildingSurface:Detailed, WALL-1PF, WALL, WALL-1, PLENUM-1,
    Ground, , SunExposed, WindExposed, 0.5, 4, 0.0, 0.0, 3.0, 0.0, 0.0, 2.4, 
    30.5, 0.0, 2.4, 30.5, 0.0, 3.0;
"""
    simpleobjtxt = """WALL:UNDERGROUND, WALL-1PF, WALL-1, PLENUM-1, 180.0,
    90.0, 0, 0, 0, 30.5, 0.6;"""
    idf = IDF()
    idf.initreadtxt(bsdtxt)
    bsd = idf.idfobjects["BuildingSurface:Detailed".upper()][0]
    surf = simplesurface.wallunderground(
        idf, bsd, deletebsd=False,
        setto000=True)
    newidttxt = bsdtxt + simpleobjtxt
    newidf = IDF()
    newidf.initreadtxt(newidttxt)
    assert idf.__almostequal__(newidf)

    # test  for deletebsd = True
    idf = IDF()
    idf.initreadtxt(bsdtxt)
    bsd = idf.idfobjects["BuildingSurface:Detailed".upper()][0]
    surf = simplesurface.wallunderground(
        idf, bsd, deletebsd=True,
        setto000=True)
    newidttxt = simpleobjtxt
    newidf = IDF()
    newidf.initreadtxt(newidttxt)
    assert idf.__almostequal__(newidf)


def test_wallinterzone():
    """py.test for wallinterzone"""
    bsdtxt = """BuildingSurface:Detailed, WALL-1PF, WALL, WALL-1, PLENUM-1,
    Surface, gumby, SunExposed, WindExposed, 0.5, 4, 0.0, 0.0, 3.0, 0.0, 0.0,
    2.4, 30.5, 0.0, 2.4, 30.5, 0.0, 3.0;
"""
    simpleobjtxt = """WALL:INTERZONE, WALL-1PF, WALL-1, PLENUM-1, gumby, 180.0,
    90.0, 0, 0, 0, 30.5, 0.6;"""
    idf = IDF()
    idf.initreadtxt(bsdtxt)
    bsd = idf.idfobjects["BuildingSurface:Detailed".upper()][0]
    surf = simplesurface.wallinterzone(
        idf, bsd, deletebsd=False,
        setto000=True)
    newidttxt = bsdtxt + simpleobjtxt
    newidf = IDF()
    newidf.initreadtxt(newidttxt)
    assert idf.__almostequal__(newidf)

    # test  for deletebsd = True
    idf = IDF()
    idf.initreadtxt(bsdtxt)
    bsd = idf.idfobjects["BuildingSurface:Detailed".upper()][0]
    surf = simplesurface.wallinterzone(idf, bsd, deletebsd=True, setto000=True)
    newidttxt = simpleobjtxt
    newidf = IDF()
    newidf.initreadtxt(newidttxt)
    assert idf.__almostequal__(newidf)


def test_roof():
    """py.test for roof"""
    bsdtxt = """BuildingSurface:Detailed, WALL-1PF, roof, WALL-1, PLENUM-1, , ,
    SunExposed, WindExposed, 0.5, 4, 0.0, 0.0, 3.0, 0.0, 0.0, 2.4, 30.5, 0.0,
    2.4, 30.5, 0.0, 3.0;
"""
    simpleobjtxt = """ROOF, WALL-1PF, WALL-1, PLENUM-1, 180.0, 90.0, 0, 0, 0, 30.5, 0.6;"""
    idf = IDF()
    idf.initreadtxt(bsdtxt)
    bsd = idf.idfobjects["BuildingSurface:Detailed".upper()][0]
    surf = simplesurface.roof(idf, bsd, deletebsd=False, setto000=True)
    newidttxt = bsdtxt + simpleobjtxt
    newidf = IDF()
    newidf.initreadtxt(newidttxt)
    assert idf.__almostequal__(newidf)

    # test  for deletebsd = True
    idf = IDF()
    idf.initreadtxt(bsdtxt)
    bsd = idf.idfobjects["BuildingSurface:Detailed".upper()][0]
    surf = simplesurface.roof(idf, bsd, deletebsd=True, setto000=True)
    newidttxt = simpleobjtxt
    newidf = IDF()
    newidf.initreadtxt(newidttxt)
    assert idf.__almostequal__(newidf)


def test_ceilingadiabatic():
    """py.test for ceilingadiabatic"""
    bsdtxt = """BuildingSurface:Detailed, WALL-1PF, ceiling, WALL-1, PLENUM-1,
    Adiabatic, , SunExposed, WindExposed, 0.5, 4, 0.0, 0.0, 3.0, 0.0, 0.0, 2.4,
    30.5, 0.0, 2.4, 30.5, 0.0, 3.0;
"""
    simpleobjtxt = """CEILING:ADIABATIC, WALL-1PF, WALL-1, PLENUM-1, 180.0,
    90.0, 0, 0, 0, 30.5, 0.6;"""
    idf = IDF()
    idf.initreadtxt(bsdtxt)
    bsd = idf.idfobjects["BuildingSurface:Detailed".upper()][0]
    surf = simplesurface.ceilingadiabatic(
        idf, bsd, deletebsd=False,
        setto000=True)
    newidttxt = bsdtxt + simpleobjtxt
    newidf = IDF()
    newidf.initreadtxt(newidttxt)
    assert idf.__almostequal__(newidf)

    # test  for deletebsd = True
    idf = IDF()
    idf.initreadtxt(bsdtxt)
    bsd = idf.idfobjects["BuildingSurface:Detailed".upper()][0]
    surf = simplesurface.ceilingadiabatic(
        idf, bsd, deletebsd=True,
        setto000=True)
    newidttxt = simpleobjtxt
    newidf = IDF()
    newidf.initreadtxt(newidttxt)
    assert idf.__almostequal__(newidf)


def test_ceilinginterzone():
    """py.test for ceilinginterzone"""
    bsdtxt = """BuildingSurface:Detailed, WALL-1PF, ceiling, WALL-1, PLENUM-1,
    Surface, gumby, SunExposed, WindExposed, 0.5, 4, 0.0, 0.0, 3.0, 0.0, 0.0,
    2.4, 30.5, 0.0, 2.4, 30.5, 0.0, 3.0;
"""
    simpleobjtxt = """CEILING:INTERZONE, WALL-1PF, WALL-1, PLENUM-1, gumby,
    180.0, 90.0, 0, 0, 0, 30.5, 0.6;"""
    idf = IDF()
    idf.initreadtxt(bsdtxt)
    bsd = idf.idfobjects["BuildingSurface:Detailed".upper()][0]
    surf = simplesurface.ceilinginterzone(
        idf, bsd, deletebsd=False,
        setto000=True)
    newidttxt = bsdtxt + simpleobjtxt
    newidf = IDF()
    newidf.initreadtxt(newidttxt)
    assert idf.__almostequal__(newidf)

    # test  for deletebsd = True
    idf = IDF()
    idf.initreadtxt(bsdtxt)
    bsd = idf.idfobjects["BuildingSurface:Detailed".upper()][0]
    surf = simplesurface.ceilinginterzone(
        idf, bsd, deletebsd=True,
        setto000=True)
    newidttxt = simpleobjtxt
    newidf = IDF()
    newidf.initreadtxt(newidttxt)
    assert idf.__almostequal__(newidf)


def test_floorgroundcontact():
    """py.test for floorgroundcontact"""
    bsdtxt = """BuildingSurface:Detailed, WALL-1PF, floor, WALL-1, PLENUM-1,
    Ground, , SunExposed, WindExposed, 0.5, 4, 0.0, 0.0, 3.0, 0.0, 0.0, 2.4,
    30.5, 0.0, 2.4, 30.5, 0.0, 3.0;
"""
    simpleobjtxt = """FLOOR:GROUNDCONTACT, WALL-1PF, WALL-1, PLENUM-1, 180.0,
    90.0, 0, 0, 0, 30.5, 0.6;"""
    idf = IDF()
    idf.initreadtxt(bsdtxt)
    bsd = idf.idfobjects["BuildingSurface:Detailed".upper()][0]
    surf = simplesurface.floorgroundcontact(
        idf, bsd, deletebsd=False,
        setto000=True)
    newidttxt = bsdtxt + simpleobjtxt
    newidf = IDF()
    newidf.initreadtxt(newidttxt)
    assert idf.__almostequal__(newidf)

    # test  for deletebsd = True
    idf = IDF()
    idf.initreadtxt(bsdtxt)
    bsd = idf.idfobjects["BuildingSurface:Detailed".upper()][0]
    surf = simplesurface.floorgroundcontact(
        idf, bsd, deletebsd=True,
        setto000=True)
    newidttxt = simpleobjtxt
    newidf = IDF()
    newidf.initreadtxt(newidttxt)
    assert idf.__almostequal__(newidf)


def test_flooradiabatic():
    """py.test for flooradiabatic"""
    bsdtxt = """BuildingSurface:Detailed, WALL-1PF, floor, WALL-1, PLENUM-1,
    Adiabatic, , SunExposed, WindExposed, 0.5, 4, 0.0, 0.0, 3.0, 0.0, 0.0, 2.4,
    30.5, 0.0, 2.4, 30.5, 0.0, 3.0;
"""
    simpleobjtxt = """FLOOR:ADIABATIC, WALL-1PF, WALL-1, PLENUM-1, 180.0, 90.0,
    0, 0, 0, 30.5, 0.6;"""
    idf = IDF()
    idf.initreadtxt(bsdtxt)
    bsd = idf.idfobjects["BuildingSurface:Detailed".upper()][0]
    surf = simplesurface.flooradiabatic(
        idf, bsd, deletebsd=False,
        setto000=True)
    newidttxt = bsdtxt + simpleobjtxt
    newidf = IDF()
    newidf.initreadtxt(newidttxt)
    assert idf.__almostequal__(newidf)

    # test  for deletebsd = True
    idf = IDF()
    idf.initreadtxt(bsdtxt)
    bsd = idf.idfobjects["BuildingSurface:Detailed".upper()][0]
    surf = simplesurface.flooradiabatic(
        idf, bsd, deletebsd=True,
        setto000=True)
    newidttxt = simpleobjtxt
    newidf = IDF()
    newidf.initreadtxt(newidttxt)
    assert idf.__almostequal__(newidf)


def test_floorinterzone():
    """py.test for floorinterzone"""
    bsdtxt = """BuildingSurface:Detailed, WALL-1PF, floor, WALL-1, PLENUM-1,
    Zone, gumby, SunExposed, WindExposed, 0.5, 4, 0.0, 0.0, 3.0, 0.0, 0.0, 2.4,
    30.5, 0.0, 2.4, 30.5, 0.0, 3.0;
"""
    simpleobjtxt = """FLOOR:INTERZONE, WALL-1PF, WALL-1, PLENUM-1, gumby,
    180.0, 90.0, 0, 0, 0, 30.5, 0.6;"""
    idf = IDF()
    idf.initreadtxt(bsdtxt)
    bsd = idf.idfobjects["BuildingSurface:Detailed".upper()][0]
    surf = simplesurface.floorinterzone(
        idf, bsd, deletebsd=False,
        setto000=True)
    newidttxt = bsdtxt + simpleobjtxt
    newidf = IDF()
    newidf.initreadtxt(newidttxt)
    assert idf.__almostequal__(newidf)

    # test  for deletebsd = True
    idf = IDF()
    idf.initreadtxt(bsdtxt)
    bsd = idf.idfobjects["BuildingSurface:Detailed".upper()][0]
    surf = simplesurface.floorinterzone(
        idf, bsd, deletebsd=True,
        setto000=True)
    newidttxt = simpleobjtxt
    newidf = IDF()
    newidf.initreadtxt(newidttxt)
    assert idf.__almostequal__(newidf)


def test_window():
    """py.test for window"""
    fsdtxt = """FenestrationSurface:Detailed, WF-1, WINDOW, 
    Dbl Clr 3mm/13mm Air, FRONT-1, , 0.5, , , 1, 4, 3.0, 0.0, 2.1, 3.0, 0.0, 
    0.9, 16.8, 0.0,
    0.9, 16.8, 0.0, 2.1;"""
    simpleobjtxt = """WINDOW, WF-1, Dbl Clr 3mm/13mm Air, FRONT-1, , , 1, 0, 0,
    13.8, 1.2;"""
    idf = IDF()
    idf.initreadtxt(fsdtxt)
    fsd = idf.idfobjects["FenestrationSurface:Detailed".upper()][0]
    surf = simplesurface.window(idf, fsd, deletebsd=False, setto000=True)
    newidttxt = fsdtxt + simpleobjtxt
    newidf = IDF()
    newidf.initreadtxt(newidttxt)
    assert idf.__almostequal__(newidf)

    # test  for deletebsd = True
    idf = IDF()
    idf.initreadtxt(fsdtxt)
    fsd = idf.idfobjects["FenestrationSurface:Detailed".upper()][0]
    surf = simplesurface.window(idf, fsd, deletebsd=True, setto000=True)
    newidttxt = simpleobjtxt
    newidf = IDF()
    newidf.initreadtxt(newidttxt)
    assert idf.__almostequal__(newidf)


def test_door():
    """py.test for window"""
    fsdtxt = """FenestrationSurface:Detailed, WR-1, door, Dbl Clr 3mm/13mm Air,
    RIGHT-1, , 0.5, , , 1, 4, 30.5, 3.8, 2.1, 30.5, 3.8, 0.9, 30.5, 11.4, 0.9,
    30.5, 11.4, 2.1;"""
    simpleobjtxt = """DOOR, WR-1, Dbl Clr 3mm/13mm Air, RIGHT-1, 1, 0, 0, 7.6,
    1.2;"""
    idf = IDF()
    idf.initreadtxt(fsdtxt)
    fsd = idf.idfobjects["FenestrationSurface:Detailed".upper()][0]
    surf = simplesurface.door(idf, fsd, deletebsd=False, setto000=True)
    newidttxt = fsdtxt + simpleobjtxt
    newidf = IDF()
    newidf.initreadtxt(newidttxt)
    assert idf.__almostequal__(newidf)

    # test  for deletebsd = True
    idf = IDF()
    idf.initreadtxt(fsdtxt)
    fsd = idf.idfobjects["FenestrationSurface:Detailed".upper()][0]
    surf = simplesurface.door(idf, fsd, deletebsd=True, setto000=True)
    newidttxt = simpleobjtxt
    newidf = IDF()
    newidf.initreadtxt(newidttxt)
    assert idf.__almostequal__(newidf)


def test_glazeddoor():
    """py.test for glazeddoor"""
    fsdtxt = """FenestrationSurface:Detailed, DF-1, GLASSDOOR, Sgl Grey 3mm,
    FRONT-1, , 0.5, , , 1, 4, 21.3, 0.0, 2.1, 21.3, 0.0, 0.0, 23.8, 0.0, 0.0,
    23.8, 0.0, 2.1;"""
    simpleobjtxt = """GLAZEDDOOR, DF-1, Sgl Grey 3mm, FRONT-1, , , 1, 0, 0,
    2.5, 2.1;"""
    idf = IDF()
    idf.initreadtxt(fsdtxt)
    fsd = idf.idfobjects["FenestrationSurface:Detailed".upper()][0]
    surf = simplesurface.glazeddoor(idf, fsd, deletebsd=False, setto000=True)
    newidttxt = fsdtxt + simpleobjtxt
    newidf = IDF()
    newidf.initreadtxt(newidttxt)
    assert idf.__almostequal__(newidf)

    # test  for deletebsd = True
    idf = IDF()
    idf.initreadtxt(fsdtxt)
    fsd = idf.idfobjects["FenestrationSurface:Detailed".upper()][0]
    surf = simplesurface.glazeddoor(idf, fsd, deletebsd=True, setto000=True)
    newidttxt = simpleobjtxt
    newidf = IDF()
    newidf.initreadtxt(newidttxt)
    assert idf.__almostequal__(newidf)
