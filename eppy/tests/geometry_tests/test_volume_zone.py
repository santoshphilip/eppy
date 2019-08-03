# Copyright (c) 2012 Tuan Tran
# =======================================================================
#  Distributed under the MIT License.
#  (See accompanying file LICENSE or copy at
#  http://opensource.org/licenses/MIT)
# =======================================================================

"""pytest for volume_zone.py"""
# Wrote by Tuan Tran trantuan@hawaii.edu / tranhuuanhtuan@gmail.com
# School of Architecture, University of Hawaii at Manoa
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import eppy.geometry.volume_zone as volume_zone
from eppy.pytest_helpers import almostequal


def test_volume():
    """py.test for volume"""
    data = (
        (
            [(0, 0, 0), (1, 0, 0), (1, 1, 0), (0, 1, 0)],
            [(0, 0, 1), (1, 0, 1), (1, 1, 1), (0, 1, 1)],
            1,
        ),  # poly1, poly2, answer
        (
            [(0, 0, 0), (1, 0, 0), (1, 1, 0), (0, 1, 0)],
            [(0, 0, 0), (1, 0, 0), (1, 1, 2), (0, 1, 2)],
            1,
        ),  # poly1, poly2, answer
    )
    for poly1, poly2, answer in data:
        result = volume_zone.vol(poly1, poly2)
        assert almostequal(answer, result, places=4) == True
