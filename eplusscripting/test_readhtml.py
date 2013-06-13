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

import readhtml
from bs4 import BeautifulSoup

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
    
def test_gettables():
    """py.test for gettables"""
    thedata = (("""<b>this is the title</b>    
    <table border="1" cellspacing="0" cellpadding="4">
        <tr>
            <td>1</td>
            <td>2</td>
        </tr>
        <tr>
            <td>3</td>
            <td>4</td>
        </tr>
    </table>    
    """,
    [('this is the title',
    [['1', '2'], ['3', '4']])]), # html_doc, titlerows
    ("""<b>this is the title 1</b>    
    <table border="1" cellspacing="0" cellpadding="4">
        <tr>
            <td>1</td>
            <td>2</td>
        </tr>
        <tr>
            <td>3</td>
            <td>4</td>
        </tr>
    </table>    
    <b>this is the title 2</b>    
    <table border="1" cellspacing="0" cellpadding="4">
        <tr>
            <td>11</td>
            <td>22</td>
        </tr>
        <tr>
            <td>33</td>
            <td>44</td>
        </tr>
    </table>    
    """,
    [('this is the title 1',
    [['1', '2'], ['3', '4']]),
    ('this is the title 2',
    [['11', '22'], ['33', '44']])]), # html_doc, titlerows
    ("""<b>this is the title 1</b>    
    <table border="1" cellspacing="0" cellpadding="4">
        <tr>
            <td>1</td>
            <td>2</td>
        </tr>
        <tr>
            <td>3</td>
            <td>4</td>
        </tr>
    </table>    
    <b>this is the title 2</b>    
    <table border="1" cellspacing="0" cellpadding="4">
        <tr>
            <td>11</td>
            <td>22</td>
        </tr>
        <tr>
            <td>33</td>
            <td>44</td>
        </tr>
    </table>    
    <table border="1" cellspacing="0" cellpadding="4">
        <tr>
            <td>111</td>
            <td>222</td>
        </tr>
        <tr>
            <td>333</td>
            <td>444</td>
        </tr>
    </table>    
    <b>this is the title 1</b>    
    <table border="1" cellspacing="0" cellpadding="4">
        <tr>
            <td>1</td>
            <td>2</td>
        </tr>
        <tr>
            <td>3</td>
            <td>4</td>
        </tr>
    </table>    
    """,
    [('this is the title 1',
    [['1', '2'], ['3', '4']]),
    ('this is the title 2',
    [['11', '22'], ['33', '44']]),
    ('this is the title 2',
    [['111', '222'], ['333', '444']]),
    ('this is the title 1',
    [['1', '2'], ['3', '4']])]), # html_doc, titlerows
    )
    for html_doc, titlerows in thedata:
        result = readhtml.titletable(html_doc)
        assert result == titlerows