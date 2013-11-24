"""py.test for simplesurface.py"""

from eppy import simplesurface
from eppy import modeleditor
from eppy.modeleditor import IDF
from eppy import simplesurface

def test_wallexterior():
    """py.test for wallexterior"""
    bsdtxt = """BuildingSurface:Detailed, WALL-1PF, WALL, WALL-1, PLENUM-1, Outdoors, , SunExposed, WindExposed, 0.5, 4, 0.0, 0.0, 3.0, 0.0, 0.0, 2.4, 30.5, 0.0, 2.4, 30.5, 0.0, 3.0;
"""
    simpleobjtxt = """WALL:EXTERIOR, WALL-1PF, WALL-1, PLENUM-1, 180.0, 90.0, 0, 0, 0, 30.5, 0.6;"""
    idf = IDF()
    idf.initreadtxt(bsdtxt)
    bsd = idf.idfobjects["BuildingSurface:Detailed".upper()][0]
    w_ext = simplesurface.wallexterior(idf, bsd, setto000=True)
    newidttxt = bsdtxt + simpleobjtxt
    newidf = IDF()
    newidf.initreadtxt(newidttxt)
    assert idf.idfstr() == newidf.idfstr()
    
def test_walladiabatic():
    """py.test for walladiabatic"""
    bsdtxt = """BuildingSurface:Detailed, WALL-1PF, WALL, WALL-1, PLENUM-1, Adiabatic, , SunExposed, WindExposed, 0.5, 4, 0.0, 0.0, 3.0, 0.0, 0.0, 2.4, 30.5, 0.0, 2.4, 30.5, 0.0, 3.0;
"""
    simpleobjtxt = """WALL:ADIABATIC, WALL-1PF, WALL-1, PLENUM-1, 180.0, 90.0, 0, 0, 0, 30.5, 0.6;"""
    idf = IDF()
    idf.initreadtxt(bsdtxt)
    bsd = idf.idfobjects["BuildingSurface:Detailed".upper()][0]
    w_ext = simplesurface.walladiabatic(idf, bsd, setto000=True)
    newidttxt = bsdtxt + simpleobjtxt
    newidf = IDF()
    newidf.initreadtxt(newidttxt)
    assert idf.idfstr() == newidf.idfstr()

def test_wallunderground():
    """py.test for wallunderground"""
    bsdtxt = """BuildingSurface:Detailed, WALL-1PF, WALL, WALL-1, PLENUM-1, Ground, , SunExposed, WindExposed, 0.5, 4, 0.0, 0.0, 3.0, 0.0, 0.0, 2.4, 30.5, 0.0, 2.4, 30.5, 0.0, 3.0;
"""
    simpleobjtxt = """WALL:UNDERGROUND, WALL-1PF, WALL-1, PLENUM-1, 180.0, 90.0, 0, 0, 0, 30.5, 0.6;"""
    idf = IDF()
    idf.initreadtxt(bsdtxt)
    bsd = idf.idfobjects["BuildingSurface:Detailed".upper()][0]
    w_ext = simplesurface.wallunderground(idf, bsd, setto000=True)
    newidttxt = bsdtxt + simpleobjtxt
    newidf = IDF()
    newidf.initreadtxt(newidttxt)
    assert idf.idfstr() == newidf.idfstr()

def test_wallinterzone():
    """py.test for wallinterzone"""
    bsdtxt = """BuildingSurface:Detailed, WALL-1PF, WALL, WALL-1, PLENUM-1, Surface, gumby, SunExposed, WindExposed, 0.5, 4, 0.0, 0.0, 3.0, 0.0, 0.0, 2.4, 30.5, 0.0, 2.4, 30.5, 0.0, 3.0;
"""
    simpleobjtxt = """WALL:INTERZONE, WALL-1PF, WALL-1, PLENUM-1, gumby, 180.0, 90.0, 0, 0, 0, 30.5, 0.6;"""
    idf = IDF()
    idf.initreadtxt(bsdtxt)
    bsd = idf.idfobjects["BuildingSurface:Detailed".upper()][0]
    w_ext = simplesurface.wallinterzone(idf, bsd, setto000=True)
    newidttxt = bsdtxt + simpleobjtxt
    newidf = IDF()
    newidf.initreadtxt(newidttxt)
    idf.saveas('idf.idf')
    newidf.saveas('new.idf')
    assert idf.idfstr() == newidf.idfstr()

