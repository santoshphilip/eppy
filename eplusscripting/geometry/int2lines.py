# Find the intersection between two lines
# V = (1/6)*|(a-d).((b-d)x(c-d))|
import numpy as np
def vol_tehrahedron(poly):
    """volume of a irregular tetrahedron"""
    a = np.array(poly[0])
    b = np.array(poly[1])
    c = np.array(poly[2])
    d = np.array(poly[3])
    return abs(np.dot((a-d),np.cross((b-d),(c-d))) / 6)

poly = [(0.0,0.0,0.0),(1.0,0.0,0.0),(1.0,1.0,0.0),(0.0,0.0,1.0)]

def central_p(poly1,poly2):
    """central point of a prism"""
    central_point = np.array([0.0,0.0,0.0])
    for i in range(len(poly1)):
        central_point += np.array(poly1[i]) + np.array(poly2[i])
    return central_point/ (len(poly1)) / 2

poly1 = [(0.0,0.0,0.0),(1.0,0.0,0.0),(1.0,1.0,0.0),(0,1.0,0.0)]
poly2 = [(0.0,0.0,1),(1.0,0.0,1),(1.0,1.0,1),(0,1.0,1)]

def vol_zone(poly1,poly2):
    """"volume of a zone defined by two polygon bases """
    c_point = central_p(poly1,poly2)
    c_point = (c_point[0],c_point[1],c_point[2])
    vol_therah = 0
    N = len(poly1)
    for i in range(N-2):
        # the upper part
        tehrahedron = [c_point,poly1[0],poly1[i+1],poly1[i+2]]
        vol_therah += vol_tehrahedron(tehrahedron)
        # the bottom part
        tehrahedron = [c_point,poly2[0],poly2[i+1],poly2[i+2]]
        vol_therah += vol_tehrahedron(tehrahedron)
    # the middle part
    for i in range(N-1):
        tehrahedron = [c_point,poly1[i],poly2[i],poly2[i+1]]
        vol_therah += vol_tehrahedron(tehrahedron)
        tehrahedron = [c_point,poly1[i],poly1[i+1],poly2[i]]
        vol_therah += vol_tehrahedron(tehrahedron)
    tehrahedron = [c_point,poly1[N-1],poly2[N-1],poly2[0]]
    vol_therah += vol_tehrahedron(tehrahedron)
    tehrahedron = [c_point,poly1[N-1],poly1[0],poly2[0]]
    vol_therah += vol_tehrahedron(tehrahedron)
    return vol_therah
    
