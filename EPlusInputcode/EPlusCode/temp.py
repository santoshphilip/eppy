# Copyright (c) 2012 Santosh Philip

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

import ncommdct
from EPlusInterfaceFunctions import parse_idd

iddname = './Energy+.idd'
iddname = './a.idd'
txt = open(iddname, 'r').read()
commdct = ncommdct.getcommdct(txt)
commlst = ncommdct.getcommlst(txt)
(nocom,nocom1,block)=parse_idd.get_nocom_vars(txt)
block1,commlst1,commdct1=parse_idd.extractidddata(iddname)
print commlst[0][-4]
