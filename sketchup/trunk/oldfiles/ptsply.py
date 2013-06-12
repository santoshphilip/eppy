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

import upfront
from flatten import flatten

txt = open('a.txt', 'r').read()
lst = txt.split('--------------------')
lst.pop(0)
lst1 = [block.splitlines()[1:] for block in lst]
from flatten import flatten
lst2 = [x.split(',') for x in flatten(lst1)]
pts = [[float(p) for p in pt] for pt in lst2]
nn = 0
outer = []
for i,  item in enumerate(lst1):
    inner = []
    for j in range(len(item)):
        inner.append(nn)
        nn += 1
    outer.append(inner)

upfront.saveupfver1((pts, outer), outfile='b.up1')
