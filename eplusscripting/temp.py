# Copyright (c) 2012 Santosh Phillip

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

"""just stuff"""

def getnamedargs(*args, **kwargs):
    """allows you to pass a dict and named args
    so you can pass ({'a':5, 'b':3}, c=8) and get
    dict(a=5, b=3, c=8)"""
    adict = {}
    for arg in args:
        if isinstance(arg, dict):
            adict.update(arg)
    adict.update(kwargs)
    return adict
    
def test_getnamedargs():
    """py.test for getnamedargs"""
    result = dict(a=1, b=2, c=3)
    assert result == getnamedargs(a=1, b=2, c=3)
    assert result == getnamedargs(dict(a=1, b=2, c=3))
    assert result == getnamedargs(dict(a=1, b=2), c=3)
    assert result == getnamedargs(dict(a=1), c=3, b=2)
    
# printkeywords(Name='Santosh', Last='Philip')
# printkeywords(dict(Name='Santosh', Last='Philip'))