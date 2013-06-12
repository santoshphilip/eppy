# Copyright (c) 2012 Santosh Philip

# This file is part of eplusinterface_diagrams.

# Eplusinterface_diagrams is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# Eplusinterface_diagrams is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with eplusinterface_diagrams.  If not, see <http://www.gnu.org/licenses/>.

"""py.test for date_functions"""
import date_functions

def test_yeardates():
    """py.test for yeardates"""
    data = ((2004, '2004-1-1', '2004-1-31', 
            '2004-12-31', '2004-12-30'), #year, jan1, jan31, dec31, dec29
    )
    for year, jan1, jan31, dec31, dec29 in data:
        d = date_functions.yeardates(year)
        assert d[0] == jan1
        assert d[30] == jan31
        assert d[-1] == dec31
        assert d[-2] == dec29

def test_yeardateshours():
    """py.test for yeardateshours"""
    data = ((2004, 
        '2004-1-1 hr2:00', 
        '2004-1-31 hr10:00', 
        '2004-12-31 hr15:00', 
        '2004-12-30 hr24:00'), # year, jan1h2, jan31h10, dec31h15, dec29h24
    )        
    for year, jan1h2, jan31h10, dec31h15, dec29h24 in data:
        yd = date_functions.yeardateshours(year)
        assert yd[0 + 2 - 1] == jan1h2
        assert yd[30 * 24 + 10 - 1] == jan31h10
        assert yd[-1 * 24 + 15 - 1] == dec31h15
        assert yd[-2 * 24 + 24 - 1] == dec29h24
        
def test_split2days():
    """py.test for split2days"""
    data = (([1,2,3,1,2,3,1,2,3], 3, 
        [[1,2,3],[1,2,3],[1,2,3]]), # lst, hrs, daylst
    )
    for lst, hrs, daylst in data:
        result = date_functions.split2days(lst, hrs)
        assert result == daylst

def test_split2months():
    """py.test for split2months"""
    data = (([1,2,3,4,5,6,7,8,9,0], 
        [2,3,2,3], 1, 
        [[1,2],[3,4,5],[6,7],[8,9,0]]),# lst, months, hours, mths
        ([1,1,2,2,3,3,4,4,5,5,6,6,7,7,8,8,9,9,0,0], 
        [2,3,2,3], 2, 
        [[1,1,2,2],[3,3,4,4,5,5],[6,6,7,7],[8,8,9,9,0,0]]),
                                        # lst, months, hours, mths
    )
    for lst, months, hours, mths in data:
        result = date_functions.split2months(lst, months, hours)
        assert result == mths
    # test for a real year with 24 hours  
    lst = [1, ] * 365 * 24 # data for each hour = 1
    months = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    sums = [m * 24 for m in months] # sum of data in each month
    result = date_functions.split2months(lst)
    sresult = [sum(m) for m in result] # sum of data in each month
    assert sresult == sums
    
def test_fillmonths():
    """py.test for fillmonths"""
    data = (([1,2], [3,4], 1, [[1,1,1],[2,2,2,2]]), 
        # data, months, hours, outdata
        ([1,2], [3,4], 2, [[1,1,1,1,1,1],[2,2,2,2,2,2,2,2]]), 
            # data, months, hours, outdata
    )
    for data, months, hours, outdata in data:
        result = date_functions.fillmonths(data, months, hours)
        assert result == outdata
           
    
def test_filterdays():
    """py.test for filterdays"""
    data = (([[1, 1],
            [2, 2],
            [3, 3],
            [4, 11],
            [1, 11],
            [2, 11],
            [3, 110],
            [4, 11],
            [1, 11],
            [2, 11],
            [3, 11],
            [4, 11],], -1, 100, date_functions.gt, 4,
            [[1, 11],
            [2, 11],
            [3, 110],
            [4, 11],]), # matrix, filterindex, filterval, condition, hrs, thefiltered
    )       
    for matrix, filterindex, filterval, condition, hrs, thefiltered in data:
        result = date_functions.filterdays(matrix, filterindex, 
                                        filterval, condition, hrs)
        assert result == thefiltered
        
        
def test_zfilterdays():
    """py.test for zfilterdays"""
    data = (([[1, 1],
            [2, 2],
            [3, 3],
            [4, 11],
            [1, 11],
            [2, 11],
            [3, 110],
            [4, 11],
            [1, 11],
            [2, 11],
            [3, 11],
            [4, 11],], -1, 100, date_functions.gt, 4,
            [[],
            [],
            [],
            [],
            [1, 11],
            [2, 11],
            [3, 110],
            [4, 11],
            [],
            [],
            [],
            [],],), # matrix, filterindex, filterval, condition, hrs, thefiltered
    )       
    for matrix, filterindex, filterval, condition, hrs, thefiltered in data:
        result = date_functions.zfilterdays(matrix, filterindex, 
                                        filterval, condition, hrs)
        print result
        print '-' * 35
        print thefiltered
        assert result == thefiltered                