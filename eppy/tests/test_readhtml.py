# Copyright (c) 2012 Santosh Philip

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

"""py.test for readhtml.py"""

import collections
from bs4 import BeautifulSoup
import eppy.readhtml as readhtml
from sample_html import sample_html as SAMPLE_HTML



def test_table2matrix():
    """py.test for table2matrix"""
    thedata = (("""<table border="1" cellspacing="0" cellpadding="4">
        <tr>
            <td>1</td>
            <td>2</td>
        </tr>
        <tr>
            <td>3</td>
            <td>4</td>
        </tr>
    </table>""",
    [['1', '2'], ['3', '4']]), # tabletxt, rows
    )
    for tabletxt, rows in thedata:
        soup = BeautifulSoup(tabletxt)
        table = soup.find('table')
        result = readhtml.table2matrix(table)
        assert result == rows
    
def test_table2val_matrix():
    """py.test for table2val_matrix"""
    thedata = (("""<table border="1" cellspacing="0" cellpadding="4">
        <tr>
            <td>b</td>
            <td>2</td>
        </tr>
        <tr>
            <td>3</td>
            <td>4</td>
        </tr>
    </table>""",
    [["b", 2], [3, 4]]), # tabletxt, rows
    )
    for tabletxt, rows in thedata:
        soup = BeautifulSoup(tabletxt)
        table = soup.find('table')
        result = readhtml.table2val_matrix(table)
        assert result == rows
    
def test_gettables():
    """py.test for gettables"""
    thedata = (([('Site and Source Energy',
    [['a', '2'], ['3', '4']]),
    ('Site to Source Energy Conversion Factors',
    [['b', '6'], ['7', '8']]),
    ('Custom Monthly Report',
    [['c', '16'], ['17', '18']]),
    ('Custom Monthly Report',
    [['d', '26'], ['27', '28']])], False), # titlerows, tofloat
    ([('Site and Source Energy',
    [['a', 2], [3, 4]]),
    ('Site to Source Energy Conversion Factors',
    [['b', 6], [7, 8]]),
    ('Custom Monthly Report',
    [['c', 16], [17, 18]]),
    ('Custom Monthly Report',
    [['d', 26], [27, 28]])], True), # titlerows, tofloat
    )
    for titlerows, tofloat in thedata:
        # print titlerows
        result = readhtml.titletable(SAMPLE_HTML, tofloat=tofloat)
        for (title1, rows1), (title2, rows2) in zip(result, titlerows):
            # print title1, title2
            assert title1 == title2
            # print rows1, rows2
            assert rows1 == rows2
        assert result == titlerows
        
def test_has_name():
    """py.test for has_name"""
    soup = BeautifulSoup(SAMPLE_HTML)
    # soup.p = <p><a href="#toc" style="float: right">Table of Contents</a></p>
    assert readhtml._has_name(soup.p) is True
    # soup.b = <b>EnergyPlus-Windows-OMP-32 7.2.0.006, YMD=2013.01.28 16:38</b>
    assert readhtml._has_name(soup.b) is True
    # soup.p.contents[0] = <a href="#toc" style="float: right">Table of Contents</a>
    assert readhtml._has_name(soup.p.contents[0]) is True
    # soup.b.contents[0] = u'EnergyPlus-Windows-OMP-32 7.2.0.006, YMD=2013.01.28 16:38'
    assert readhtml._has_name(soup.b.contents[0]) is False
    
def test_lines_table():
    """py.test for lines_table"""
    # soup = BeautifulSoup(SAMPLE_HTML)
    result = readhtml.lines_table(SAMPLE_HTML, False)
    assert result == [[[u'Table of Contents', 
            u'Report: Annual Building Utility Performance Summary', 
            u'For: Entire Facility', 
            u'Timestamp: 2014-01-13\n    16:47:19', 
            u'Values gathered over      8760.00 hours', 
            u'Site and Source Energy'], 
        [[u'a', u'2'], [u'3', u'4']]], 
    [[u'Site to Source Energy Conversion Factors'], 
        [[u'b', u'6'], [u'7', u'8']]], 
    [[u'Report: COMPONENTS OF PEAK ELECTRICAL DEMAND', 
            u'For: Meter', 
            u'Timestamp: 2014-01-13\n    16:47:19', 
            u'Custom Monthly Report'], 
        [[u'c', u'16'], [u'17', u'18']]], 
    [[u'Report: COMPONENTS OF PEAK NET ELECTRICAL DEMAND', 
            u'For: Meter', 
            u'Timestamp: 2014-01-13\n    16:47:19', 
            u'Custom Monthly Report'], 
        [[u'd', u'26'], [u'27', u'28']]]]

def test_report_tables():
    """py.test for test_named_tables"""
    result = readhtml._report_tables(SAMPLE_HTML)
    assert result == {u'Report: Annual Building Utility Performance Summary': [[u'a', 2.0], [3.0, 4.0]],
    u'Report: COMPONENTS OF PEAK ELECTRICAL DEMAND': [[u'c', 16.0], [17.0, 18.0]],
    u'Report: COMPONENTS OF PEAK NET ELECTRICAL DEMAND': [[u'd', 26.0], [27.0, 28.0]]}

def test_make_ntgrid():
    """py.test make_ntgrid"""
    grid = [["",  "a b", "b c", "c d"],
     ["x y", 1,     2,     3 ],
     ["y z", 4,     5,     6 ],
     ["z z", 7,     8,     9 ],]
    result = readhtml._make_ntgrid(grid)
    ntcol = collections.namedtuple('ntcol', "x_y y_z z_z")
    ntrow = collections.namedtuple('ntrow', "a_b b_c c_d")
    assert result == ntcol(x_y=ntrow(a_b=1, b_c=2, c_d=3), 
          y_z=ntrow(a_b=4, b_c=5, c_d=6), 
          z_z=ntrow(a_b=7, b_c=8, c_d=9))