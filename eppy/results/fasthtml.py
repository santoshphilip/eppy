# Copyright (c) 2020 Santosh Philip
# =======================================================================
#  Distributed under the MIT License.
#  (See accompanying file LICENSE or copy at
#  http://opensource.org/licenses/MIT)
# =======================================================================
# -*- coding: utf-8 -*-
"""functions to do a fast read from the E+ HTML table file"""
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
    """get the next table in the html file

    Continues to read the file line by line and collects lines from the start of the next table until the end of the table

    Parameters
    ----------
    fhandle : file like object
        A file handle to the E+ HTML table file

    Returns
    -------
    table : str
        The table in HTML format
    """
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
    """fast extraction of the table using the header to identify the table

    This function reads only one table from the HTML file. This is in contrast to `results.readhtml.titletable` that will read all the tables into memory and allows you to interactively look thru them. The function `results.readhtml.titletable` can be very slow on large HTML files.

    This function is useful when you know which file you are looking for. It looks for the title line that is in bold just before the table. Some tables don't have such a title in bold. This function will not work for tables that don't have a title in bold

    Parameters
    ----------
    fhandle : file like object
        A file handle to the E+ HTML table file
    header: str
        This is the title of the table you are looking for

    Returns
    -------
    titleandtable : (str, list)
        - (title, table)
            - title = previous item with a <b> tag
            - table = rows -> [[cell1, cell2, ..], [cell1, cell2, ..], ..]
    """
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
    """get all lines from the present location in fhandle to the end of the next table

    This function is used by `tablebyindex` to find the title for the table, which is in the lines before the table. Then it can return the title and the table

    Parameters
    ----------
    fhandle : file like object
        A file handle to the E+ HTML table file

    Returns
    -------
    lines_and_table : str
        The table in HTML format with lines before it.
    """
    lines = fhandle
    tablelines = []
    for line in lines:
        line = _decodeline(line)
        tablelines.append(line)
        if line.strip().startswith("</table"):
            break
    return "".join(tablelines)


def tablebyindex(filehandle, index):
    """fast extraction of the table using the index to identify the table

    This function reads only one table from the HTML file. This is in contrast to `results.readhtml.titletable` that will read all the tables into memory and allows you to interactively look thru them. The function `results.readhtml.titletable` can be very slow on large HTML files.

    This function is useful when you know which file you are looking for. It does not work with negative indices, like you can in a list. If you know a way to make negative indices work, do a pull request :-)

    Parameters
    ----------
    fhandle : file like object
        A file handle to the E+ HTML table file
    index: int
        This is the index of the table you are looking for

    Returns
    -------
    titleandtable : (str, list)
        - (title, table)
            - title = previous item with a <b> tag
            - table = rows -> [[cell1, cell2, ..], [cell1, cell2, ..], ..]
    """
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
