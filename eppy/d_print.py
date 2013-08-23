# Copyright (c) 2013 Santosh Philip

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

from modeleditor import IDF

from StringIO import StringIO
import iddv7
IDF.setiddname(StringIO(iddv7.iddtxt))
idf1 = IDF(StringIO(''))

ploop = idf1.newidfobject('PLANTLOOP', 'p_loop')
cloop = idf1.newidfobject('CONDENSERLOOP', 'c_loop')
idf1.outputtype = 'nocomment'
idf1.outputtype = 'compressed'
idf1.saveas('gumby.idf')
# print idf1.idfstr()
