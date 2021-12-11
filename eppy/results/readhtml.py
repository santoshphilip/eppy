# Copyright (c) 2012 Santosh Philip
# =======================================================================
#  Distributed under the MIT License.
#  (See accompanying file LICENSE or copy at
#  http://opensource.org/licenses/MIT)
# =======================================================================

"""read the html outputs"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import string
import collections
from bs4 import BeautifulSoup, NavigableString, Tag


class NotSimpleTable(Exception):
    """Exception Object"""

    pass


def tdbr2EOL(td):
    """convert the <br/> in <td> block into line ending (EOL = \n)"""
    for br in td.find_all("br"):
        br.replace_with("\n")
    txt = str(td)  # make it back into test
    # would be unicode(id) in python2
    soup = BeautifulSoup(txt, "lxml")  # read it as a BeautifulSoup
    ntxt = soup.find("td")  # BeautifulSoup has lot of other html junk.
    # this line will extract just the <td> block
    return ntxt


def is_simpletable(table):
    """test if the table has only strings in the cells"""
    tds = table("td")
    for td in tds:
        if td.contents != []:
            td = tdbr2EOL(td)
            if len(td.contents) == 1:
                thecontents = td.contents[0]
                if not isinstance(thecontents, NavigableString):
                    return False
            else:
                return False
    return True


def table_withcelltag_2matrix(table):
    """convert a table to a list of lists - a 2D matrix
    but ignores tags within a cell"""
    # an idf object has a name like "glass <thicknessis 3mm>"
    # the "<thicknessis 3mm>" will be changed by soup into
    # "<thicknessis 3mm><</thicknessis 3mm>"
    # which is a tag inside the cell - so it is not a simpletable
    # this function will ignore the tag inside the cell
    rows = []
    for tr in table("tr"):
        row = []
        for td in tr("td"):
            td = tdbr2EOL(td)  # convert any '<br>' in the td to line ending
            row.append(cell2txt(td))
        rows.append(row)
    return rows


def table2matrix(table):
    """convert a table to a list of lists - a 2D matrix"""

    if not is_simpletable(table):
        # if it is not a simple table, it is because an idf object has a name
        # like "glass <thicknessis 3mm>"
        # the "<thicknessis 3mm>" will be changed by soup into
        # "<thicknessis 3mm><</thicknessis 3mm>"
        # which is a tag inside the cell - so it is not a simpletable
        # so we need another function
        return table_withcelltag_2matrix(table)
    rows = []
    for tr in table("tr"):
        row = []
        for td in tr("td"):
            td = tdbr2EOL(td)  # convert any '<br>' in the td to line ending
            try:
                row.append(td.contents[0])
            except IndexError:
                row.append("")
        rows.append(row)
    return rows


def table_withcelltag_2val_matrix(table):
    """convert a table to a list of lists - a 2D matrix
    Converts numbers to float
    but ignores tags within a cell"""
    # an idf object has a name like "glass <thicknessis 3mm>"
    # the "<thicknessis 3mm>" will be changed by soup into
    # "<thicknessis 3mm><</thicknessis 3mm>"
    # which is a tag inside the cell - so it is not a simpletable
    # this function will ignore the tag inside the cell
    rows = []
    for tr in table("tr"):
        row = []
        for td in tr("td"):
            td = tdbr2EOL(td)
            val = cell2txt(td)
            try:
                val = float(val)
                row.append(val)
            except ValueError:
                row.append(val)
        rows.append(row)
    return rows


def table2val_matrix(table):
    """convert a table to a list of lists - a 2D matrix
    Converts numbers to float"""
    if not is_simpletable(table):
        # raise NotSimpleTable("Not able read a cell in the table as a string")
        # run a different function for nonsimple table
        # if it is not a simple table, it is because an idf object has a name
        # like "glass <thicknessis 3mm>"
        # the "<thicknessis 3mm>" will be changed by soup into
        # "<thicknessis 3mm><</thicknessis 3mm>"
        # which is a tag inside the cell - so it is not a simpletable
        # so we need another function
        return table_withcelltag_2val_matrix(table)
    rows = []
    for tr in table("tr"):
        row = []
        for td in tr("td"):
            td = tdbr2EOL(td)
            try:
                val = td.contents[0]
            except IndexError:
                row.append("")
            else:
                try:
                    val = float(val)
                    row.append(val)
                except ValueError:
                    row.append(val)
        rows.append(row)
    return rows


def titletable(html_doc, tofloat=True):
    """return a list of [(title, table), .....]

    title = previous item with a <b> tag
    table = rows -> [[cell1, cell2, ..], [cell1, cell2, ..], ..]"""
    soup = BeautifulSoup(html_doc, "html.parser")
    btables = soup.find_all(["b", "table"])  # find all the <b> and <table>
    titletables = []
    for i, item in enumerate(btables):
        if item.name == "table":
            for j in range(i + 1):
                if btables[i - j].name == "b":  # step back to find a <b>
                    break
            titletables.append((btables[i - j], item))
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
        if name == None:
            return False
        return True
    except AttributeError:
        return False


def lines_table(html_doc, tofloat=True):
    """return a list of [(lines, table), .....]

    lines = all the significant lines before the table.
    These are lines between this table and
    the previous table or 'hr' tag

    table = rows -> [[cell1, cell2, ..], [cell1, cell2, ..], ..]

    The lines act as a description for what is in the table
    """
    soup = BeautifulSoup(html_doc, "html.parser")
    linestables = []
    elements = soup.p.next_elements  # start after the first para
    for element in elements:
        tabletup = []
        if not _has_name(element):
            continue
        if element.name == "table":  # hit the first table
            beforetable = []
            prev_elements = element.previous_elements  # walk back and get the lines
            for prev_element in prev_elements:
                if not _has_name(prev_element):
                    continue
                if prev_element.name not in ("br", None):  # no lines here
                    if prev_element.name in ("table", "hr", "tr", "td"):
                        # just hit the previous table. You got all the lines
                        break
                    if prev_element.parent.name == "p":
                        # if the parent is "p", you will get it's text anyways from the parent
                        pass
                    else:
                        if prev_element.get_text():  # skip blank lines
                            beforetable.append(prev_element.get_text())
            beforetable.reverse()
            tabletup.append(beforetable)
            function_selector = {True: table2val_matrix, False: table2matrix}
            function = function_selector[tofloat]
            tabletup.append(function(element))
        if tabletup:
            linestables.append(tabletup)
    return linestables


def _asciidigits(s):
    """if s is not ascii or digit, return an '_'"""
    if s not in string.ascii_letters + string.digits:
        s = "_"
    return s


def _nospace(s):
    """replace all non-ascii, non_digit or space with '_'"""
    return "".join([_asciidigits(i) for i in s])


def _transpose(arr):
    return list(map(list, list(zip(*arr))))


def _make_ntgrid(grid):
    """make a named tuple grid

    [["",  "a b", "b c", "c d"],
     ["x y", 1,     2,     3 ],
     ["y z", 4,     5,     6 ],
     ["z z", 7,     8,     9 ],]
    will return
    ntcol(x_y=ntrow(a_b=1, b_c=2, c_d=3),
          y_z=ntrow(a_b=4, b_c=5, c_d=6),
          z_z=ntrow(a_b=7, b_c=8, c_d=9))"""
    hnames = [_nospace(n) for n in grid[0][1:]]
    vnames = [_nospace(row[0]) for row in grid[1:]]
    vnames_s = " ".join(vnames)
    hnames_s = " ".join(hnames)
    ntcol = collections.namedtuple("ntcol", vnames_s)
    ntrow = collections.namedtuple("ntrow", hnames_s)
    rdict = [dict(list(zip(hnames, row[1:]))) for row in grid[1:]]
    ntrows = [ntrow(**rdict[i]) for i, name in enumerate(vnames)]
    ntcols = ntcol(**dict(list(zip(vnames, ntrows))))
    return ntcols


def named_grid_h(grid):
    """make a horizontal named grid"""
    return _make_ntgrid(grid)


def named_grid_v(grid):
    """make a vertical named grid"""
    return _make_ntgrid(_transpose(grid))


def cell2txt(td):
    """clean up the td and return text in it
    It will ignore any tags within the td"""
    td = tdbr2EOL(td)
    lst = []
    for txt in td.contents:
        try:
            a = txt.contents
        except AttributeError as e:
            lst.append(txt)
    return "".join(lst)
