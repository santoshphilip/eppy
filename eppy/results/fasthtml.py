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


def _decodeline(line, encoding="utf-8"):
    """decodes bytes to string, if line is not bytes, line is returned
    
    It will first attempt to decode line with value of `encoding`. If that fails, it will try with encoding="ISO-8859-2". If that fails, it will return line.
    
    Why is it trying encoding="ISO-8859-2". Looks like E+ uses this encoding in some example files and which is then output in the HTML file
    
    # TODO this code looks fragile. Maybe use standard library HTML parse to deal with encoding?    

    Parameters
    ----------
    line : str, bytes
    encoding : str

    Returns
    -------
    line : str
        decoded line
    """
    try:
        return line.decode(encoding)
    except (AttributeError, UnicodeDecodeError) as e:
        if e.__class__ == UnicodeDecodeError:
            # encoding could be ISO-8859-2 in e+ html
            return _decodeline(line, encoding="ISO-8859-2")
        else:
            return line


def getnexttable(fhandle):
    """get the next table in the file"""
    lines = fhandle
    tablelines = []
    for line in lines:
        line = _decodeline(line)
        if line.strip().startswith("<table"):
            tablelines.append(line)
            break
    for line in lines:
        line = _decodeline(line)
        tablelines.append(line)
        if line.strip().startswith("</table"):
            break
    return "".join(tablelines)


def tablebyname(filehandle, header):
    """fast extraction of the table with header"""
    htmlheader = f"<b>{header}</b><br><br>"

    with filehandle:
        for line in filehandle:
            line = _decodeline(line)
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
        line = _decodeline(line)
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
