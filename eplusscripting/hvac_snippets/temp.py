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

"""py.test for hvacbuilder"""
import sys
import os
sys.path.append('../')
from modeleditor import IDF
from StringIO import StringIO

iddname = "../../iddfiles/Energy+V6_0.idd"
idfname = "h.idf"

import snippet
iddtxt = snippet.iddtxt
idftxt = snippet.idftxt

IDF.setiddname(StringIO(iddtxt))
IDF.setiddname(iddname)
idf = IDF(StringIO(idftxt))

# IDF.setiddname(StringIO(iddtxt))
idf = IDF(StringIO(idftxt))

idf.printidf()


# from modeleditor import IDF
# from StringIO import StringIO
# iddname = "../iddfiles/Energy+V6_0.idd"
# idfname = "./hvac_snippets/h.idf"
# IDF.setiddname(iddname)
# idf = IDF(idfname)
