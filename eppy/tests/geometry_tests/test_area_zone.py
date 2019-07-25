# Copyright (c) 2012 Tuan Tran
# =======================================================================
#  Distributed under the MIT License.
#  (See accompanying file LICENSE or copy at
#  http://opensource.org/licenses/MIT)
# =======================================================================

""" pytest for area_zone.py"""
# Wrote by Tuan Tran trantuan@hawaii.edu / tranhuuanhtuan@gmail.com
# School of Architecture, University of Hawaii at Manoa
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import eppy.geometry.area_zone as area_zone
from eppy.pytest_helpers import almostequal


def test_area():
    """test for area of a zone"""

    data = (
        ([(0, 0, 0), (1, 0, 1), (1, 1, 0), (0, 1, 1)], 1),  # polygon, answer,
        ([(0, 0, 0), (1, 0, 0), (1, 0, 1), (0, 0, 1)], 0),
        ([(0, 0, 0), (0, 1, 0), (0, 1, 1), (0, 0, 1)], 0),
        ([(0, 0, 4), (5, 0, 4), (5, 5, 6), (0, 5, 6)], 25),
    )
    for poly, answer in data:
        result = area_zone.area(poly)
        assert almostequal(answer, result, places=4) == True
