# Copyright (c) 2012 Santosh Philip
# =======================================================================
#  Distributed under the MIT License.
#  (See accompanying file LICENSE or copy at
#  http://opensource.org/licenses/MIT)
# =======================================================================
"""read the idf file by just parsing the text"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import eppy.modeleditor as modeleditor
from eppy.modeleditor import IDF


def nocomment(astr, com="!"):
    """
    just like the comment in python.
    removes any text after the phrase 'com'
    """
    alist = astr.splitlines()
    for i in range(len(alist)):
        element = alist[i]
        pnt = element.find(com)
        if pnt != -1:
            alist[i] = element[:pnt]
    return "\n".join(alist)


def _tofloat(num):
    """to float"""
    try:
        return float(num)
    except ValueError:
        return num


def idf2txt(txt):
    """convert the idf text to a simple text"""
    astr = nocomment(txt)
    objs = astr.split(";")
    objs = [obj.split(",") for obj in objs]
    objs = [[line.strip() for line in obj] for obj in objs]
    objs = [[_tofloat(line) for line in obj] for obj in objs]
    objs = [tuple(obj) for obj in objs]
    objs.sort()

    lst = []
    for obj in objs:
        for field in obj[:-1]:
            lst.append("%s," % (field,))
        lst.append("%s;\n" % (obj[-1],))

    return "\n".join(lst)


def idfreadtest(iddhandle, idfhandle1, idfhandle2, verbose=False, save=False):
    """compare the results of eppy reader and simple reader"""
    # read using eppy:
    try:
        IDF.setiddname(iddhandle)
    except modeleditor.IDDAlreadySetError:
        # idd has already been set
        pass
    idf = IDF(idfhandle1)
    idfstr = idf.idfstr()
    idfstr = idf2txt(idfstr)
    # -
    # do a simple read
    simpletxt = idfhandle2.read()
    try:
        simpletxt = simpletxt.decode("ISO-8859-2")
    except AttributeError:
        pass
    simpletxt = idf2txt(simpletxt)
    # -
    if save:
        open("simpleread.idf", "w").write(idfstr)
        open("eppyread.idf", "w").write(simpletxt)
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
                        print()
                        print("%s- : %s" % (i, line1))
                        print("%s- : %s" % (i, line2))
                    return False
            except ValueError:
                if verbose:
                    print()
                    print("%s- : %s" % (i, line1))
                    print("%s- : %s" % (i, line2))
                return False
    return True
