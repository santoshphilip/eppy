# Copyright (c) 2016 Jamie Bull
# =======================================================================
#  Distributed under the MIT License.
#  (See accompanying file LICENSE or copy at
#  http://opensource.org/licenses/MIT)
# =======================================================================
"""pytest for int2lines.py"""

from eppy.geometry.int2lines import intersection


def test_intersection():
    """pytest for intersection of two lines.
    """
    a = [(0,1,1), (1,0,0)]
    b = [(0,0,0), (1,1,1)]
    expected = [(0.5,0.5,0.5)]  # simple intersection
    result = intersection(a, b)
    assert result == expected
    
    a = [(0,0,0), (1,0,0)]
    b = [(3,3,3), (2,1,2)]
    expected = []  # non-intersecting
    result = intersection(a, b)
    assert result == expected
    
    a = [(0,0,0), (1,1,0)]
    b = [(3,3,0), (2,2,0)]
    expected = []  # collinear, not touching
    result = intersection(a, b)
    assert result == expected
    
    a = [(0,0,0), (1,1,0)]
    b = [(3,3,0), (1,1,0)]
    expected = [(1,1,0)]  # collinear, touching at end point
    result = intersection(a, b)
    assert result == expected
    
    a = [(0,0,0), (2,2,0)]
    b = [(3,3,0), (1,1,0)]
    expected = [(1, 1, 0), (2, 2, 0)]  # overlapping lines
    result = intersection(a, b)
    assert result == expected
    
