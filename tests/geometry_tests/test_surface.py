# Copyright (c) 2012 Tuan Tran
# Copyright (c) 2020 Cheng Cui
# =======================================================================
#  Distributed under the MIT License.
#  (See accompanying file LICENSE or copy at
#  http://opensource.org/licenses/MIT)
# =======================================================================

"""pytest for surface.py"""
# Wrote by Tuan Tran trantuan@hawaii.edu / tranhuuanhtuan@gmail.com
# School of Architecture, University of Hawaii at Manoa
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import eppy.geometry.surface as surface
from eppy.pytest_helpers import almostequal
import pytest


def test_area():
    """test the area of a polygon poly"""
    data = (
        ([(0, 0, 0), (1, 0, 0), (1, 1, 0), (0, 1, 0)], 1),
        # polygon, expected,
        ([(0, 0, 0), (1, 0, 0), (1, 0, 1), (0, 0, 1)], 1),
        ([(0, 0, 0), (0, 1, 0), (0, 1, 1), (0, 0, 1)], 1),
        ([(0, 0, 0), (0, 1, 0), (0, 2, 0), (0, 3, 0)], 0),
        (
            [
                (-4.611479, 6.729214, -0.332978),
                (-0.694944, 4.990984, 2.243709),
                (-2.147088, 0.302854, 1.288344),
                (-6.063622, 2.041084, -1.288344),
            ],
            25,
        ),
        (
            [(0, 0, 0), (0.5, 0, 0), (1, 0, 0), (1, 0, 1), (0, 0, 1)],
            1,
        ),  # 1st 3 points are linear
        (
            [(0, 0, 0), (0.5, 0, 0), (1, 0, 0), (2, 0, 0), (3, 0, 0)],
            0,
        ),  # all points are linear
    )
    for poly, expected in data:
        result = surface.area(poly)
        assert almostequal(expected, result, places=4) == True


def test_height():
    """test the height of a polygon poly"""
    data = (
        ([(0, 0, 0), (1, 0, 0), (1, 1, 0), (0, 1, 0)], 1),
        # polygon, expected,
        ([(0, 0, 0), (8, 0, 0), (11, 0, 4), (3, 0, 4)], 5),
        ([(0, 0, 0), (10, 0, 0), (10, 9, 0), (0, 9, 0)], 9),
        (
            [
                (3.571913, -9.390334, 1.487381),
                (10.905826, -6.194443, 1.487381),
                (8.998819, -1.818255, 0.0),
                (1.664906, -5.014146, 0.0),
            ],
            5,
        ),
        ([(0.0, 0.0, 3.0), (0.0, 0.0, 2.4), (30.5, 0.0, 2.4), (30.5, 0.0, 3.0)], 0.6),
    )
    for poly, expected in data:
        result = surface.height(poly)
        assert almostequal(expected, result, places=5) == True


def test_width():
    """test the width of a polygon poly"""
    data = (
        ([(0, 0, 0), (1, 0, 0), (1, 1, 0), (0, 1, 0)], 1),
        # polygon, expected,
        ([(0, 0, 0), (8, 0, 0), (11, 0, 4), (3, 0, 4)], 8),
        ([(0, 0, 0), (10, 0, 0), (10, 9, 0), (0, 9, 0)], 10),
        (
            [
                (3.571913, -9.390334, 1.487381),
                (10.905826, -6.194443, 1.487381),
                (8.998819, -1.818255, 0.0),
                (1.664906, -5.014146, 0.0),
            ],
            8,
        ),
    )
    for poly, expected in data:
        result = surface.width(poly)
        assert almostequal(expected, result, places=4) == True


def test_azimuth():
    """test the azimuth of a polygon poly"""
    data = (
        ([(0, 0, 0), (1, 0, 0), (1, 1, 1), (0, 1, 1)], 180),
        # polygon, expected,
        ([(0, 0, 0), (1, 0, 0), (1, 1, 0), (0, 1, 0)], 0),
        (
            [
                (3.571913, -9.390334, 1.487381),
                (10.905826, -6.194443, 1.487381),
                (8.998819, -1.818255, 0.0),
                (1.664906, -5.014146, 0.0),
            ],
            360 - 23.546134,
        ),
    )
    for poly, expected in data:
        result = surface.azimuth(poly)
        assert almostequal(expected, result, places=3) == True


