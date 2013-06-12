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

readdatacommdct(idfname, iddfile='Energy+.idd') # takes filename
    block,commlst,commdct=parse_idd.extractidddata(iddfile) # takes filename
        # opened only once in function. 
    data = eplusdata.eplusdata(theidd,idfname) # idfname is a filename
        eplusdata.eplusdata.__init__ 
            # if statement has to respond to fname being a file obejct
        eplusdata.eplusdata.makedict(dictfile, fname) # fname is a filename


