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

"""read the html outputs"""


# import sys
# print sys.version
# import bs4
from bs4 import BeautifulSoup, NavigableString, Tag

class NotSimpleTable(Exception):
    pass
        

def is_simpletable(table):
    """test if the table has only strings in the cells"""
    tds = table('td')
    for td in tds:
        if td.contents != []:
            if len(td.contents) == 1:
                if not isinstance(td.contents[0], NavigableString):
                    return False
            else:
                return False
    return True

def table2matrix(table):
    """convert a table to a list of lists - a 2D matrix"""

    if not is_simpletable(table):
        raise NotSimpleTable, "Not able read a cell in the table as a string"
    rows = []
    for tr in table('tr'):
        row = []
        for td in tr('td'):
            try:
                row.append(td.contents[0])
            except IndexError, e:
                row.append('')
        rows.append(row)
    return rows

def table2val_matrix(table):
    """convert a table to a list of lists - a 2D matrix
    Converts numbers to float"""
    if not is_simpletable(table):
        raise NotSimpleTable, "Not able read a cell in the table as a string"
    rows = []
    for tr in table('tr'):
        row = []
        for td in tr('td'):
            try:
                val = td.contents[0]
            except IndexError, e:
                row.append('')
            else:
                try:
                    val = float(val)
                    row.append(val)
                except ValueError, e:
                    row.append(val)
        rows.append(row)
    return rows


def titletable(html_doc, tofloat=True):
    """return a list of [(title, table), .....]
    
    title = previous item with a <b> tag
    table = rows -> [[cell1, cell2, ..], [cell1, cell2, ..], ..]"""
    soup = BeautifulSoup(html_doc)
    btables = soup.find_all(['b', 'table']) # find all the <b> and <table> 
    titletables = []
    for i, item in enumerate(btables):
        if item.name == 'table':
            for j in range(i + 1):
                if btables[i-j].name == 'b':# step back to find a <b>
                    break
            titletables.append((btables[i-j], item))
    if tofloat:
        t2m = table2val_matrix
    else:
        t2m = table2matrix
    titlerows = [(tl.contents[0], t2m(tb)) for tl, tb in titletables]
    return titlerows
    
def _has_name(soup_obj):
    """checks if soup_obj is really a soup object or just a string
    If it has a name it is a soup object"""
    try:
        name = soup_obj.name
        return True
    except AttributeError, e:
        return False    
        
def lines_table(html_doc):
    """return a list of [(lines, table), .....]
    
    lines = all the significant lines before the table. 
        These are lines between this table and 
        the previous table or 'hr' tag
    table = rows -> [[cell1, cell2, ..], [cell1, cell2, ..], ..]
    
    The lines act as a description for what is in the table
    """
    pass
