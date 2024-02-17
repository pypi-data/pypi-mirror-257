from lazylinop import LazyLinOp
import numpy as np


def diag(v, k=0):
    """
    Extracts a diagonal or constructs a diagonal :py:class:`LazyLinOp`.

    Args:
        v: (linear operator or a vector numpy array)
            - If ``v`` is a :py:class:`LazyLinOp` or any object with a
              :py:func:`toarray` function, returns a copy of its k-th diagonal.
            - If ``v`` is a 1D numpy array, returns a :py:class:`LazyLinOp` with
              ``v`` on the k-th diagonal.
        k: (``int``)
             the index of diagonal, 0 for the main diagonal,
             ``k > 0`` for diagonals above,
             ``k < 0`` for diagonals below (see :py:func:`eye`).

    Returns:
        The extracted diagonal numpy vector or
        the constructed diagonal :py:class:`LazyLinOp`.

    Example: (diagonal :py:class:`LazyLinOp`)
        >>> from lazylinop import diag
        >>> import numpy as np
        >>> v = np.arange(1, 6)
        >>> v
        array([1, 2, 3, 4, 5])
        >>> ld1 = diag(v)
        >>> ld1
        <5x5 LazyLinOp with dtype=int64>
        >>> ld1.toarray()
        array([[1, 0, 0, 0, 0],
               [0, 2, 0, 0, 0],
               [0, 0, 3, 0, 0],
               [0, 0, 0, 4, 0],
               [0, 0, 0, 0, 5]])
        >>> ld2 = diag(v, -2)
        >>> ld2
        <7x7 LazyLinOp with dtype=int64>
        >>> ld2.toarray()
        array([[0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0],
               [1, 0, 0, 0, 0, 0, 0],
               [0, 2, 0, 0, 0, 0, 0],
               [0, 0, 3, 0, 0, 0, 0],
               [0, 0, 0, 4, 0, 0, 0],
               [0, 0, 0, 0, 5, 0, 0]])
        >>> ld3 = diag(v, 2)
        >>> ld3
        <7x7 LazyLinOp with dtype=int64>
        >>> ld3.toarray()
        array([[0, 0, 1, 0, 0, 0, 0],
               [0, 0, 0, 2, 0, 0, 0],
               [0, 0, 0, 0, 3, 0, 0],
               [0, 0, 0, 0, 0, 4, 0],
               [0, 0, 0, 0, 0, 0, 5],
               [0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0]])

    Example: (diagonal extraction)
        >>> from lazylinop import diag, aslazylinop
        >>> import numpy as np
        >>> lD = aslazylinop(np.random.rand(10, 12))
        >>> d = diag(lD, -2)
        >>> # verify d is really the diagonal of index -2
        >>> d_ = np.array([lD[i, i-2] for i in range(abs(-2), lD.shape[0])])
        >>> np.allclose(d, d_)
        True


    .. seealso::
        `numpy.diag
        <https://numpy.org/doc/stable/reference/generated/numpy.diag.html>`_
    """
    te = TypeError("v must be a 1-dim vector (np.ndarray) or a 2d "
                   "array/LinearOperator.")
    if isinstance(v, np.ndarray) and v.ndim == 1:
        m = v.size + abs(k)

        def matmat(x, v, k):
            v = v.reshape(v.size, 1)
            if len(x.shape) == 1:
                x_is_1d = True
                x = x.reshape(x.size, 1)
            else:
                x_is_1d = False
            if k > 0:
                y = v * x[k:k+v.size]
                y = np.vstack((y, np.zeros((k, x.shape[1]), dtype=v.dtype)))
            elif k < 0:
                y = v * x[:v.size]
                y = np.vstack((np.zeros((abs(k), x.shape[1]), dtype=v.dtype),
                               y))
            else:  # k == 0
                y = v * x[:v.size]
            if x_is_1d:
                y = y.ravel()
            return y
        return LazyLinOp((m, m), matmat=lambda x: matmat(x, v, k),
                            rmatmat=lambda x: matmat(x, np.conj(v), -k),
                            dtype=v.dtype)
    elif v.ndim == 2:
        if isinstance(v, np.ndarray):
            return np.diag(v, k=k)
        elif hasattr(v, "toarray"):
            return np.diag(v.toarray(), k)
        else:
            raise te
    else:  # v is 1-dim but not a numpy array
        raise te