def test_true_azimuth():
    """test the true azimuth of a polygon poly"""
    data = (
        (45, 30, 0, 75),
        # bldg_north, zone_rel_north, surf_azimuth, expected,
        ("", 0, 180, 180),
        (20, "", 20, 40),
        (240, 90, 180, 150),
    )
    for (
        bldg_north,
        zone_rel_north,
        surf_azimuth,
        expected,
    ) in data:
        result = surface.true_azimuth(bldg_north, zone_rel_north, surf_azimuth)
        assert almostequal(expected, result, places=3) == True


def test_tilt():
    """test the tilt of a polygon poly"""
    data = (
        ([(0, 0, 0), (1, 0, 0), (1, 1, 0), (0, 1, 0)], 0),
        # polygon, expected,
        ([(0, 0, 0), (5, 0, 0), (5, 0, 8), (0, 0, 8)], 90),
        ([(0, 0, 0), (1, 0, 0), (1, 1, 1), (0, 1, 1)], 45),
        (
            [
                (3.571913, -9.390334, 1.487381),
                (10.905826, -6.194443, 1.487381),
                (8.998819, -1.818255, 0.0),
                (1.664906, -5.014146, 0.0),
            ],
            90 - 72.693912,
        ),
    )
    for poly, expected in data:
        result = surface.tilt(poly)
        assert almostequal(expected, result, places=3) == True


@pytest.mark.parametrize(
    "vertices, expected",
    [
        (
            ["A", "B", "C", "D"],
            [("D", "A", "B"), ("A", "B", "C"), ("B", "C", "D"), ("C", "D", "A")],
        )
    ],
)
def test_vertex3tuple(vertices, expected):
    """py.test for vertex3tuple"""
    result = surface.vertex3tuple(vertices)
    assert result == expected


@pytest.mark.parametrize(
    "pta, ptb, ptc, expected",
    [
        ((0, 0, 0), (1, 0, 0), (1, 1, 0), (0.0, 0.0, 1.0)),
        ((1, 0, 0), (1, 1, 0), (0, 1, 0), (0.0, 0.0, 1.0)),
        ((1, 1, 0), (0, 1, 0), (0, 0, 0), (0.0, 0.0, 1.0)),
        ((0, 1, 0), (0, 0, 0), (1, 0, 0), (0.0, 0.0, 1.0)),
    ],
)
def test_unit_normal(pta, ptb, ptc, expected):
    """py.test for unit_normal"""
    result = surface.unit_normal(pta, ptb, ptc)
    assert result == expected


@pytest.mark.parametrize(
    "poly, expected",
    [
        (
            [(0, 0, 0), (1, 0, 0), (1, 1, 0), (0, 1, 0)],
            (0.0, 0.0, 1.0),
        ),  # all non-linear
        (
            [(0, 0, 0), (0.5, 0, 0), (1, 0, 0), (1, 1, 0), (0, 1, 0)],
            (0.0, 0.0, 1.0),
        ),  # 1st 3 points are linear
        (
            [(0, 0, 0), (1, 0, 0), (1, 0.5, 0), (1, 1, 0), (0, 1, 0)],
            (0.0, 0.0, 1.0),
        ),  # all non-linear
        # ([(0, 0, 0), (1, 0, 0), (2, 0, 0), (3, 0, 0)],
        # (0.0, 0.0, 1.0)), # all linear
    ],
)
def test_get_an_unit_normal(poly, expected):
    """py.test for get_an_unit_normal"""
    result = surface.get_an_unit_normal(poly)
    assert result == expected


def test_get_an_unit_normal_ZeroDivisionError():
    """pytest for get_an_unit_normal ZeroDivisionError"""
    with pytest.raises(ZeroDivisionError):
        surface.get_an_unit_normal([(0, 0, 0), (1, 0, 0), (2, 0, 0), (3, 0, 0)])
