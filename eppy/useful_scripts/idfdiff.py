# Copyright (c) 2012 Santosh Philip
# =======================================================================
#  Distributed under the MIT License.
#  (See accompanying file LICENSE or copy at
#  http://opensource.org/licenses/MIT)
# =======================================================================


"""
Do a diff between two idf files.
Prints the diff in csv  or html file format.
You can redirect the output to a file and open the file using as a spreadsheet or by using a browser
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import argparse

from pprint import pprint
import sys
import itertools

try:
    from itertools import zip_longest as zip_longest
except:
    from itertools import izip_longest as zip_longest
from bs4 import BeautifulSoup, Tag

pathnameto_eplusscripting = "../../"
sys.path.append(pathnameto_eplusscripting)

from eppy.bunch_subclass import BadEPFieldError
from eppy.modeleditor import IDF
from eppy.easyopen import easyopen
from eppy.modeleditor import IDDAlreadySetError

help_message = """
The help message goes here.
"""


class IDDMismatchError(Exception):
    pass


class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg


def getobjname(item):
    """return obj name or blank"""
    try:
        objname = item.Name
    except BadEPFieldError as e:
        objname = " "
    return objname


def theheader(n1, n2):
    """return the csv header"""
    s = "Object Key, Object Name, Field Name, %s, %s" % ("file1", "file2")
    return s.split(",")


class DtlsSorter(object):
    """helps me to sort it using the order of keys in idd file"""

    def __init__(self, dtls):
        self.dtlsorder = {j: i for i, j in enumerate(dtls)}

    def getkey(self, item):
        return self.dtlsorder[item[0]]  # item[0] is the object key


def makecsvdiffs(thediffs, idf1, idf2):
    """return the csv to be displayed"""
    dtls = idf1.model.dtls  # undocumented variable
    return makecsvdiffs_raw(thediffs, dtls, idf1.idfname, idf2.idfname)


def makecsvdiffs_raw(thediffs, dtls, n1, n2):
    """return the csv to be displayed - the args here are tricky
    This function is called by makecsvdiffs.
    Best not to call directly"""

    def ishere(val):
        if val == None:
            return "not here"
        else:
            return "is here"

    rows = []
    rows.append(["file1 = %s" % (n1,)])
    rows.append(["file2 = %s" % (n2,)])
    rows.append("")
    rows.append(theheader(n1, n2))
    keys = list(thediffs.keys())  # ensures sorting by Name
    keys.sort()
    # sort the keys in the same order as in the idd
    dtlssorter = DtlsSorter(dtls)
    keys = sorted(keys, key=dtlssorter.getkey)
    for key in keys:
        if len(key) == 2:
            rw2 = [""] + [ishere(i) for i in thediffs[key]]
        else:
            rw2 = list(thediffs[key])
        rw1 = list(key)
        rows.append(rw1 + rw2)
    return rows


def idfdiffs(idf1, idf2):
    """return the diffs between the two idfs"""
    # for any object type, it is sorted by name
    thediffs = {}
    keys = idf1.model.dtls  # undocumented variable

    for akey in keys:
        idfobjs1 = idf1.idfobjects[akey]
        idfobjs2 = idf2.idfobjects[akey]
        names = set(
            [getobjname(i) for i in idfobjs1] + [getobjname(i) for i in idfobjs2]
        )
        names = sorted(names)
        idfobjs1 = sorted(idfobjs1, key=lambda idfobj: idfobj["obj"])
        idfobjs2 = sorted(idfobjs2, key=lambda idfobj: idfobj["obj"])
        for name in names:
            n_idfobjs1 = [item for item in idfobjs1 if getobjname(item) == name]
            n_idfobjs2 = [item for item in idfobjs2 if getobjname(item) == name]
            for idfobj1, idfobj2 in zip_longest(n_idfobjs1, n_idfobjs2):
                if idfobj1 == None:
                    thediffs[(idfobj2.key.upper(), getobjname(idfobj2))] = (
                        None,
                        idf2.idfname,
                    )  # (idf1.idfname, None) -> old
                    break
                if idfobj2 == None:
                    thediffs[(idfobj1.key.upper(), getobjname(idfobj1))] = (
                        idf1.idfname,
                        None,
                    )  # (None, idf2.idfname) -> old
                    break
                for i, (f1, f2) in enumerate(zip(idfobj1.obj, idfobj2.obj)):
                    if i == 0:
                        f1, f2 = f1.upper(), f2.upper()
                    if f1 != f2:
                        thediffs[
                            (akey, getobjname(idfobj1), idfobj1.objidd[i]["field"][0])
                        ] = (f1, f2)
    return thediffs


def makecsv(csvdiffs):
    """retun the csv of the diffs"""
    lines = []
    for row in csvdiffs:
        line = ",".join([str(cell) for cell in row])
        lines.append(line)
    return "\n".join(lines)


def printcsv(csvdiffs):
    """print the csv"""
    for row in csvdiffs:
        print(",".join([str(cell) for cell in row]))


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


def makehtmlsoup(csvdiffs):
    """make the html soup"""
    soup = BeautifulSoup()
    html = Tag(soup, name="html")
    para1 = Tag(soup, name="p")
    para1.append(csvdiffs[0][0])
    para2 = Tag(soup, name="p")
    para2.append(csvdiffs[1][0])
    table = Tag(soup, name="table")
    table.attrs.update(dict(border="1"))

    soup.append(html)
    html.append(para1)
    html.append(para2)
    html.append(table)
    heading2table(soup, table, csvdiffs[3])
    for row in csvdiffs[4:]:
        row = [str(cell) for cell in row]
        row2table(soup, table, row)
    # print soup.prettify()
    return soup


def printhtml(csvdiffs):
    """print the html"""
    soup = makehtmlsoup(csvdiffs)
    print(soup)


def htmlinnotebook(soup):
    """display the html in jupyter notebook"""
    from IPython.core.display import display, HTML

    soupstr = str(soup)
    display(HTML(soupstr))


if __name__ == "__main__":
    # do the argparse stuff
    parser = argparse.ArgumentParser(usage=None, description=__doc__)
    parser.add_argument(
        "file1",
        action="store",
        help="location of first with idf files = ./somewhere/f1.idf",
    )
    parser.add_argument(
        "file2",
        action="store",
        help="location of second with idf files = ./somewhere/f2.idf",
    )
    parser.add_argument(
        "--idd",
        action="store",
        help="location of idd file = ./somewhere/eplusv8-0-1.idd",
    )
    # parser.add_argument(
    #     'idd', action='store',
    #     help='location of idd file = ./somewhere/eplusv8-0-1.idd')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--csv", action="store_true")
    group.add_argument("--html", action="store_true")
    nspace = parser.parse_args()
    fname1 = nspace.file1
    fname2 = nspace.file2
    iddfile = nspace.idd
    print(iddfile, fname1, fname2)
    # IDF.setiddname(iddfile)
    idf1 = easyopen(fname1, idd=iddfile)
    try:
        idf2 = easyopen(fname2, idd=iddfile)
    except IDDAlreadySetError as e:
        astr = "The two files have different version numners"
        raise IDDMismatchError(astr)

    # TODO What id they have different idd files ?
    thediffs = idfdiffs(idf1, idf2)
    csvdiffs = makecsvdiffs(thediffs, idf1, idf2)
    if nspace.csv:
        printcsv(csvdiffs)
    elif nspace.html:
        printhtml(csvdiffs)


# python idfdiff.py --csv --idd ../resources/iddfiles/Energy+V7_2_0.idd ../resources/idffiles/V_7_2/constr.idf ../resources/idffiles/V_7_2/constr_diff.idf
# python idfdiff.py --html --idd ../resources/iddfiles/Energy+V7_2_0.idd ../resources/idffiles/V_7_2/constr.idf ../resources/idffiles/V_7_2/constr_diff.idf
# python idfdiff2.py --html --idd ../resources/iddfiles/Energy+V8_0_0.idd ../resources/idffiles/V8_0_0/5ZoneSupRetPlenRAB.idf ../resources/idffiles/V8_0_0/5ZoneWaterLoopHeatPump.idf
# python idfdiff.py --csv  ../resources/idffiles/V_7_2/constr.idf ../resources/idffiles/V_7_2/constr_diff.idf
# python idfdiff.py --csv  ../resources/idffiles/V_7_2/constr.idf ../resources/idffiles/V_7_2/constr_diff_bad.idf
