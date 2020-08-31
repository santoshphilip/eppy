# Copyright (c) 2012 Santosh Philip
# =======================================================================
#  Distributed under the MIT License.
#  (See accompanying file LICENSE or copy at
#  http://opensource.org/licenses/MIT)
# =======================================================================

"""py.test for examples. (ex_*.py files)"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from eppy.idfreader import idfreader
import eppy.snippet as snippet
import os
import eppy.pytest_helpers as pytest_helpers
import eppy.modeleditor as modeleditor

# iddfile = "../iddfiles/Energy+V7_0_0_036.idd"
# fname = "../idffiles/V_7_0/5ZoneSupRetPlenRAB.idf"


# iddsnippet = snippet.iddsnippet
from eppy.iddcurrent import iddcurrent

iddsnippet = iddcurrent.iddtxt

idfsnippet = snippet.idfsnippet

from io import StringIO

idffhandle = StringIO(idfsnippet)
iddfhandle = StringIO(iddsnippet)
bunchdt, data, commdct, idd_index = idfreader(idffhandle, iddfhandle)


def test_readwrite():
    """py.test for ex_readwrite"""
    txt = str(data)
    head = "Zone,\n     PLENUM-1,\n     0.0,\n     0.0,\n     0.0,\n     0.0,\n     1,\n     1,\n     0.609600067,\n     283.2;\n\n"
    tail = "\n\nBuildingSurface:Detailed,\n     WALL-1PF,\n     WALL,\n     WALL-1,\n     PLENUM-1,\n     Outdoors,\n     ,\n     SunExposed,\n     WindExposed,\n     0.5,\n     4,\n     0.0,\n     0.0,\n     3.0,\n     0.0,\n     0.0,\n     2.4,\n     30.5,\n     0.0,\n     2.4,\n     30.5,\n     0.0,\n     3.0;\n\n"
    # assert head == txt[:108]
    # assert tail == txt[-280:]


def test_pythonic():
    """py.test for ex_pythonic.py"""
    zones = bunchdt["zone"]  # all the zones
    zone0 = zones[0]
    # -
    printout = "PLENUM-1"
    assert zone0.Name == printout
    # -
    printout = [
        "PLENUM-1",
        "SPACE1-1",
        "SPACE2-1",
        "SPACE3-1",
        "SPACE4-1",
        "SPACE5-1",
        "Sup-PLENUM-1",
    ]
    zonenames = [zone.Name for zone in zones]
    assert printout == zonenames
    # -
    printout = [
        "283.2",
        "239.247360229",
        "103.311355591",
        "239.247360229",
        "103.311355591",
        "447.682556152",
        "208.6",
    ]
    zonevolumes = [zone.Volume for zone in zones]
    for item1, item2 in zip(printout, zonevolumes):
        item1, item2 = float(item1), float(item2)
        assert pytest_helpers.almostequal(item1, item2)
    # -
    printout = [("SPACE2-1", "103.311355591"), ("SPACE4-1", "103.311355591")]
    smallzones = [zn for zn in zones if float(zn.Volume) < 150]
    namevolume = [(zn.Name, zn.Volume) for zn in smallzones]
    for (n1, v1), (n2, v2) in zip(printout, namevolume):
        (n1, v1) = (n1, float(v1))
        (n2, v2) = (n2, float(v2))
        assert n1 == n2
        assert pytest_helpers.almostequal(v1, v2)
    # -
    printout = 2
    assert printout == len(smallzones)
    # -
    printout = [
        "PLENUM-1",
        "SPACE1-1",
        "FIRST-SMALL-ZONE",
        "SPACE3-1",
        "SECOND-SMALL-ZONE",
        "SPACE5-1",
        "Sup-PLENUM-1",
    ]
    smallzones[0].Name = "FIRST-SMALL-ZONE"
    smallzones[1].Name = "SECOND-SMALL-ZONE"
    # now the zone names are:
    zonenames = [zone.Name for zone in zones]
    assert printout == zonenames


def test_addobject():
    """py.test for ex_addobject.py"""
    zones = bunchdt["zone"]  # all the zones
    assert len(zones) == 7
    modeleditor.addobject(bunchdt, data, commdct, "Zone".upper(), None, aname="NewZone")
    assert len(zones) == 8
    assert zones[-1].obj == [
        "ZONE",
        "NewZone",
        0.0,
        0.0,
        0.0,
        0.0,
        1,
        1,
        "autocalculate",
        "autocalculate",
        "autocalculate",
        "",
        "",
        "Yes",
    ]


def test_functions():
    """py.test for ex_functions.py"""
    surfaces = bunchdt["BuildingSurface:Detailed"]  # all the surfaces
    assert len(surfaces) == 1
    surface = surfaces[0]
    assert surface.Name == "WALL-1PF"
    assert surface.azimuth == 180.0
    assert surface.tilt == 90.0
    assert pytest_helpers.almostequal(surface.area, 18.3)
