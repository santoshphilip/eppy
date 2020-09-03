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


def test_getextensible():
    """py.test for getextensible"""
    data = (
        (
            [
                {
                    "format": ["singleLine"],
                    "group": "Simulation Parameters",
                    "idfobj": "Version",
                    "memo": ["Specifies the EnergyPlus version of the IDF file."],
                    "unique-object": [""],
                },
                {},
                {},
                {},
            ],
            None,
        ),  # objidd, expected
        (
            [
                {
                    "extensible:2": [
                        '- repeat last two fields, remembering to remove ; from "inner" fields.'
                    ],
                    "group": "Schedules",
                    "idfobj": "Schedule:Day:Interval",
                    "memo": [
                        "A Schedule:Day:Interval contains a full day of values with specified end times for each value",
                        "Currently, is set up to allow for 10 minute intervals for an entire day.",
                    ],
                    "min-fields": ["5"],
                },
                {},
                {},
                {},
            ],
            2,
        ),  # objidd, expected
    )
    for objidd, expected in data:
        result = idfreader.getextensible(objidd)
        assert result == expected


def test_endof_extensible():
    """py.test for endof_extensible"""
    data = (
        (1, ["gumby", "A1", "A2"], ["A2"]),  # extensible, thisblock, expected
        (1, ["gumby", "A1", "A2", "A3"], ["A3"]),  # extensible, thisblock, expected
        (
            2,
            ["gumby", "A1", "A2", "A3"],
            ["A2", "A3"],
        ),  # extensible, thisblock, expected
    )
    for extensible, thisblock, expected in data:
        result = idfreader.endof_extensible(extensible, thisblock)
        assert result == expected


def test_extension_of_extensible():
    """py.test for extension_of_extensible"""
    data = (
        (
            [
                {
                    "extensible:1": None,
                    "group": "Schedules",
                    "idfobj": "Schedule:Day:Interval",
                },
                {},
                {},
                {},
            ],
            ["Gumby", "A1", "A2"],
            1,
            ["A3"],
        ),  # objidd, objblock, n, expected
        (
            [
                {
                    "extensible:1": None,
                    "group": "Schedules",
                    "idfobj": "Schedule:Day:Interval",
                },
                {},
                {},
                {},
            ],
            ["Gumby", "A1", "A2"],
            2,
            ["A3", "A4"],
        ),  # objidd, objblock, n, expected
        (
            [
                {
                    "extensible:1": None,
                    "group": "Schedules",
                    "idfobj": "Schedule:Day:Interval",
                },
                {},
                {},
                {},
            ],
            ["Gumby", "A1", "A2"],
            3,
            ["A3", "A4", "A5"],
        ),  # objidd, objblock, n, expected
        (
            [
                {
                    "extensible:2": None,
                    "group": "Schedules",
                    "idfobj": "Schedule:Day:Interval",
                },
                {},
                {},
                {},
            ],
            ["Gumby", "A1", "A2"],
            2,
            ["A3", "A4"],
        ),  # objidd, objblock, n, expected
        (
            [
                {
                    "extensible:4": None,
                    "group": "Schedules",
                    "idfobj": "Schedule:Day:Interval",
                },
                {},
                {},
                {},
            ],
            ["Gumby", "N3", "A4", "M8", "A5"],
            4,
            ["N4", "A6", "M9", "A7"],
        ),  # objidd, objblock, n, expected
        (
            [
                {
                    "extensible:4": None,
                    "group": "Schedules",
                    "idfobj": "Schedule:Day:Interval",
                },
                {},
                {},
                {},
            ],
            ["Gumby", "N3", "A4", "M8", "A5"],
            12,
            [
                "N4",
                "A6",
                "M9",
                "A7",
                "N5",
                "A8",
                "M10",
                "A9",
                "N6",
                "A10",
                "M11",
                "A11",
            ],
        ),  # objidd, objblock, n, expected
    )
    for objidd, objblock, n, expected in data:
        result = idfreader.extension_of_extensible(objidd, objblock, n)
        assert result == expected
