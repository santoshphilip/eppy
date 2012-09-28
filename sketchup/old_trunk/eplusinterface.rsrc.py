{'application':{'type':'Application',
          'name':'Minimal',
    'backgrounds': [
    {'type':'Background',
          'name':'bgMin',
          'title':'Minimal PythonCard Application',
          'size':(200, 100),
          'icon':'database.ico',
          'visible':0,

        'menubar': {'type':'MenuBar',
         'menus': [
             {'type':'Menu',
             'name':'menuFile',
             'label':'File',
             'items': [
                  {'type':'MenuItem',
                   'name':'menuFileAbout',
                   'label':'&About\tAlt+a',
                   'command':'about',
                  },
                  {'type':'MenuItem',
                   'name':'menuFileExit',
                   'label':'E&xit\tAlt+X',
                   'command':'exit',
                  },
              ]
             },
         ]
     },
         'components': [

] # end components
} # end background
] # end backgrounds
} }
