"""get max list and min list of a E+ output variable
minlist is the min 5 values
--------------
usage:
python maxminlist.py fname ReportVariableDataDictionaryIndex
python maxminlist.py -l simlist.txt ReportVariableDataDictionaryIndex
simlist.txt = file with a list of E+ filenames
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

def getmaxmin(fname, varindex):
    """return variable name, max and min of the variable"""
    # print fname
    cursor = eplussql.getcursor(fname)
    startpoint = eplussql.get_wfilestart(cursor)
    matrix = eplussql.get_variables(cursor, varindex, startpoint)
    varname = eplussql.get_variablename(cursor, varindex)
    return varname, min(matrix), max(matrix)
    
def getmaxminlist(fname, varindex, numitems=5):
    """return variable name, max and min of the variable"""
    # print fname
    cursor = eplussql.getcursor(fname)
    startpoint = eplussql.get_wfilestart(cursor)
    matrix = eplussql.get_variables(cursor, varindex, startpoint)
    varname = eplussql.get_variablename(cursor, varindex)
    matrix.sort()
    return varname, matrix[:numitems], matrix[-numitems:]
    
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
        if alist:
            txt = open(fname, 'r').read()
            names = getnames(txt)
            matrix = [getmaxminlist(name, varindex, 2) for name in names]
            for name, row in zip(names, matrix):
                name = name.split('.')[0]
                varname, mnlst, mxlst = row
                mnlst = [str(item) for item in mnlst]
                mxlst = [str(item) for item in mxlst]
                mnlst = ','.join(mnlst)
                mxlst = ','.join(mxlst)
                row = "%s, %s, min=, %s, max=, %s" % (name, varname, mnlst, mxlst)
                # tup =  tuple([name] + list(row))
                # print "%s, %s, %s, %s" % row
                print row
        else:
            fnamesql = "%s.sql" % (fname, )
            varname, mn, mx, = getmaxminlist(fnamesql, varindex)
            mn = [str(item) for item in mn]
            mn = ','.join(mn)
            mx = [str(item) for item in mx]
            mx = ','.join(mx)
            print "%s, %s, min=,%s, %s" % (fname, varname, mn, mx)
        
    except Usage, err:
        print >> sys.stderr, sys.argv[0].split("/")[-1] + ": " + str(err.msg)
        print >> sys.stderr, "\t for help use --help"
        return 2


if __name__ == "__main__":
    sys.exit(main())
