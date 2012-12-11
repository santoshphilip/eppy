""""This module is used for calculation of zone area for E+ surfaces"""
# Wrote by Tuan Tran trantuan@hawaii.edu / tranhuuanhtuan@gmail.com
# School of Architecture, University of Hawaii at Manoa

# import area_surface as surf
import surface 

def area(poly):
    """Calculation of zone area"""
    poly_xy = []
    N = len(poly)
    for i in range(N):
        poly[i] = poly[i][0:2] + (0,)
        poly_xy.append(poly[i])
    return surface.area(poly)