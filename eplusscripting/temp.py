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

def unicodetest(s, filler="xxxxx"):
    """test for unicode, and return placholder if not unicode"""
    try:
        return s.decode('utf-8')
    except UnicodeDecodeError:
        return filler

fname = '../iddfiles/Energy+V8_0_0.idd'
fhandle = open(fname, 'r')
i = 0
for line in fhandle:
    i = i + 1
    for s in line:
        if unicodetest(s, 'superman') == 'superman':
            print i, line
