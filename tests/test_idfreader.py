# Copyright (c) 2012 Santosh Philip
# =======================================================================
#  Distributed under the MIT License.
#  (See accompanying file LICENSE or copy at
#  http://opensource.org/licenses/MIT)
# =======================================================================

"""pytest for idfreader. very few tests"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from io import StringIO

import eppy.idfreader as idfreader
from eppy.EPlusInterfaceFunctions import readidf

from eppy.iddcurrent import iddcurrent

iddfhandle = StringIO(iddcurrent.iddtxt)


def test_iddversiontuple():
    """py.test for iddversiontuple"""
    iddtxt = """stuff 9.8.4
    other stuff"""
    fhandle = StringIO(iddtxt)
    result = idfreader.iddversiontuple(fhandle)
    assert result == (9, 8, 4)


def test_convertafield():
    """py.test for convertafield"""
    data = (
        ({"type": "integer"}, "1", "N1", 1),
        # field_comm, field_val, field_iddname, expected
        ({}, "1", "N1", 1.0),
        # field_comm, field_val, field_iddname, expected
        ({"type": "real"}, "1", "N1", 1.0),
        # field_comm, field_val, field_iddname, expected
        ({}, "autosize", "N1", "autosize"),
        ({}, "4", "A1", "4"),
        # field_comm, field_val, field_iddname, expected
    )
    for field_comm, field_val, field_iddname, expected in data:
        result = idfreader.convertafield(field_comm, field_val, field_iddname)
        assert result == expected


def test_convertallfields():
    """py.test convertallfields"""
    data = (
        ("version, 8.1;", "VERSION", ["version", "8.1"]),
        # idfstr, objkey, expected
        (
            "WINDOWMATERIAL:SIMPLEGLAZINGSYSTEM, simple, 0.45;",
            "WINDOWMATERIAL:SIMPLEGLAZINGSYSTEM",
            ["WINDOWMATERIAL:SIMPLEGLAZINGSYSTEM", "simple", 0.45],
        ),
        # idfstr, objkey, expected
        (
            "HVACTEMPLATE:ZONE:FANCOIL, gumby1, gumby2, 0.45;",
            "HVACTEMPLATE:ZONE:FANCOIL",
            ["HVACTEMPLATE:ZONE:FANCOIL", "gumby1", "gumby2", 0.45],
        ),
        # idfstr, objkey, expected
        (
            "HVACTEMPLATE:ZONE:FANCOIL, gumby1, gumby2, autosize;",
            "HVACTEMPLATE:ZONE:FANCOIL",
            ["HVACTEMPLATE:ZONE:FANCOIL", "gumby1", "gumby2", "autosize"],
        ),
        # idfstr, objkey, expected
    )
    commdct = None
    block = None
    for idfstr, objkey, expected in data:
        idfhandle = StringIO(idfstr)
        block, data, commdct, idd_index = readidf.readdatacommdct1(
            idfhandle, iddfile=iddfhandle, commdct=commdct, block=block
        )
        idfreader.convertallfields(data, commdct, block)
        result = data.dt[objkey][0]
        assert result == expected
