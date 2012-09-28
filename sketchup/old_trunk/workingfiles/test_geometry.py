"""py.test routines for geometry.py"""

# from Scientific.Geometry import Vector
import geometry
from pydottest import almostequals
    
    
# def test_linevector3d():
#     """py.test for linevector3d()"""
#     p1, p2 = (4, 5, 7), (8, 7, 5)
#     v = Vector(4, 2, -2)
#     assert geometry.linevector3d(p1, p2) == v

# def test_facenormal():
#     """py.test for facenormal()"""
#     data = (
#         (((180.0, 0.0, 0.0), (180.0, 144.0, 0.0),
#          (180.0, 144.0, 60.0), (180.0, 0.0, 60.0)),
#          (1.0, 0.0, 0.0)),
#         (((180.0, 0.0, 0.0), (281.823376490863, 101.823376490863, 0.0),
#          (281.823376490863, 101.823376490863, 60.0), (180.0, 0.0, 60.0)),
#          (0.707106781186547, -0.707106781186548, 0.0)),
#         (((180.0, 0.0, 0.0), (270.966091219871, 101.823376490863, 45.751177560564),
#          (244.006951302916, 101.823376490863, 99.3534608602341), (153.040860083046, 0.0, 53.6022832996702)),
#          (0.631708966804655, -0.707106781186547, 0.317716510837249)),
#     )
#     for plane, normal in data:
#         result = geometry.facenormal(plane)
#         vnormal = Vector(normal)
#         assert result.angle(vnormal) == 0.0

def test_poly2triangles():
    """py.test for poly2triangles"""
    data = (
    ([1,2,3,4,5,6], [(1, 2, 3), (1, 3, 4), (1, 4, 5), (1, 5, 6)]),
    ([1,2,3,4,5], [(1, 2, 3), (1, 3, 4), (1, 4, 5)]),
    ([1,2,3],[(1,2,3)]),
    ) 
    for poly, triangles in data:
        assert geometry.poly2triangles(poly) == triangles

def test_lindelength3d():
    """py.test for linelength3d()"""
    lgt = 155
    p1 = (29.7354611812028, 73.6063721969898, -7.105427357601e-15)
    p2 = (77.1440837563596, 198.709264913276, 78.2731674301201)
    result = geometry.linelength3d(p1, p2)
    assert almostequals(result, lgt)

def test_trianglearea3d():
    """py.test for trianglearea3d()"""
    poly = ((234.261130830644, 91.3751730360274, 1.4210854715202e-14), \
            (29.7354611812028, 73.6063721969898, -7.105427357601e-15), \
            (77.1440837563596, 198.709264913276, 78.2731674301201))
    area = 14752.132411125584
    result = geometry.trianglearea3d(poly)
    assert almostequals(result, area)

def test_polygonarea3d():
    """py.test or polygonarea3d()"""
    poly = [[97.952770165533494, -89.688089019337596, 1.23613716318408e-14],
     [-42.113949041963799, -48.668412230783197, 4.3225283531169101e-15],
     [-176.015056172523, 95.487947355641097, 9.98244187111785e-15],
     [-59.700839733667401, 203.52759542159399, 9.98244187111785e-15],
     [193.10639752719001, 28.032400933162201, 2.21573588081702e-14],
     [175.70277016553399, -89.688089019337596, 1.23613716318408e-14]]
    area = 60724.6427925073
    result = geometry.polygonarea3d(poly)
    assert almostequals(result, area)