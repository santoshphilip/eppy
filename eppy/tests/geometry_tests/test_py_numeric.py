# Copyright (c) 2014 Eric Youngson

# This file is part of eppy.

# Eppy is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# Eppy is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with eppy.  If not, see <http://www.gnu.org/licenses/>.

"""pytest for py_numeric.py"""
# Written by Eric Youngson eric@successionecological.com / eayoungs@gmail.com
# Succession Ecological Services: Portland, Oregon

import eppy.geometry.py_numeric as py_numeric
from eppy.pytest_helpers import almostequal


def vctr_cross():
    """test the cross product of two 3 dimentional vectors"""

    # Vector cross-product.
    x = [1, 2, 3]
    y = [4, 5, 6]
    z = py_numeric.cross(x, y)

    assert z == [-3, 6, -3]


def vctr_dot():
    """test the dot product of two 3 dimentional vectors"""

    # Vector dot-product.
    x = [1, 2, 3]
    y = [4, 5, 6]
    z = py_numeric.dot(x, y)

    assert z == [4, 10, 18]
