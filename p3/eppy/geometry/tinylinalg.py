# Copyright (c) 2014 Eric Allen Youngson
# =======================================================================
#  Distributed under the MIT License.
#  (See accompanying file LICENSE or copy at
#  http://opensource.org/licenses/MIT)
# =======================================================================

"""This module is used to implement native Python functions to replace those
    called from numpy, when not available"""






# Written by Eric Youngson eric@scneco.com / eayoungs@gmail.com
# Succession Ecological Services: Portland, Oregon

class LinAlgError(Exception):
    """Exception"""
    pass

def det(anarray):
    """det"""
    if len(anarray) == 3 and [len(vec) == 3 for vec in anarray]:
        try:
            # http://mathworld.wolfram.com/Determinant.html
            det_a = (
                anarray[0][0] * anarray[1][1] * anarray[2][2] +
                anarray[0][1] * anarray[1][2] * anarray[2][0] +
                anarray[0][2] * anarray[1][0] * anarray[2][1] -
                (
                    anarray[0][2] * anarray[1][1] * anarray[2][0] +
                    anarray[0][1] * anarray[1][0] * anarray[2][2] +
                    anarray[0][0] * anarray[1][2] * anarray[2][1]
                )
                )
        except LinAlgError as err:
            det_a = err
    else:
        raise IndexError('Vector has invalid dimensions')
    return det_a