def test_roof():
    """py.test for roof"""
    bsdtxt = """BuildingSurface:Detailed, WALL-1PF, roof, WALL-1, PLENUM-1, , , SunExposed, WindExposed, 0.5, 4, 0.0, 0.0, 3.0, 0.0, 0.0, 2.4, 30.5, 0.0, 2.4, 30.5, 0.0, 3.0;
"""
    simpleobjtxt = """ROOF, WALL-1PF, WALL-1, PLENUM-1, 180.0, 90.0, 0, 0, 0, 30.5, 0.6;"""
    idf = IDF()
    idf.initreadtxt(bsdtxt)
    bsd = idf.idfobjects["BuildingSurface:Detailed".upper()][0]
    w_ext = simplesurface.roof(idf, bsd, setto000=True)
    newidttxt = bsdtxt + simpleobjtxt
    newidf = IDF()
    newidf.initreadtxt(newidttxt)
    assert idf.idfstr() == newidf.idfstr()
    
def test_ceilingadiabatic():
    """py.test for ceilingadiabatic"""
    bsdtxt = """BuildingSurface:Detailed, WALL-1PF, ceiling, WALL-1, PLENUM-1, Adiabatic, , SunExposed, WindExposed, 0.5, 4, 0.0, 0.0, 3.0, 0.0, 0.0, 2.4, 30.5, 0.0, 2.4, 30.5, 0.0, 3.0;
"""
    simpleobjtxt = """CEILING:ADIABATIC, WALL-1PF, WALL-1, PLENUM-1, 180.0, 90.0, 0, 0, 0, 30.5, 0.6;"""
    idf = IDF()
    idf.initreadtxt(bsdtxt)
    bsd = idf.idfobjects["BuildingSurface:Detailed".upper()][0]
    w_ext = simplesurface.ceilingadiabatic(idf, bsd, setto000=True)
    newidttxt = bsdtxt + simpleobjtxt
    newidf = IDF()
    newidf.initreadtxt(newidttxt)
    assert idf.idfstr() == newidf.idfstr()

def test_ceilinginterzone():
    """py.test for ceilinginterzone"""
    bsdtxt = """BuildingSurface:Detailed, WALL-1PF, ceiling, WALL-1, PLENUM-1, Surface, gumby, SunExposed, WindExposed, 0.5, 4, 0.0, 0.0, 3.0, 0.0, 0.0, 2.4, 30.5, 0.0, 2.4, 30.5, 0.0, 3.0;
"""
    simpleobjtxt = """CEILING:INTERZONE, WALL-1PF, WALL-1, PLENUM-1, gumby, 180.0, 90.0, 0, 0, 0, 30.5, 0.6;"""
    idf = IDF()
    idf.initreadtxt(bsdtxt)
    bsd = idf.idfobjects["BuildingSurface:Detailed".upper()][0]
    w_ext = simplesurface.ceilinginterzone(idf, bsd, setto000=True)
    newidttxt = bsdtxt + simpleobjtxt
    newidf = IDF()
    newidf.initreadtxt(newidttxt)
    idf.saveas('idf.idf')
    newidf.saveas('new.idf')
    assert idf.idfstr() == newidf.idfstr()

def test_floorgroundcontact():
    """py.test for floorgroundcontact"""
    bsdtxt = """BuildingSurface:Detailed, WALL-1PF, floor, WALL-1, PLENUM-1, Ground, , SunExposed, WindExposed, 0.5, 4, 0.0, 0.0, 3.0, 0.0, 0.0, 2.4, 30.5, 0.0, 2.4, 30.5, 0.0, 3.0;
"""
    simpleobjtxt = """FLOOR:GROUNDCONTACT, WALL-1PF, WALL-1, PLENUM-1, 180.0, 90.0, 0, 0, 0, 30.5, 0.6;"""
    idf = IDF()
    idf.initreadtxt(bsdtxt)
    bsd = idf.idfobjects["BuildingSurface:Detailed".upper()][0]
    w_ext = simplesurface.floorgroundcontact(idf, bsd, setto000=True)
    newidttxt = bsdtxt + simpleobjtxt
    newidf = IDF()
    newidf.initreadtxt(newidttxt)
    assert idf.idfstr() == newidf.idfstr()

