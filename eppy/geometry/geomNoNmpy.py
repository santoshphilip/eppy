def cross(a, b, axisa=-1, axisb=-1, axisc=-1, axis=None):
    """
    Return the cross product of two (arrays of) vectors.

    The cross product of `a` and `b` in :math:`R^3` is a vector perpendicular
    to both `a` and `b`.  If `a` and `b` are arrays of vectors, the vectors
    are defined by the last axis of `a` and `b` by default, and these axes
    can have dimensions 2 or 3.  Where the dimension of either `a` or `b` is
    2, the third component of the input vector is assumed to be zero and the
    cross product calculated accordingly.  In cases where both input vectors
    have dimension 2, the z-component of the cross product is returned.

    Parameters
    ----------
    a : array_like
        Components of the first vector(s).
    b : array_like
        Components of the second vector(s).
    axisa : int, optional
        Axis of `a` that defines the vector(s).  By default, the last axis.
    axisb : int, optional
        Axis of `b` that defines the vector(s).  By default, the last axis.
    axisc : int, optional
        Axis of `c` containing the cross product vector(s).  By default, the
        last axis.
    axis : int, optional
        If defined, the axis of `a`, `b` and `c` that defines the vector(s)
        and cross product(s).  Overrides `axisa`, `axisb` and `axisc`.

    Returns
    -------
    c : ndarray
        Vector cross product(s).

    Raises
    ------
    ValueError
        When the dimension of the vector(s) in `a` and/or `b` does not
        equal 2 or 3.

    See Also
    --------
    inner : Inner product
    outer : Outer product.
    ix_ : Construct index arrays.

    Notes
    -----
    .. versionadded:: 1.9.0
    Supports full broadcasting of the inputs.

    Examples
    --------
    Vector cross-product.

    >>> x = [1, 2, 3]
    >>> y = [4, 5, 6]
    >>> np.cross(x, y)
    array([-3,  6, -3])

    One vector with dimension 2.

    >>> x = [1, 2]
    >>> y = [4, 5, 6]
    >>> np.cross(x, y)
    array([12, -6, -3])

    Equivalently:

    >>> x = [1, 2, 0]
    >>> y = [4, 5, 6]
    >>> np.cross(x, y)
    array([12, -6, -3])

    Both vectors with dimension 2.

    >>> x = [1,2]
    >>> y = [4,5]
    >>> np.cross(x, y)
    -3

    Multiple vector cross-products. Note that the direction of the cross
    product vector is defined by the `right-hand rule`.

    >>> x = np.array([[1,2,3], [4,5,6]])
    >>> y = np.array([[4,5,6], [1,2,3]])
    >>> np.cross(x, y)
    array([[-3,  6, -3],
           [ 3, -6,  3]])

    The orientation of `c` can be changed using the `axisc` keyword.

    >>> np.cross(x, y, axisc=0)
    array([[-3,  3],
           [ 6, -6],
           [-3,  3]])

    Change the vector definition of `x` and `y` using `axisa` and `axisb`.

    >>> x = np.array([[1,2,3], [4,5,6], [7, 8, 9]])
    >>> y = np.array([[7, 8, 9], [4,5,6], [1,2,3]])
    >>> np.cross(x, y)
    array([[ -6,  12,  -6],
           [  0,   0,   0],
           [  6, -12,   6]])
    >>> np.cross(x, y, axisa=0, axisb=0)
    array([[-24,  48, -24],
           [-30,  60, -30],
           [-36,  72, -36]])

    """
    if axis is not None:
        axisa, axisb, axisc = (axis,) * 3
    a = asarray(a)
    b = asarray(b)
    # Move working axis to the end of the shape
    a = rollaxis(a, axisa, a.ndim)
    b = rollaxis(b, axisb, b.ndim)
    msg = ("incompatible dimensions for cross product\n"
           "(dimension must be 2 or 3)")
    if a.shape[-1] not in (2, 3) or b.shape[-1] not in (2, 3):
        raise ValueError(msg)

        # Create the output array
    shape = broadcast(a[..., 0], b[..., 0]).shape
    if a.shape[-1] == 3 or b.shape[-1] == 3:
        shape += (3,)
    dtype = promote_types(a.dtype, b.dtype)
    cp = empty(shape, dtype)

    # create local aliases for readability
    a0 = a[..., 0]
    a1 = a[..., 1]
    if a.shape[-1] == 3:
        a2 = a[..., 2]
    b0 = b[..., 0]
    b1 = b[..., 1]
    if b.shape[-1] == 3:
        b2 = b[..., 2]
    if cp.ndim != 0 and cp.shape[-1] == 3:
        cp0 = cp[..., 0]
        cp1 = cp[..., 1]
        cp2 = cp[..., 2]

    if a.shape[-1] == 2:
        if b.shape[-1] == 2:
            # a0 * b1 - a1 * b0
            multiply(a0, b1, out=cp)
            cp -= a1 * b0
            if cp.ndim == 0:
                return cp
            else:
                # This works because we are moving the last axis
                return rollaxis(cp, -1, axisc)
        else:
            # cp0 = a1 * b2 - 0  (a2 = 0)
            # cp1 = 0 - a0 * b2  (a2 = 0)
            # cp2 = a0 * b1 - a1 * b0
            multiply(a1, b2, out=cp0)
            multiply(a0, b2, out=cp1)
            negative(cp1, out=cp1)
            multiply(a0, b1, out=cp2)
            cp2 -= a1 * b0
    elif a.shape[-1] == 3:
        if b.shape[-1] == 3:
            # cp0 = a1 * b2 - a2 * b1
            # cp1 = a2 * b0 - a0 * b2
            # cp2 = a0 * b1 - a1 * b0
            multiply(a1, b2, out=cp0)
            tmp = array(a2 * b1)
            cp0 -= tmp
            multiply(a2, b0, out=cp1)
            multiply(a0, b2, out=tmp)
            cp1 -= tmp
            multiply(a0, b1, out=cp2)
            multiply(a1, b0, out=tmp)
            cp2 -= tmp
        else:
            # cp0 = 0 - a2 * b1  (b2 = 0)
            # cp1 = a2 * b0 - 0  (b2 = 0)
            # cp2 = a0 * b1 - a1 * b0
            multiply(a2, b1, out=cp0)
            negative(cp0, out=cp0)
            multiply(a2, b0, out=cp1)
            multiply(a0, b1, out=cp2)
            cp2 -= a1 * b0

    if cp.ndim == 1:
        return cp
    else:
        # This works because we are moving the last axis
        return rollaxis(cp, -1, axisc)

