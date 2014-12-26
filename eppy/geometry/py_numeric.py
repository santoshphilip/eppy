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


def vctr_cross(u, v):
    """
    Return the cross product of two 3 dimentional vectors.

    The cross product of `a` and `b` in :math:`R^3` is a vector perpendicular
    to both `a` and `b`.  If `a` and `b` are arrays of vectors, the vectors
    are defined by the last axis of `a` and `b` by default, and these axes
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
        for i in range(uDim):
            uxv.append(0)
        uxv = [u[1]*v[2]-u[2]*v[1],
               -(u[0]*v[2]-u[2]*v[0]),
               u[0]*v[1]-u[1]*v[0]]
    else:
            uxv = 'ERROR'
    return uxv


def vctr_dot(u, v):
    """
    Return the dot product of two 3 dimentional vectors.
    """

    uDim = len(u)
    vDim = len(v)

    u_dot_v = []

    # http://reference.wolfram.com/language/ref/Dot.html
    if uDim == vDim == 3:
        for i in range(uDim):
            u_dot_v.append(0)
        u_dot_v = [u[0]*v[0],
                   u[1]*v[1],
                   u[2]*v[2]]
    else:
            u_dot_v = 'ERROR'
    return u_dot_v
