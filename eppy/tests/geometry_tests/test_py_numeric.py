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
import pytest


# Exception class
class LinAlgError(Exception):
    """
    Generic Python-exception-derived object raised by linalg functions.

    General purpose exception class, derived from Python's exception.Exception
    class, programmatically raised in linalg functions when a Linear
    Algebra-related condition would prevent further correct execution of the
    function.

    Parameters
    ----------
    None

    Examples
    --------
    >>> from numpy import linalg as LA
    >>> LA.inv(np.zeros((2,2)))
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "...linalg.py", line 350,
        in inv return wrap(solve(a, identity(a.shape[0], dtype=a.dtype)))
      File "...linalg.py", line 249,
        in solve
        raise LinAlgError('Singular matrix')
    numpy.linalg.LinAlgError: Singular matrix

    """
    pass

# Dealing with errors in _umath_linalg

_linalg_error_extobj = None


def _raise_linalgerror_singular(err, flag):
    raise LinAlgError("Singular matrix")


# Start vector cross product tests
def test_vctr_cross():
    """test the cross product of two 3 dimentional vectors"""

    # Vector cross-product.
    x = [1, 2, 3]
    y = [4, 5, 6]
    z = py_numeric.vctr_cross(x, y)

    assert z == [-3, 6, -3]


def test_2dim_cross():
    """test the cross product of two 2 dimentional vectors"""

    # 2 dim cross-product.
    x = [1, 2]
    y = [4, 5]
    z = py_numeric.vctr_cross(x, y)

    assert z == 'ERROR'


def test_4dim_cross():
    """test the cross product of two 2 dimentional vectors"""

    # 4 dim cross-product.
    x = [1, 2, 3, 4]
    y = [5, 6, 7, 8]
    z = py_numeric.vctr_cross(x, y)

    assert z == 'ERROR'


def test_mdim_cross():
    """test the cross product of two 4 dimentional vectors"""

    # Mixed dim cross-product.
    x = [1, 2, 3]
    y = [4, 5, 6, 7]
    z = py_numeric.vctr_cross(x, y)

    assert z == 'ERROR'


# Start vector dot product tests
def test_vctr_dot():
    """test the dot product of two mixed dimentional vectors"""

    # Vector dot-product.
    x = [1, 2, 3]
    y = [4, 5, 6]
    z = py_numeric.vctr_dot(x, y)

    assert z == [4, 10, 18]


def test_2dim_dot():
    """test the dot product of two 2 dimentional vectors"""

    # 2 dim dot-product.
    x = [1, 2]
    y = [4, 5]
    z = py_numeric.vctr_dot(x, y)

    assert z == 'ERROR'


def test_4dim_dot():
    """test the dot product of two 4 dimentional vectors"""

    # 4 dim dot-product.
    x = [1, 2, 3, 4]
    y = [5, 6, 7, 8]
    z = py_numeric.vctr_dot(x, y)

    assert z == 'ERROR'


def test_mdim_dot():
    """test the dot product of two mixed dimentional vectors"""

    # Mixed dim dot-product.
    x = [1, 2, 3]
    y = [4, 5, 6, 7]
    z = py_numeric.vctr_dot(x, y)

    assert z == 'ERROR'


def test_vctr_det():
    """test calculation of the determinant of a three dimentional"""

    # Three dim determinant
    x = [5, -2, 1]
    y = [0, 3, -1]
    z = [2, 0, 7]
    a = py_numeric.vctr_det(x, y, z)

    assert a == 103


def test_singular_vctr_det():
    """test calculation of a singular determinant of a three dimentional"""

    # Assertions about exceptions: http://pytest.org/latest/assert.html
    with pytest.raises(LinAlgError) as execinfo:
        # Three dim determinant
        x = [1, 0, 0]
        y = [-2, 0, 0]
        z = [4, 6, 1]
        a = py_numeric.vctr_det(x, y, z)

    assert 'Singular matrix' in str(execinfo.value)
