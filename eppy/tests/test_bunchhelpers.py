# Copyright (c) 2012 Santosh Philip

"""pytest for bunchhelpers"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import eppy.bunchhelpers as bunchhelpers

def test_onlylegalchar():
    """py.test for onlylegalchar"""
    data = (
        ('abc', 'abc'), # name, newname
        ('abc {mem}', 'abc mem'), # name, newname
        ('abc {mem} #1', 'abc mem 1'), # name, newname
    )
    for name, newname in data:
        result = bunchhelpers.onlylegalchar(name)
        assert result == newname

def test_makefieldname():
    """py.test for makefieldname"""
    data = (
        ('aname', 'aname'), # namefromidd, bunchname
        ('a name', 'a_name'), # namefromidd, bunchname
        ('a name #1', 'a_name_1'), # namefromidd, bunchname
    )
    for namefromidd, bunchname in data:
        result = bunchhelpers.makefieldname(namefromidd)
        assert result == bunchname

def testintinlist():
    """pytest for intinlist"""
    data = (
        ('this is', False), # lst, hasint
        ('this is 1', True), # lst, hasint
        ('this 54 is ', True), # lst, hasint
    )
    for lst, hasint in data:
        result = bunchhelpers.intinlist(lst)
        assert result == hasint

def test_replaceint():
    """pytest for replaceint"""
    data = (
        ('this is', 'this is'), # fname, newname
        ('this is 54', 'this is %s'), # fname, newname
        # ('this is #54', 'this is %s'), # fname, newname
    )
    for fname, newname in data:
        result = bunchhelpers.replaceint(fname)
        assert result == newname

