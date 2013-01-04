"""py.test for examples. (ex_*.py files)"""
from idfreader import idfreader
import snippet
import os

# iddfile = "../iddfiles/Energy+V7_0_0_036.idd"
# fname = "../idffiles/V_7_0/5ZoneSupRetPlenRAB.idf"

iddsnippet = snippet.iddsnippet
idfsnippet = snippet.idfsnippet

from StringIO import StringIO
idffhandle = StringIO(idfsnippet)
iddfhandle = StringIO(iddsnippet)
bunchdt, data, commdct = idfreader(idffhandle, iddfhandle)

def test_readwrite():
    """py.test for ex_readwrite"""
    txt = str(data)
    head = 'Zone,\n     PLENUM-1,\n     0,\n     0,\n     0,\n     0,\n     1,\n     1,\n     0.609600067,\n     283.2;\n\n'
    print txt[:100]
    assert head == txt[:100]
    tail = ';\n\nZone,\n     Sup-PLENUM-1,\n     0,\n     0,\n     0,\n     0,\n     1,\n     1,\n     0.45,\n     208.6;\n\n'
    assert tail == txt[-100:]
    
def test_pythonic():
    """py.test for ex_pythonic.py"""
    zones = bunchdt['zone'.upper()] # all the zones
    zone0 = zones[0]
    print zone0
    # - 
    printout = "PLENUM-1"
    assert zone0.Name == printout
    # - 
    printout = ['PLENUM-1', 'SPACE1-1', 'SPACE2-1', 'SPACE3-1', 'SPACE4-1', 
        'SPACE5-1', 'Sup-PLENUM-1']
    zonenames = [zone.Name for zone in zones]
    assert printout == zonenames
    # - 
    printout = ['283.2', '239.247360229', '103.311355591', '239.247360229', 
        '103.311355591', '447.682556152', '208.6']
    zonevolumes = [zone.Volume for zone in zones]
    assert printout == zonevolumes
    # - 
    printout = [('SPACE2-1', '103.311355591'), ('SPACE4-1', '103.311355591')]
    smallzones = [zn for zn in zones if float(zn.Volume) < 150]
    namevolume = [(zn.Name, zn.Volume) for zn in smallzones]
    assert printout == namevolume
    # - 
    printout = 2
    assert printout == len(smallzones)
    # - 
    printout = ['PLENUM-1', 'SPACE1-1', 'FIRST-SMALL-ZONE', 'SPACE3-1', 
        'SECOND-SMALL-ZONE', 'SPACE5-1', 'Sup-PLENUM-1']
    smallzones[0].Name = "FIRST-SMALL-ZONE"
    smallzones[1].Name = "SECOND-SMALL-ZONE"
    # now the zone names are:
    zonenames = [zone.Name for zone in zones]
    assert printout == zonenames
    

