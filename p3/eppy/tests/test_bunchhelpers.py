# Copyright (c) 2012 Santosh Philip

# This file is part of eppy.

# Eppy is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# Eppy is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with eppy.  If not, see <http://www.gnu.org/licenses/>.

"""pytest for bunchhelpers"""






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

