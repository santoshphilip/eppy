# Copyright (c) 2012 Santosh Philip
# Copyright (c) 2016 Jamie Bull
# =======================================================================
#  Distributed under the MIT License.
#  (See accompanying file LICENSE or copy at
#  http://opensource.org/licenses/MIT)
# =======================================================================
"""py.test for loopdiagram.py"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os

import pytest

from eppy.useful_scripts.loopdiagram import clean_edges
from eppy.useful_scripts.loopdiagram import dropnodes
from eppy.useful_scripts.loopdiagram import edges2nodes
from eppy.useful_scripts.loopdiagram import process_idf
from eppy.useful_scripts.loopdiagram import replace_colon
from eppy.pytest_helpers import do_integration_tests


THIS_DIR = os.path.dirname(os.path.abspath(__file__))

RESOURCES_DIR = os.path.join(THIS_DIR, os.pardir, "eppy", "resources")

IDD_FILES = os.path.join(RESOURCES_DIR, "iddfiles")
IDF_FILES = os.path.join(RESOURCES_DIR, "idffiles")


def test_dropnodes():
    """py.test for dropnodes"""
    # test 1
    node = "node"
    (a, b, c, d, e, f, g, h, i) = (
        ("a", node),
        "b",
        ("c", node),
        "d",
        ("e", node),
        "f",
        ("g", node),
        "h",
        ("i", node),
    )
    edges = [(a, b), (b, c), (c, d), (d, e), (e, f), (f, g), (g, h), (h, i)]
    theresult = [("a", "b"), ("b", "d"), ("d", "f"), ("f", "h"), ("h", "i")]
    result = dropnodes(edges)
    assert result == theresult
    # test 2
    (a, b, c, d, e, f, g, h, i, j) = (
        ("a", node),
        "b",
        ("c", node),
        ("d", node),
        "e",
        "f",
        ("g", node),
        ("h", node),
        "i",
        ("j", node),
    )
    edges = [
        (a, b),
        (b, c),
        (c, e),
        (e, g),
        (g, i),
        (i, j),
        (b, d),
        (d, f),
        (f, h),
        (h, i),
    ]
    theresult = [("a", "b"), ("b", "e"), ("e", "i"), ("i", "j"), ("b", "f"), ("f", "i")]
    result = dropnodes(edges)
    assert result == theresult


def test_edges2nodes():
    """py.test for edges2nodes"""
    thedata = (
        ([("a", "b"), ("b", "c"), ("c", "d")], ["a", "b", "c", "d"]),  # edges, nodes
    )
    for edges, nodes in thedata:
        result = edges2nodes(edges)
        assert result == nodes


def test_replace_colon():
    """py.test for replace_colon"""
    data = (("zone:aap", "@", "zone@aap"),)  # s, r, replaced
    for s, r, replaced in data:
        result = replace_colon(s, r)
        assert result == replaced


def test_cleanedges():
    """py.test for cleanedges"""
    data = (
        (
            [("a:a", "a"), (("a", "a"), "a:a"), ("a:a", ("a", "a"))],
            (("a__a", "a"), (("a", "a"), "a__a"), ("a__a", ("a", "a"))),
        ),
        # edg, clean_edg
    )
    for edg, clean_edg in data:
        result = clean_edges(edg)
        assert result == clean_edg


@pytest.mark.skipif(
    not do_integration_tests(), reason="$EPPY_INTEGRATION env var not set"
)
def test_loopdiagram_integration():
    """End-to-end smoke test on an example file"""
    idd = os.path.join(IDD_FILES, "Energy+V8_1_0.idd")
    fname = os.path.join(IDF_FILES, "V8_1_0/Boiler.idf")
    process_idf(fname, idd)
