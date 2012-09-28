
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

