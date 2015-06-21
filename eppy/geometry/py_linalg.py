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
# Written by Eric Youngson eric@scneco.com / eayoungs@gmail.com
# Succession Ecological Services: Portland, Oregon


class LinAlgError(Exception):
    pass


def det(u, v, w):
    uDim = len(u)
    vDim = len(v)
    wDim = len(w)

    det_A = []

    if uDim == vDim == wDim == 3:
        try:
            # http://mathworld.wolfram.com/Determinant.html
            A = [[u[0], u[1], u[2]], [v[0], v[1], v[2]], [w[0], w[1], w[2]]]
            det_A = (A[0][0] * A[1][1] * A[2][2] + A[0][1] * A[1][2] *
                     A[2][0] + A[0][2] * A[1][0] * A[2][1] - (A[0][2] *
                     A[1][1] * A[2][0] + A[0][1] * A[1][0] * A[2][2] +
                     A[0][0] * A[1][2] * A[2][1]))
            if det_A == 0:
                raise Exception('Singular matrix')
        except LinAlgError as e:
            det_A = e
    else:
        raise IndexError('Vector has invalid dimensions')
    return det_A
