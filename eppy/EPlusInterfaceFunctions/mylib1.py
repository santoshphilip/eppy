# EPlusInterface (EPI) - An interface for EnergyPlus
# Copyright (C) 2004 Santosh Philip

# This file is part of EPlusInterface.
#
# EPlusInterface is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# EPlusInterface is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with EPlusInterface; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA


# Santosh Philip, the author of EPlusInterface, can be contacted at the following email address:
# santosh_philip AT yahoo DOT com
# Please send all bug reports, enhancement proposals, questions and comments to that address.
#
# VERSION: 0.001

"""Legacy code from EPlusInterface"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals




def write_str2file(pathname, astr):
    """writes a string to file"""
    fname = pathname
    fhandle = open(fname, 'wb')
    fhandle.write(astr)
    fhandle.close()

def readfile(pathname):
    """retrun the data in the file"""
    fhandle = open(pathname, 'rb')
    data = fhandle.read()
    data = data.decode('ISO-8859-2')
    fhandle.close()
    return data

def readfileasmac():
    """docstring for readfileasmac"""
    return None