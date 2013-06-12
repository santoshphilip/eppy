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


{ 'application':{ 'type':'Application',
            'name':'Minimal',

    'backgrounds':
 [ 
  { 'type':'Background',
    'name':'bgMin',
    'title':'Minimal PythonCard Application',
    'size':( 200, 100 ),

    'menubar': 
    { 
        'type':'MenuBar',
        'menus': 
        [
            { 'type':'Menu',
              'name':'menuFile',
              'label':'File',
              'items': [ 
                { 'type':'MenuItem',
                  'name':'menuFileAbout',
                  'label':'&About\tAlt+a',
                  'command':'about' },
                { 'type':'MenuItem',
                  'name':'menuFileExit',
                  'label':'E&xit\tAlt+X',
                  'command':'exit' } ,
                  ] },
        ]       
    },

   'components':
   [ 
    { 'type':'TextField',
      'name':'field1',
      'position':(0, 0),
      'text':'Hello PythonCard' },
   ]
  }
 ]
 }
 }

