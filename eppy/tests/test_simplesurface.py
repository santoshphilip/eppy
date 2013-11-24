"""py.test for simplesurface.py"""

from eppy import simplesurface

def test_add():
    """py.test for add"""
    assert simplesurface.add(2, 3) == 5
    
def test_wallexterior():
    """py.test for wallexterior"""
    bsdtxt = """BuildingSurface:Detailed, WALL-1PF, WALL, WALL-1, PLENUM-1, Outdoors, , SunExposed, WindExposed, 0.5, 4, 0.0, 0.0, 3.0, 0.0, 0.0, 2.4, 30.5, 0.0, 2.4, 30.5, 0.0, 3.0;
"""
    w_exttxt = """WALL:EXTERIOR, WALL-1PF, WALL-1, PLENUM-1, 180.0, 90.0, 0, 0, 0, 30.5, 0.6;"""
    