def dot(a, b, strict=False):
    """
    Return the dot product of two arrays.

    .. note::
      Works only with 2-D arrays at the moment.

    This function is the equivalent of `numpy.dot` that takes masked values
    into account, see `numpy.dot` for details.

    Parameters
    ----------
    a, b : ndarray
        Inputs arrays.
    strict : bool, optional
        Whether masked data are propagated (True) or set to 0 (False) for the
        computation. Default is False.
        Propagating the mask means that if a masked value appears in a row or
        column, the whole row or column is considered masked.

    See Also
    --------
    numpy.dot : Equivalent function for ndarrays.

    Examples
    --------
    >>> a = ma.array([[1, 2, 3], [4, 5, 6]], mask=[[1, 0, 0], [0, 0, 0]])
    >>> b = ma.array([[1, 2], [3, 4], [5, 6]], mask=[[1, 0], [0, 0], [0, 0]])
    >>> np.ma.dot(a, b)
    masked_array(data =
     [[21 26]
     [45 64]],
                 mask =
     [[False False]
     [False False]],
           fill_value = 999999)
    >>> np.ma.dot(a, b, strict=True)
    masked_array(data =
     [[-- --]
     [-- 64]],
                 mask =
     [[ True  True]
     [ True False]],
           fill_value = 999999)

    """
    #!!!: Works only with 2D arrays. There should be a way to get it to run with higher dimension
    if strict and (a.ndim == 2) and (b.ndim == 2):
        a = mask_rows(a)
        b = mask_cols(b)
    #
    d = np.dot(filled(a, 0), filled(b, 0))
    #
    am = (~getmaskarray(a))
    bm = (~getmaskarray(b))
    m = ~np.dot(am, bm)
    return masked_array(d, mask=m)
