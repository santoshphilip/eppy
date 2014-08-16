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
# along with Eppy.  If not, see <http://www.gnu.org/licenses/>.

"""
do a diff between two idf files
prints the difference in a csv file format.
You can redirect the output to a csv file and open as a spreadsheet.

"""
    
    
import argparse

import sys
import itertools
from bs4 import BeautifulSoup, Tag

pathnameto_eplusscripting = "../../"
sys.path.append(pathnameto_eplusscripting)

from eppy.bunch_subclass import BadEPFieldError
from eppy.modeleditor import IDF



help_message = '''
The help message goes here.
'''


class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg


def getobjname(item):
    """return obj name or blank """
    try:
        objname = item.Name
    except BadEPFieldError, e:
        objname = ' '
    return objname


def theheader(n1, n2):
    """return the csv header"""
    s =  "Object Key, Object Name, Field Name, %s, %s" % (n1, n2)
    return s.split(',')

def makecsvdiffs(thediffs, n1, n2):
    """treturn the csv to be displayed"""
    def ishere(val):
        if val == None:
            return "not here" 
        else:
            return "is here"
    rows = []
    rows.append(theheader(n1, n2))
    keys = thediffs.keys()
    for key in keys:
        if len(key) == 2:
            rw2 = [''] + [ishere(i) for i in thediffs[key]]
        else:
            rw2 = list(thediffs[key])
        rw1 = list(key)
        rows.append(rw1 + rw2)
    return rows
        
        
def idfdiffs1(idf1, idf2):
    """print the diffs between the two idfs"""
    thediffs = {}
    keys = idf1.model.dtls # undocumented variable

    for akey in keys:
        idfobjs1 = idf1.idfobjects[akey]
        idfobjs2 = idf2.idfobjects[akey]
        names = set([getobjname(i) for i in idfobjs1] + 
                    [getobjname(i) for i in idfobjs2])
        names = sorted(names)
        idfobjs1 = sorted(idfobjs1, key=lambda idfobj: idfobj['obj'])
        idfobjs2 = sorted(idfobjs2, key=lambda idfobj: idfobj['obj'])
        for name in names:
            n_idfobjs1 = [item for item in idfobjs1 
                            if getobjname(item) == name]
            n_idfobjs2 = [item for item in idfobjs2 
                            if getobjname(item) == name]
            for idfobj1, idfobj2 in itertools.izip_longest(n_idfobjs1, 
                                                          n_idfobjs2):
                if idfobj1 == None:
                    thediffs[(idfobj2.key.upper(), 
                                getobjname(idfobj2))] = (idf1.idfname, None)
                    break
                if idfobj2 == None:
                    thediffs[(idfobj1.key.upper(), 
                                getobjname(idfobj1))] = (None, idf2.idfname)
                    break
                for i, (f1, f2) in enumerate(zip(idfobj1.obj, idfobj2.obj)):
                    if f1 != f2:
                        thediffs[(akey, 
                                getobjname(idfobj1),    
                                idfobj1.objidd[i]['field'][0])] = (f1, f2)
    return thediffs

def printcsv(csvdiffs):
    """print the csv"""
    for row in csvdiffs:
        print ','.join([str(cell) for cell in row])

def heading2table(soup, table, row):
    """add heading row to table"""
    tr = Tag(soup, name="tr")
    table.append(tr)
    for attr in row:
        th = Tag(soup, name="th")
        tr.append(th)
        th.append(attr)
    
def row2table(soup, table, row):
    """ad a row to the table"""
    tr = Tag(soup, name="tr")
    table.append(tr)
    for attr in row:
        td = Tag(soup, name="td")
        tr.append(td)
        td.append(attr)
        
        
def printhtml(csvdiffs):
    """print the html"""
    soup = BeautifulSoup()
    html = Tag(soup, name="html")
    table = Tag(soup, name="table")
    table.attrs.update(dict(border="1"))

    soup.append(html)
    html.append(table)
    heading2table(soup, table, csvdiffs[0])
    for row in csvdiffs[1:]:
        row = [str(cell) for cell in row]
        row2table(soup, table, row)
    print soup.prettify()    
        

if __name__    == '__main__':
    # do the argparse stuff
    parser = argparse.ArgumentParser(usage=None, description=__doc__)
    parser.add_argument('idd', action='store', 
        help='location of idd file = ./somewhere/eplusv8-0-1.idd')
    parser.add_argument('file1', action='store', 
        help='location of first with idf files = ./somewhere/f1.idf') 
    parser.add_argument('file2', action='store', 
        help='location of second with idf files = ./somewhere/f2.idf') 
    nspace = parser.parse_args()
    fname1 = nspace.file1
    fname2 = nspace.file2
    iddfile = nspace.idd
    IDF.setiddname(iddfile)
    idf1 = IDF(fname1)
    idf2 = IDF(fname2)
    thediffs = idfdiffs1(idf1, idf2)
    csvdiffs = makecsvdiffs(thediffs, idf1.idfname, idf2.idfname)
    # printcsv(csvdiffs)
    printhtml(csvdiffs)
    
# python idfdiff1.py ../resources/iddfiles/Energy+V7_2_0.idd ../resources/idffiles/V_7_2/constructions.idf ../resources/idffiles/V_7_2/constructions_diff.idf