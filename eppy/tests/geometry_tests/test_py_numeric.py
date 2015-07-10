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

import eppy.geometry.tinynumpy as py_numeric
from eppy.pytest_helpers import almostequal
import pytest


# Start vector cross product tests
def test_cross():
    """test the cross product of two 3 dimentional vectors"""

    # Vector cross-product.
    x = [1, 2, 3]
    y = [4, 5, 6]
    z = py_numeric.cross(x, y)

    assert z == [-3, 6, -3]


def test_2dim_cross():
    """test the cross product of two 2 dimentional vectors"""

    # 2 dim cross-product.
    x = [1, 2]
    y = [4, 5]

    with pytest.raises(IndexError) as execinfo:
        z = py_numeric.cross(x, y)

    assert 'Vector has invalid dimensions' in str(execinfo.value)


def test_4dim_cross():
    """test the cross product of two 2 dimentional vectors"""

    # 4 dim cross-product.
    x = [1, 2, 3, 4]
    y = [5, 6, 7, 8]

    with pytest.raises(IndexError) as execinfo:
        z = py_numeric.cross(x, y)

    assert 'Vector has invalid dimensions' in str(execinfo.value)


def test_mdim_cross():
    """test the cross product of two 4 dimentional vectors"""

    # Mixed dim cross-product.
    x = [1, 2, 3]
    y = [4, 5, 6, 7]

    with pytest.raises(IndexError) as execinfo:
        z = py_numeric.cross(x, y)

    assert 'Vector has invalid dimensions' in str(execinfo.value)


# Start vector dot product tests
def test_dot():
    """test the dot product of two mixed dimentional vectors"""

    # Vector dot-product.
    x = [1, 2, 3]
    y = [4, 5, 6]
    z = py_numeric.dot(x, y)

    assert z == 32


def test_2dim_dot():
    """test the dot product of two 2 dimentional vectors"""

    # 2 dim dot-product.
    x = [1, 2]
    y = [4, 5]

    with pytest.raises(IndexError) as execinfo:
        z = py_numeric.dot(x, y)

    assert 'Vector has invalid dimensions' in str(execinfo.value)


def test_4dim_dot():
    """test the dot product of two 4 dimentional vectors"""

    # 4 dim dot-product.
    x = [1, 2, 3, 4]
    y = [5, 6, 7, 8]

    with pytest.raises(IndexError) as execinfo:
        z = py_numeric.dot(x, y)

    assert 'Vector has invalid dimensions' in str(execinfo.value)


def test_mdim_dot():
    """test the dot product of two mixed dimentional vectors"""

    # Mixed dim dot-product.
    x = [1, 2, 3]
    y = [4, 5, 6, 7]

    with pytest.raises(IndexError) as execinfo:
        z = py_numeric.dot(x, y)

    assert 'Vector has invalid dimensions' in str(execinfo.value)


# Start vector determinant tests
def test_det():
    """test calculation of the determinant of a three dimentional"""

    # Three dim determinant
    x = [5, -2, 1]
    y = [0, 3, -1]
    z = [2, 0, 7]
    mat = [x, y, z]

    a = py_numeric.linalg.det(mat)

    assert a == 103
