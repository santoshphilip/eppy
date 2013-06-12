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

#!/usr/bin/env python
# encoding: utf-8
"""
reads e.txt as the sketchup output file
save the it as e.idf
"""

import sys
import os

import makeidf


def main():
    """
    reads e.txt as the sketchup output file
    save the it as e.idf
    """
    fname = 'e.txt'
    txt = open(fname, 'r').read()
    eplustxt = makeidf.makeidf(txt) 
    open('e.idf', 'wb').write(eplustxt)


if __name__ == '__main__':
    main()

