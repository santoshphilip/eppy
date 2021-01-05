# Copyright (c) 2020 Santosh Philip
# =======================================================================
#  Distributed under the MIT License.
#  (See accompanying file LICENSE or copy at
#  http://opensource.org/licenses/MIT)
# =======================================================================
# -*- coding: utf-8 -*-
"""do stuff with the energyplus output html"""
# TODO : move this to eppy.readhtml
# TODO Document it in user documentation.
import copy
from io import StringIO

from eppy.results import readhtml


def sniphtml(fname, theline=None):
    """snip the html file at theline"""
    if theline is None:
        theline = "<p><b>Table of Contents</b></p>"
    try:
        fhandle = open(fname, "r")
    except TypeError as e:
        fhandle = fname
    lines = []
    with fhandle:
        for line in fhandle:
            if line.strip() == "<p><b>Table of Contents</b></p>":
                break
            lines.append(line)
    linestxt = "".join(lines)
    tail = """</body>
</html>
"""
    outhtml = f"{linestxt}{tail}"
    return outhtml


def gets2sconversions(htables):
    """get the site to source conversions from the htmlfile"""
    header = "Site to Source Energy Conversion Factors"
    convtable = getthetable(htables, header)
    convtable.pop(0)
    return dict(convtable)


def getthetable(htables, header=None):
    """get the table with the header"""
    thetable = [table[-1] for table in htables if table[0] == header][0]
    thetable = copy.deepcopy(thetable)  # else it will change the htables
    return thetable


def getcolindexdict(table):
    """get the {name:index} dict from header of the table"""
    header = table[0]
    colindexdict = {
        val.split("[")[0].strip(): i + 1 for i, val in enumerate(header[1:])
    }
    return colindexdict


def getcolindexconvdict(colindexdict, convdct):
    """get {colindex:conversion} dict"""
    econvdct = dict()
    for key in colindexdict:
        if key in convdct:
            econvdct[colindexdict[key]] = convdct[key]
        else:
            econvdct[key] = 1
    return econvdct


def dropnonemergy(mat, energyunit=None):
    """drop the non-energy column. energyunit is the energy units in the header"""
    if energyunit is None:
        energyunit = "kBtu"
    energyunit = f"[{energyunit}]"
    firstline = mat[0]
    skipcols = [
        i for i, val in enumerate(firstline) if not val.strip().endswith(energyunit)
    ]
    skipcols.remove(0)
    newmat = []
    for row in mat:
        cells = []
        for i, cell in enumerate(row):
            if i not in skipcols:
                cells.append(cell)
        newmat.append(cells)
    return newmat


def sourceenergyenduses(enduses, colindexconvdict):
    """convert site eenergy in enduses table to source energy"""
    c_enduses = []
    for row in enduses:
        cells = []
        for i, cell in enumerate(row):
            convfactor = colindexconvdict.setdefault(i, 1)
            try:
                newcell = cell * convfactor
            except TypeError as e:
                newcell = cell
            cells.append(newcell)
        c_enduses.append(cells)
    return c_enduses


def sumenergy(mat):
    """sum the energy in the table"""
    energymat = []
    for row in mat:
        try:
            tot = sum(row[1:])
        except TypeError as e:
            continue
        cells = [row[0], tot]
        energymat.append(cells)
    return energymat


def sumsourceenergyenduses(htables):
    """convert enedues to source energy, and return the summed energy for each end use"""
    convdct = gets2sconversions(htables)
    enduses = getthetable(htables, header="End Uses")
    eindexdict = getcolindexdict(enduses)
    econvdct = getcolindexconvdict(eindexdict, convdct)
    c_enduses = sourceenergyenduses(enduses, econvdct)
    newmat = dropnonemergy(c_enduses)
    energymat = sumenergy(newmat)
    return energymat


# TODO this code looks fragile. Maybe use stardard libraty HTML parse to deal with encoding?
def decodeline(line, encoding="utf-8"):
    try:
        return line.decode(encoding)
    except (AttributeError, UnicodeDecodeError) as e:
        if e.__class__ == UnicodeDecodeError:
            # encoding could be ISO-8859-2 in e+ html
            return decodeline(line, encoding="ISO-8859-2")
        else:
            return line


def getnexttable(fhandle):
    """get the next table in the file"""
    lines = fhandle
    tablelines = []
    for line in lines:
        line = decodeline(line)
        if line.strip().startswith("<table"):
            tablelines.append(line)
            break
    for line in lines:
        line = decodeline(line)
        tablelines.append(line)
        if line.strip().startswith("</table"):
            break
    return "".join(tablelines)


def tablebyname(filehandle, header):
    """fast extraction of the table with header"""
    htmlheader = f"<b>{header}</b><br><br>"

    with filehandle:
        for line in filehandle:
            line = decodeline(line)
            if line.strip() == htmlheader:
                justtable = getnexttable(filehandle)
                thetable = f"{htmlheader}\n{justtable}"
                break

    filehandle = StringIO(thetable)
    htables = readhtml.titletable(filehandle)
    try:
        return list(htables[0])
    except IndexError as e:
        None


def get_upto_nexttable(fhandle):
    """get the next table in the file and all lines before it"""
    # unteseted pseudocode
    lines = fhandle
    tablelines = []
    for line in lines:
        line = decodeline(line)
        tablelines.append(line)
        if line.strip().startswith("</table"):
            break
    return "".join(tablelines)


def tablebyindex(filehandle, index):
    """fast extraction of html table with index"""
    with filehandle:
        tableindex = 0
        for i in range(index + 1):
            thetable = get_upto_nexttable(filehandle)
    filehandle = StringIO(thetable)
    htables = readhtml.titletable(filehandle)
    try:
        return htables[0]
    except IndexError as e:
        None
