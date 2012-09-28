"""py.test for comfort.py"""

import comfort
from pytest_helpers import almostequal


def test_indexloop():
    """py.test for indexloop"""
    data = ((1, [0,1,2,3], 1), # i, lst, ni
        (-1, [0,1,2,3], -1), # i, lst, ni
        (4, [0,1,2,3], 0), # i, lst, ni
        (5, [0,1,2,3], 1), # i, lst, ni
    )
    for i, lst, ni in data:
        result = comfort.indexloop(i, lst)
        assert result == ni

def test_comfort_optimal():
    """py.test for comfort_optimal"""
    data = ((20, 24.0), # tavg, comf
    )
    for tavg, comf in data:
        result = comfort.comfort_optimal(tavg)
        assert result == comf
        
def test_comfort_upper():
    """py.test for comfort_upper"""
    data = ((20, 0, 27.5), # tavg, windinc, comf
        (20, 1, 28.5), # tavg, windinc, comf
    )
    for tavg, windinc, comf in data:
        result = comfort.comfort_upper(tavg, windinc=windinc)
        assert result == comf

def test_comfort_lower():
    """py.test for comfort_lower"""
    data = ((20, 20.5), # tavg, comf
    )
    for tavg, comf in data:
        result = comfort.comfort_lower(tavg)
        assert result == comf

def test_avg_around():
    """py.test for avg_around"""
    data = ((1, [1,2,3,4], 0, 0, 2), # i, lst, upspan, downspan, avg
        (2, [1,3,3,6], 1, 1, 4), # i, lst, upspan, downspan, avg
        (2, [1,3,3,6,7], 1, 1, 4), # i, lst, upspan, downspan, avg
        (2, [1,2,3,6], 1, 0, 2.5), # i, lst, upspan, downspan, avg
        (3, [1,2,3,4], 0, 1, 2.5), # i, lst, upspan, downspan, avg
        (4, [1,2,3,4,5,6,7,8,9], 5, 5, 5), # i, lst, upspan, downspan, avg
        (4, [1,2,3,4,5,6,7,8,9], 6, 6, 5), # i, lst, upspan, downspan, avg
    )
    for i, lst, upspan, downspan, avg in data:
        result = comfort.avg_around(i, lst, upspan, downspan)
        assert result == avg
        
def test_comfort80():
    """py.test for comfort80"""
    data = ((23, 80, True, 28.43), # tavg, limit, celsius, comf
    )
    for tavg, limit, celsius, comf in data:
        result = comfort.comfort(tavg, limit=limit, celsius=celsius)
        assert result == comf
        
def test_comfortET():
    """py.test for comfortET"""
    data = ((23.0386, 80, 2, True, 30.2747), 
        # etavg, limit, windinc, celsius, comf
    )
    for etavg, limit, windinc, celsius, comf in data:
        result = comfort.comfortET(etavg, limit, windinc, celsius)    
        assert round(result, 3) == round(comf, 3)
        
def test_comfort_matrix():
    """py.test for comfort_matrix"""
    data = (# ([[22,27],
    #         [23,28],
    #         [30,32],
    #         [32,30],
    #         [28,23],
    #         [27,22]],
    #         comfort.comfort,
    #         1,1,
    #         #-
    #         [[22,27,24,28.74,1.74],
    #         [23,28,25,29.05,1.05],
    #         [30,32,28.33333333,30.08333333,-1.916666667],
    #         [32,30,30,30.6,0.6],
    #         [28,23,29,30.29,7.29],
    #         [27,22,25.66666667,29.25666667,7.256666667]]), 
        # inmat, comfunc, upspan, downspan, outmat
        ([[22,27],
        [23,28],
        [30,32],
        [32,30],
        [28,23],
        [27,22]],
        comfort.comfortET,
        1,1,
        #-
        [[22.0, 27.0, 24.0, 28.52, 1.52],
         [23.0, 28.0, 25.0, 28.774999999999999, 0.77500000000000002],
         [30.0, 32.0, 28.333333329999999, 29.625, -2.375],
         [32.0, 30.0, 30.0, 30.050000000000001, 0.050000000000000003],
         [28.0, 23.0, 29.0, 29.795000000000002, 6.7949999999999999],
         [27.0, 22.0, 25.666666670000001, 28.945, 6.9450000000000003]]), 
        # inmat, comfunc, upspan, downspan, outmat    
        )
    for inmat, comfunc, upspan, downspan, outmat in data:
        result = comfort.comfort_matrix(inmat, comfunc, upspan, downspan)
        for row1, row2 in zip(result, outmat):
            for c1, c2 in zip(row1, row2):
                assert almostequal(c1, c2)
    