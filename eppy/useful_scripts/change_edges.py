# Copyright (c) 2012 Santosh Philip
# =======================================================================
#  Distributed under the MIT License.
#  (See accompanying file LICENSE or copy at
#  http://opensource.org/licenses/MIT)
# =======================================================================
"""change the edges in loopdaigram so that there are no names with colons (:) """
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals


def replace_colon(s, replacewith="__"):
    """replace the colon with something"""
    return s.replace(":", replacewith)


def clean_edges(arg):
    if isinstance(arg, str):  # Python 3: isinstance(arg, str)
        return replace_colon(arg)
    try:
        return tuple(clean_edges(x) for x in arg)
    except TypeError:  # catch when for loop fails
        return replace_colon(arg)  # not a sequence so just return repr

        # start pytests +++++++++++++++++++++++


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


# end pytests +++++++++++++++++++++++
