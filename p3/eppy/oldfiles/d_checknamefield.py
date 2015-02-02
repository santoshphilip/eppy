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


"""Name fields may end with Name rather than be Name
test this
conclusion: just check if the field has a reference"""

from modeleditor import IDF
from io import StringIO
iddname = "../iddfiles/Energy+V8_0_0.idd"
IDF.setiddname(iddname)
idf = IDF(StringIO(""))
idds = idf.idd_info
i = 0
bpoint = 5
for fieldidds in idds:
    i += 1
    for fieldidd in fieldidds:
        if 'field' in fieldidd and 'reference' in fieldidd:
            if fieldidd['field'][0].find('Name') != -1:
                if fieldidd['field'][0] != 'Name':
                    print(fieldidd['field'][0], idf.model.dtls[i])
    if i > bpoint:
        pass

