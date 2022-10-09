# Copyright (c) 2022 Santosh Philip
# =======================================================================
#  Distributed under the MIT License.
#  (See accompanying file LICENSE or copy at
#  http://opensource.org/licenses/MIT)
# =======================================================================

"""py.tests for ext_field_functions.py"""

import pytest
import eppy.ext_field_functions as extff


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
        result = extff.getextensible(objidd)
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
        result = extff.extension_of_extensible(objidd, objblock, n)
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
        result = extff.endof_extensible(extensible, thisblock)
        assert result == expected


@pytest.mark.parametrize(
    "objidd, afieldname, expected",
    [
        (
            [
                {
                    "extensible:2": [
                        '- repeat last two fields remembering to remove ; from "inner" fields.'
                    ]
                },
                {"field": ["Name"]},
                {"field": ["Optical Data Temperature 1"], "begin-extensible": [""]},
                {"field": ["Window Material Glazing Name 1"]},
                {"field": ["Optical Data Temperature 2"]},
                {"field": ["Window Material Glazing Name 2"]},
            ],
            "Optical_Data_Temperature_32",
            True,
        ),  # objidd, afieldname, expected
        (
            [
                {
                    "extensible:2": [
                        '- repeat last two fields remembering to remove ; from "inner" fields.'
                    ]
                },
                {"field": ["Name"]},
                {"field": ["Optical Data Temperature 1"], "begin-extensible": [""]},
                {"field": ["Window Material Glazing Name 1"]},
                {"field": ["Optical Data Temperature 2"]},
                {"field": ["Window Material Glazing Name 2"]},
            ],
            "Gumby_800",
            False,
        ),  # objidd, afieldname, expected
        (
            [
                {
                    "extensible:2": [
                        '- repeat last two fields remembering to remove ; from "inner" fields.'
                    ]
                },
                {"field": ["Name"]},
                {"field": ["Optical Data Temperature 1"], "begin-extensible": [""]},
                {"field": ["Window Material Glazing Name 1"]},
                {"field": ["Optical Data Temperature 2"]},
                {"field": ["Window Material Glazing Name 2"]},
            ],
            "Optical_Data Temperature 32",
            False,
        ),  # objidd, afieldname, expected
    ],
)
def test_islegalextensiblefield(objidd, afieldname, expected):
    """py.test for islegalextensiblefield"""
    result = extff.islegalextensiblefield(objidd, afieldname)
    assert result == expected


@pytest.mark.parametrize(
    "fname, expected",
    [
        ("this_name_4", 4),  # fname, expected
        ("this_3_name_4", 4),  # fname, expected
        ("this_name", None),  # fname, expected
    ],
)
def test_extfieldint(fname, expected):
    """py.test for extfieldint"""
    result = extff.extfieldint(fname)
    assert result == expected
