Numpy functions to be recreated in Python

1. [x] Cross product
2. [x] Dot product
3. [ ] Determinant
4. [ ] Array
5. [ ] Square root
6. [ ] Arc-cosine

-------------------------------------------------------------------------------------------------------------------------

Searching 8 files for "np."

/Users/eayoungs/repo/Code/SimTools/Scripting/eppy/eppy/geometry/height_surface.py:
   32:         prod = np.**cross**(vi1, vi2)
   36:     result = np.**dot**(total, unit_normal(poly[0], poly[1], poly[2]))
   49:     x = np.linalg.**det**([[1,a[1],a[2]],[1,b[1],b[2]],[1,c[1],c[2]]])

/Users/eayoungs/repo/Code/SimTools/Scripting/eppy/eppy/geometry/int2lines.py:
   23:     a = np.**array**(poly[0])

/Users/eayoungs/repo/Code/SimTools/Scripting/eppy/eppy/geometry/surface.py:
   90:     vec1_modulus = np.**sqrt**((vec1*vec1).sum())
   95:     return math.degrees(np.**arccos**(cos_angle)) 
