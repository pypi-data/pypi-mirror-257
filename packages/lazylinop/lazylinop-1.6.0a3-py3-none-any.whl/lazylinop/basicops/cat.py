from lazylinop import islazylinop, aslazylinop


def hstack(ops):
    """
    Concatenates linear operators horizontally.

    Args:
        ops: (``tuple`` of compatible linear operators)
            For any pair ``i, j < len(ops)``, ``ops[i].shape[0] ==
            ops[i].shape[0]``.

    Returns:
        A concatenation :class:`LazyLinOp`.

    Example:
        >>> from lazylinop import hstack, ones, islazylinop
        >>> import numpy as np
        >>> A = np.ones((10, 10))
        >>> B = ones((10, 2))
        >>> lcat = hstack((A, B))
        >>> islazylinop(lcat)
        True
        >>> np.allclose(lcat.toarray(), np.hstack((A, B.toarray())))
        True

    .. seealso::

        :func:`vstack`
        `numpy.hstack
        <https://numpy.org/doc/stable/reference/generated/numpy.hstack.html>`_
    """
    lop = ops[0]
    if not islazylinop(lop):
        lop = aslazylinop(ops[0])
    return lop.concatenate(*ops[1:], axis=1)


def vstack(ops):
    """
    Concatenates linear operators horizontally.

    Args:
        ops: (``tuple`` of compatible linear operators)
            For any pair ``i, j < len(ops)``, ``ops[i].shape[1] ==
            ops[i].shape[1]``.

    Returns:
        A concatenation :class:`LazyLinOp`.

    Example:
        >>> from lazylinop import vstack, ones, islazylinop
        >>> import numpy as np
        >>> A = np.ones((10, 10))
        >>> B = ones((2, 10))
        >>> lcat = vstack((A, B))
        >>> islazylinop(lcat)
        True
        >>> np.allclose(lcat.toarray(), np.vstack((A, B.toarray())))
        True

    .. seealso::
        :func:`hstack`
        `numpy.hstack
        <https://numpy.org/doc/stable/reference/generated/numpy.hstack.html>`_

    """
    lop = ops[0]
    if not islazylinop(lop):
        lop = aslazylinop(ops[0])
    return lop.concatenate(*ops[1:], axis=0)
