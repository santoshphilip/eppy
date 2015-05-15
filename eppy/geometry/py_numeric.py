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

"""This module is used to implement native Python functions to replace those
    called from numpy, when using eppy with Rhino"""
# Written by Eric Youngson eric@successionecological.com / eayoungs@gmail.com
# Succession Ecological Services: Portland, Oregon


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


class MatrixDimError(LinAlgError):
    pass


def _raise_linalgerror_singular(err, flag):
    raise LinAlgError("Singular matrix")


def vctr_cross(u, v):
    """
    Return the cross product of two 3 dimentional vectors.

    The cross product of `u` and `v` in :math:`R^3` is a vector perpendicular
    to both `u` and `v`.  If `u` and `v` are arrays of vectors, the vectors
    are defined by the last axis of `u` and `v` by default, and these axes
    can have dimensions 2 or 3.

    Parameters
    ----------
    u : array_like
        Components of the first vector(s).
    v : array_like
        Components of the second vector(s).

    Returns
    -------
    uxv : 3darray
        Vector cross product(s).

    Raises
    ------
    ValueError
        When the dimension of the vector(s) in `u` and/or `v` does not
        equal 3.

    Examples
    --------
    Vector cross-product.

    >>> x = [1, 2, 3]
    >>> y = [4, 5, 6]
    >>> np.cross(x, y)
    array([-3,  6, -3])
    """

    uDim = len(u)
    vDim = len(v)

    uxv = []

    # http://mathworld.wolfram.com/CrossProduct.html
    if uDim == vDim == 3:
        try:
            for i in range(uDim):
                uxv.append(0)
                uxv = [u[1]*v[2]-u[2]*v[1],
                    -(u[0]*v[2]-u[2]*v[0]),
                    u[0]*v[1]-u[1]*v[0]]
        except LinAlgError as e:
            uxv = e
    else: raise IndexError('Vector has invalid dimensions')
    return uxv


def vctr_dot(u, v):
    """
    Return the dot product of two 3 dimentional vectors.

    The dot product of `u` and `v` in :math:`R^3` is a vector perpendicular
    to both `u` and `v`.  If `u` and `v` are arrays of vectors, the vectors
    are defined by the last axis of `u` and `v` by default, and these axes
    can have dimensions 2 or 3.

    Parameters
    ----------
    u : array_like
        Components of the first vector(s).
    v : array_like
        Components of the second vector(s).

    Returns
    -------
    uxv : 3darray
        Vector dot product(s).

    Raises
    ------
    ValueError
        When the dimension of the vector(s) in `u` and/or `v` does not
        equal 3.

    Examples
    --------
    Vector dot-product.

    >>> x = [1, 2, 3]
    >>> y = [4, 5, 6]
    >>> np.dot(x, y)
    array([4, 10, 18])
    """

    uDim = len(u)
    vDim = len(v)

    u_dot_v = []

    # http://reference.wolfram.com/language/ref/Dot.html
    if uDim == vDim == 3:
        try:
            for i in range(uDim):
                u_dot_v.append(0)
                u_dot_v = [u[0]*v[0],
                        u[1]*v[1],
                        u[2]*v[2]]
        except LinAlgError as e:
            u_dot_v = e 
    else: raise IndexError('Vector has invalid dimensions')
    return u_dot_v


def vctr_det(u, v, w):
    uDim = len(u)
    vDim = len(v)
    wDim = len(w)

    det_A = []

    if uDim == vDim == wDim == 3:
        try:
            A = [[u[0], u[1], u[2]], [v[0], v[1], v[2]], [w[0], w[1], w[2]]]
            det_A = (A[0][0] * A[1][1] * A[2][2] + A[0][1] * A[1][2] * A[2][0]
                + A[0][2] * A[1][0] * A[2][1] - (A[0][2] * A[1][1] * A[2][0]
                + A[0][1] * A[1][0] * A[2][2] + A[0][0] * A[1][2]
                * A[2][1])
                )
        except LinAlgError as e:
                print("ERROR: Singluar Matrix")
        else:
            return det_A
