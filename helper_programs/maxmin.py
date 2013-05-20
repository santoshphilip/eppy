# Copyright (c) 2012 Santosh Phillip

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

"""get max  and min  of a E+ output variable
--------------
usage:
python maxminlist.py fname ReportVariableDataDictionaryIndex
python maxminlist.py -l simlist.txt ReportVariableDataDictionaryIndex
simlist.txt = file with a list of E+ filenames
----
change the hard coded convertc2f value (True, False) for temperature conversion
"""

import eplussql

fname = '../01gh01/01gh05.sql'
varindex = 70

import sys
import getopt


help_message = '''
The help message goes here.
'''


class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg

def getmaxmin(fname, varindex, convertc2f=False):
    """return variable name, max and min of the variable"""
    cursor = eplussql.getcursor(fname)
    # startpoint = eplussql.get_wfilestart(cursor)
    varunit = eplussql.get_variableunit(cursor, varindex)
    if convertc2f and varunit == u'C':
        func = eplussql.c2f
        varunit = u'F'
    else:
        func = None
    matrix = eplussql.get_variables(cursor, varindex, func=func)
    varname = eplussql.get_variablename(cursor, varindex)
    keyvalue = eplussql.get_keyvalue(cursor, varindex)
    return varname, keyvalue, varunit, min(matrix), max(matrix)
    
def getnames(txt, suffix='sql'):
    """get a list of names from txt. add the suffix"""
    txt = txt.strip()
    lines = txt.splitlines()
    lines = [line.strip() for line in lines]
    names = ["%s.%s" % (line, suffix) for line in lines]
    return names

def test_getnames():
    """py.test for getnames"""
    data = (("a\nb\nc\n", ["a.sql", "b.sql", "c.sql"]), #txt, names
        ("a \nb\nc\n", ["a.sql", "b.sql", "c.sql"]), #txt, names
        ("a \nb\nc\n\n\n", ["a.sql", "b.sql", "c.sql"]), #txt, names
    )
    for txt, names in data:
        result = getnames(txt)
        assert result == names
        
        
        
def main(argv=None):
    if argv is None:
        argv = sys.argv
    try:
        try:
            opts, args = getopt.getopt(argv[1:], "ho:vl", ["help", "output="])
        except getopt.error, msg:
            raise Usage(msg)
    
        # option processing
        alist = False
        for option, value in opts:
            if option == "-v":
                verbose = True
            if option == "-l":
                alist = True
            if option in ("-h", "--help"):
                raise Usage(help_message)
            if option in ("-o", "--output"):
                output = value
                
                
        fname, varindex = args
        convertc2f = True
        if alist:
            txt = open(fname, 'r').read()
            names = getnames(txt)
            matrix = [getmaxmin(name, varindex, convertc2f=convertc2f) for name in names]    
            for name, row in zip(names, matrix):
                name = name.split('.')[0]
                tup =  tuple([name] + list(row))
                print "%s, %s, %s, %s, %s, %s" % tup
        else:
            fnamesql = "%s.sql" % (fname, )
            varname, keyvalue, varunit, mn, mx, = getmaxmin(fnamesql, varindex, convertc2f=convertc2f)
            print "%s, %s, %s, %s, %s, %s" % (fname, varname, keyvalue, varunit, mn, mx)
        
    except Usage, err:
        print >> sys.stderr, sys.argv[0].split("/")[-1] + ": " + str(err.msg)
        print >> sys.stderr, "\t for help use --help"
        return 2


if __name__ == "__main__":
    sys.exit(main())
