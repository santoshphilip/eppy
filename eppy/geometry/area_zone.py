# Copyright (c) 2012 Tuan Tran
# =======================================================================
#  Distributed under the MIT License.
#  (See accompanying file LICENSE or copy at
#  http://opensource.org/licenses/MIT)
# =======================================================================

""""This module is used for calculation of zone area for E+ surfaces"""
# Wrote by Tuan Tran trantuan@hawaii.edu / tranhuuanhtuan@gmail.com
# School of Architecture, University of Hawaii at Manoa
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

# import area_surface as surf
import eppy.geometry.surface as surface


def area(poly):
    """Calculation of zone area"""
    poly_xy = []
    num = len(poly)
    for i in range(num):
        poly[i] = poly[i][0:2] + (0,)
        poly_xy.append(poly[i])
    return surface.area(poly)
