from lazylinop import LazyLinOp, binary_dtype
import numpy as np


def zeros(shape, dtype=None):
    """
    Returns a zero :py:class:`LazyLinOp`.

    .. admonition:: Free memory cost
        :class: admonition note

        Whatever is the shape of the ``zeros``, it has no memory cost.

    Args:
        shape: (``tuple[int, int]``)
             The operator shape.

        dtype: (data-type str)
            numpy compliant data-type str (e.g. 'float64').

    Example:
        >>> from lazylinop import zeros
        >>> import numpy as np
        >>> Lz = zeros((10, 12))
        >>> x = np.random.rand(12)
        >>> Lz @ x
        array([0., 0., 0., 0., 0., 0., 0., 0., 0., 0.])

    .. seealso:: `numpy.zeros <https://numpy.org/doc/stable/reference/
        generated/numpy.zeros.html>`_.
    """
    if dtype is None:
        dtype = 'float'

    def _matmat(op, shape):
        nonlocal dtype
        dtype = binary_dtype(dtype, op.dtype)
        # shape[1] == op.shape[0] (because of LazyLinOp)
        # op.ndim > 2 can't happen because of LazyLinOp def
        # op a LazyLinOp can't happen either for the same reason
        if op.ndim == 2:
            return np.zeros((shape[0], op.shape[1]), dtype=dtype)
        else:  # op.ndim == 1: (see LazyLinOp.__matmul__)
            return np.zeros((shape[0],))
    return LazyLinOp(shape, matmat=lambda x:
                        _matmat(x, shape),
                        rmatmat=lambda x: _matmat(x, (shape[1],
                                                      shape[0])),
                        dtype=dtype)
