# Copyright (c) 2012 Santosh Phillip

# This file is part of eplusinterface_diagrams.

# Eplusinterface_diagrams is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# Eplusinterface_diagrams is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with eplusinterface_diagrams.  If not, see <http://www.gnu.org/licenses/>.

"""read first line from runlist.tmp
make a batch file with it, 
delete that line and save runlist.tmp
-
if line is:
    dosomething abc | dosomethingelse xyz
the batch file is:
    dosomething abc
    dosomethingelse xyz"""
    
fname = "runlist.tmp"
batname = 'meplus_main.bat'
txt = open(fname, 'r').read()
lines = txt.splitlines()
try:
    first = lines.pop(0)
    open(fname, 'w').write('\n'.join(lines))

    firstlines = first.split('|')
    firstlines = [line.strip() for line in firstlines]
    open(batname, 'w').write('\n'.join(firstlines))
except IndexError, e:
    open(batname, 'w').write('REM ====== task complete ========')
