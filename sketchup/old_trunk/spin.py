"""testing to see in what order the points in sketchup are given
Results: Right hand corkscrew in the direction of the normal"""

from Scientific.Geometry import Vector
import readsketchup
import geometry

txt = open('e.txt', 'r').read()
dct = readsketchup.readsketchup(txt)
for key in dct.keys():
    plane = dct[key]['points']
    normal = Vector(dct[key]['normal'])
    calcnormal = geometry.facenormal(plane)
    # print normal
    # print calcnormal
    print normal.angle(calcnormal)
    print
    