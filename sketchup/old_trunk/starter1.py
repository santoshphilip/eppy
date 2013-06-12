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

#!/usr/bin/python

"""
__version__ = "$Revision: 1.8 $"
__date__ = "$Date: 2005/12/17 15:20:02 $"
"""

from PythonCard import model


class Minimal(model.Background):
    def on_menuFileAbout_select(self, event):
        pass

if __name__ == '__main__':
    app = model.Application(Minimal)
    app.MainLoop()
