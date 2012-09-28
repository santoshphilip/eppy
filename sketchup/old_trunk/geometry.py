"""simple 3D geometry functions"""

# from Scientific.Geometry import Vector
import math

# def linevector3d(p1, p2):
#     """return a vector from 3D point p1 to p2"""
#     p = [c2-c1 for c1, c2 in zip(p1, p2)]
#     return Vector(p)
# 
# def facenormal(plane, reverse=False):
#     """return the normal to the plane
#     plane is a list of 3D points 
#     the order of the points is a right hand corkscrew in the direction of the normal
#     reverse=True will use a left hand corkscrew
#     ====================
#     - rewrite this to take into consideration that the 
#     first 3 points might form a straight line"""
#     threepoints = plane[:3]
#     p1, p2, p3 = threepoints[0], threepoints[1], threepoints[2]
#     v1, v2 = linevector3d(p2, p3), linevector3d(p2, p1)
#     v =  v1.cross(v2)
#     return v

def poly2triangles(poly):
    """convert a polygon to many triangles
    where poly = (p1, p2, p3, p4) and p = (x, y, z)
    presently works only for convex polygons"""
    return [(poly[0], p2, p3) for p2, p3 in zip(poly[1:-1], poly[2:])]

def trianglearea3d(poly):
    """return the area of the triangle from:
    Area = sqrt(s*(s-a)*(s-b)*(s-c)) where s=(a+b+c)/2 is the semi-perimeter"""
    p1, p2, p3 = poly
    a = linelength3d(p1, p2)
    b = linelength3d(p2, p3)
    c = linelength3d(p3, p1)
    s = (a + b + c)/2
    return math.sqrt(s * (s - a) * (s - b) * (s - c))
    

def linelength3d(p1, p2):
    """return the length of the line from p1 to p2
    where p = (x, y, z)"""
    (x1, y1, z1), (x2, y2, z2) = p1, p2
    return math.sqrt((x1 - x2) * (x1 - x2) + \
                (y1 - y2) * (y1 - y2) + \
                (z1 - z2) * (z1 - z2))

def polygonarea3d(poly):
    """return the area of the polygon
    where: poly = (p1, p2, p3, p4, p5) p = (x, y, z)
    presently works only for convex polygons"""
    triangles = poly2triangles(poly)
    tareas = [trianglearea3d(tri) for tri in triangles]
    return sum(tareas)