# Copyright (c) 2012 Santosh Philip
# =======================================================================
#  Distributed under the MIT License.
#  (See accompanying file LICENSE or copy at
#  http://opensource.org/licenses/MIT)
# =======================================================================

"""py.test for readhtml.py"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import pytest
import collections
from bs4 import BeautifulSoup
import eppy.results.readhtml as readhtml
from .sample_html import sample_html as SAMPLE_HTML


def test_table2matrix():
    """py.test for table2matrix"""
    thedata = (
        (
            """<table border="1" cellspacing="0" cellpadding="4">
                <tr>
                    <td>1</td>
                    <td>2</td>
                </tr>
                <tr>
                    <td>3</td>
                    <td>4</td>
                </tr>
            </table>""",
            [["1", "2"], ["3", "4"]],
        ),  # tabletxt, rows
        # test when there is crud in the cell of the table
        (
            """<table border="1" cellspacing="0" cellpadding="4">
                <tr>
                    <td>1<aaa>something</aaa></td>
                    <td>2</td>
                </tr>
                <tr>
                    <td>3</td>
                    <td>4</td>
                </tr>
            </table>""",
            [["1", "2"], ["3", "4"]],
        ),  # tabletxt, rows
    )
    for tabletxt, rows in thedata:
        soup = BeautifulSoup(tabletxt, "lxml")
        table = soup.find("table")
        result = readhtml.table2matrix(table)
        assert result == rows


def test_table2val_matrix():
    """py.test for table2val_matrix"""
    thedata = (
        (
            """<table border="1" cellspacing="0" cellpadding="4">
            <tr>
                <td>b</td>
                <td>2</td>
            </tr>
            <tr>
                <td>3</td>
                <td>4</td>
            </tr>
            </table>""",
            [["b", 2], [3, 4]],
        ),  # tabletxt, rows
        # the following test data has a <br> in the <td></td>
        # it will test if tdbr2EOL works correctly
        (
            """<table border="1" cellspacing="0" cellpadding="4">
            <tr>
                <td>b <br> b</td>
                <td>2</td>
            </tr>
            <tr>
                <td>3</td>
                <td>4</td>
            </tr>
            </table>""",
            [["b \n b", 2], [3, 4]],
        ),  # tabletxt, rows
        # has a tag in a cell
        (
            """<table border="1" cellspacing="0" cellpadding="4">
            <tr>
                <td>b<sometag> stuff </sometag></td>
                <td>2</td>
            </tr>
            <tr>
                <td>3</td>
                <td>4</td>
            </tr>
            </table>""",
            [["b", 2], [3, 4]],
        ),  # tabletxt, rows
    )
    for tabletxt, rows in thedata:
        soup = BeautifulSoup(tabletxt, "lxml")
        table = soup.find("table")
        result = readhtml.table2val_matrix(table)
        assert result == rows


def test_gettables():
    """py.test for gettables"""
    thedata = (
        (
            [
                ("Site and Source Energy", [["a", "2"], ["3", "4"]]),
                ("Site to Source Energy Conversion Factors", [["b", "6"], ["7", "8"]]),
                ("Custom Monthly Report", [["c", "16"], ["17", "18"]]),
                ("Custom Monthly Report", [["d", "26"], ["27", "28"]]),
            ],
            False,
        ),  # titlerows, tofloat
        (
            [
                ("Site and Source Energy", [["a", 2], [3, 4]]),
                ("Site to Source Energy Conversion Factors", [["b", 6], [7, 8]]),
                ("Custom Monthly Report", [["c", 16], [17, 18]]),
                ("Custom Monthly Report", [["d", 26], [27, 28]]),
            ],
            True,
        ),  # titlerows, tofloat
    )
    for titlerows, tofloat in thedata:
        result = readhtml.titletable(SAMPLE_HTML, tofloat=tofloat)
        for (title1, rows1), (title2, rows2) in zip(result, titlerows):
            assert title1 == title2
            assert rows1 == rows2
        assert result == titlerows


def test_has_name():
    """py.test for has_name"""
    soup = BeautifulSoup(SAMPLE_HTML, "lxml")
    # soup.p = <p><a href="#toc" style="float: right">Table of Contents</a></p>
    assert readhtml._has_name(soup.p) is True
    # soup.b = <b>EnergyPlus-Windows-OMP-32 7.2.0.006, YMD=2013.01.28 16:38</b>
    assert readhtml._has_name(soup.b) is True
    # soup.p.contents[0] = <a href="#toc" style="float: right">Table of Contents</a>
    assert readhtml._has_name(soup.p.contents[0]) is True
    # soup.b.contents[0] = u'EnergyPlus-Windows-OMP-32 7.2.0.006, YMD=2013.01.28 16:38'
    assert readhtml._has_name(soup.b.contents[0]) is False


def test_lines_table():
    """py.test for lines_table"""
    # soup = BeautifulSoup(SAMPLE_HTML)
    result = readhtml.lines_table(SAMPLE_HTML, False)
    assert result == [
        [
            [
                "Table of Contents",
                "Report: Annual Building Utility Performance Summary",
                "For: Entire Facility",
                "Timestamp: 2014-01-13\n    16:47:19",
                "Values gathered over      8760.00 hours",
                "Site and Source Energy",
            ],
            [["a", "2"], ["3", "4"]],
        ],
        [["Site to Source Energy Conversion Factors"], [["b", "6"], ["7", "8"]]],
        [
            [
                "Report: COMPONENTS OF PEAK ELECTRICAL DEMAND",
                "For: Meter",
                "Timestamp: 2014-01-13\n    16:47:19",
                "Custom Monthly Report",
            ],
            [["c", "16"], ["17", "18"]],
        ],
        [
            [
                "Report: COMPONENTS OF PEAK NET ELECTRICAL DEMAND",
                "For: Meter",
                "Timestamp: 2014-01-13\n    16:47:19",
                "Custom Monthly Report",
            ],
            [["d", "26"], ["27", "28"]],
        ],
    ]


def test_make_ntgrid():
    """py.test make_ntgrid"""
    grid = [
        ["", "a b", "b c", "c d"],
        ["x y", 1, 2, 3],
        ["y z", 4, 5, 6],
        ["z z", 7, 8, 9],
    ]
    result = readhtml._make_ntgrid(grid)
    ntcol = collections.namedtuple("ntcol", "x_y y_z z_z")
    ntrow = collections.namedtuple("ntrow", "a_b b_c c_d")
    assert result == ntcol(
        x_y=ntrow(a_b=1, b_c=2, c_d=3),
        y_z=ntrow(a_b=4, b_c=5, c_d=6),
        z_z=ntrow(a_b=7, b_c=8, c_d=9),
    )


# cell2txt
@pytest.mark.parametrize(
    "tdtxt, expected",
    [
        ('<td align="right">cell text</td>', "cell text"),  # tdtxt, expected
        (
            '<td align="right">cell text<aaa> </aaa></td>',
            "cell text",
        ),  # tdtxt, expected
        (
            '<td align="right">cell text<aaa> </aaa> more text</td>',
            "cell text more text",
        ),  # tdtxt, expected
        (
            '<td align="right">cell text<aaa> something here</aaa> more text</td>',
            "cell text more text",
        ),  # tdtxt, expected
        (
            '<td align="right"><aaa> </aaa>cell text</td>',
            "cell text",
        ),  # tdtxt, expected
        ('<td align="right"></td>', ""),  # tdtxt, expected
    ],
)
def test_cell2txt(tdtxt, expected):
    """py.test for cell2txt"""
    soup = BeautifulSoup(tdtxt, "html.parser")
    td = soup.td
    result = readhtml.cell2txt(td)
    assert result == expected
