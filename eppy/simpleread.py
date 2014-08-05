"""read the idf file by just parsing the text"""

import StringIO
import eppy.modeleditor as modeleditor
from eppy.modeleditor import IDF

def nocomment(st,com='!'):
    """
    just like the comment in python.
    removes any text after the phrase 'com'
    """
    ls=st.splitlines()
    for i in range(len(ls)):
        el=ls[i]
        pt=el.find(com)
        if pt!=-1:
            ls[i]=el[:pt]
    return '\n'.join(ls)


def _tofloat(s):
    try:
        return float(s)
    except ValueError as e:
        return s
        
def idf2txt(txt):
    """convert the idf text to a simple text"""
    st = nocomment(txt)
    objs = st.split(';')
    objs = [obj.split(',') for obj in objs]
    objs = [[line.strip() for line in obj] for obj in objs]
    objs = [[_tofloat(line) for line in obj] for obj in objs]
    objs = [tuple(obj) for obj in objs]
    objs.sort()

    lst = []
    for obj in objs:
        for field in obj[:-1]:
            lst.append('%s,' % (field, ))
        lst.append('%s;\n' % (obj[-1], ))

    return '\n'.join(lst)
    
    
def idfreadtest(iddhandle, idfhandle1, idfhandle2, verbose=False, save=False):
    """compare the results of eppy reader and simple reader"""
    # read using eppy:
    try:
        IDF.setiddname(iddhandle)
    except modeleditor.IDDAlreadySetError as e:
        # idd has already been set
        pass
    idf = IDF(idfhandle1)
    idfstr = idf.idfstr()
    idfstr = idf2txt(idfstr)
    # - 
    # do a simple read
    simpletxt = idfhandle2.read()
    simpletxt = idf2txt(simpletxt)
    # - 
    if save:
        open('simpleread.idf', 'w').write(idfstr)
        open('eppyread.idf', 'w').write(simpletxt)
    # do the compare      
    lines1 = idfstr.splitlines()
    lines2 = simpletxt.splitlines()
    for i, (line1, line2) in enumerate(zip(lines1, lines2)):
        if line1 != line2:
            # test if it is a mismatch in number format
            try:
                line1 = float(line1[:-1])
                line2 = float(line2[:-1])
                if line1 != line2:
                    if verbose:
                        print
                        print "%s- : %s" % (i, line1)
                        print "%s- : %s" % (i, line2)
                    return False
            except ValueError as e:
                if verbose:
                    print
                    print "%s- : %s" % (i, line1)
                    print "%s- : %s" % (i, line2)
                return False    
    return True
    



# fname = './iddfile/smallfile.idf'
# fhandle = open(fname, 'r')
# st = fhandle.read()
# print idf2txt(st)