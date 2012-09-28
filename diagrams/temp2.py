"""testing unicode make diagrams.
Can be deleted once done"""

import diagram

edges = (('a', 'b'), ('a', 'c'))
edges = ((('a', "epnode"), 'b:d'), (('a', "epnode"), 'c'))
edges = diagram.cleanedges(edges)
g = diagram.makediagram(edges)
g.write_png('a.png')

