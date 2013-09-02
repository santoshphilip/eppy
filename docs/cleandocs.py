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


"""clean up the docs diles in this folder"""

import shutil
import os
pth = "./generated"
if  os.path.exists(pth):
    shutil.rmtree(pth)
# rm -r ./generated
pth1, pth2 = "./_build/html", "./generated" 
if  os.path.exists(pth1):
    shutil.move(pth1, pth2)
pth = "./_build"
if  os.path.exists(pth):
    shutil.rmtree(pth)
pth = "./_templates"
if  os.path.exists(pth):
    shutil.rmtree(pth)
# mv ./_build/html ./generated
# rm -r _build
# rm -r _templates
