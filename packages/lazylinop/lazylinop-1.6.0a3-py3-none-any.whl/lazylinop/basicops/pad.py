import numpy as np
from lazylinop import LazyLinOp, aslazylinop
from lazylinop.basicops import hstack, vstack, eye, kron
from scipy.sparse import issparse
from warnings import warn


def pad(X, pad_width, constant_values=0):
    """
    Returns a :py:class:`LazyLinOp` of the padded ``X``.

    Args:
        X: (``scipy LinearOperator``, ``LazyLinOperator``, ``numpy array``)
            The operator/array/vector to pad.
        pad_width: (``tuple``, ``list``)
            Number (``int``) of values padded to the edges of each axis.

            - ``(B0, A0)`` if ``X`` is one-dimensional (B for before,
              A for after).
            - ``((B0, A0), (B1, A1))`` if ``X`` is two-dimensional.
            See Figure `Padding format`.
        constant_values: (``tuple``, ``list``, ``scalar``)
            ``((VB0, VA0)``, ``(VB1, VA1))``, or ``((VB0, VA0))`` or
            ``(V,)`` or ``V``: padding values before (``VBi``) and values after
            (``VAi``) on each dimension. In Figure `Padding format` value
            ``VBi`` (resp. ``VAi``) goes where padding width ``Bi`` (resp.
            ``Ai``) is.

            - If not enough values ``VBi = VAi``.
            - If values are missing for the second dimension, same values as
              for the first dimension are used.

    .. _padding_format
    Padding format (on a vector ``v`` and a matrix ``M``)
    --------------
        .. image:: _static/pad_width.svg

    Example:
        >>> from lazylinop import pad
        >>> from numpy import arange
        >>> A = arange(18*2).reshape((18, 2))
        >>> A
        array([[ 0,  1],
               [ 2,  3],
               [ 4,  5],
               [ 6,  7],
               [ 8,  9],
               [10, 11],
               [12, 13],
               [14, 15],
               [16, 17],
               [18, 19],
               [20, 21],
               [22, 23],
               [24, 25],
               [26, 27],
               [28, 29],
               [30, 31],
               [32, 33],
               [34, 35]])
        >>> lpA = pad(A, (2, 3))
        >>> lpA
        <23x2 LazyLinOp with dtype=int64>
        >>> lpA.toarray()
        array([[ 0,  0],
               [ 0,  0],
               [ 0,  1],
               [ 2,  3],
               [ 4,  5],
               [ 6,  7],
               [ 8,  9],
               [10, 11],
               [12, 13],
               [14, 15],
               [16, 17],
               [18, 19],
               [20, 21],
               [22, 23],
               [24, 25],
               [26, 27],
               [28, 29],
               [30, 31],
               [32, 33],
               [34, 35],
               [ 0,  0],
               [ 0,  0],
               [ 0,  0]])
        >>> lpA2 = pad(A, ((2, 3), (4, 1)))
        >>> lpA2
        <23x7 LazyLinOp with dtype=int64>
        >>> lpA2.toarray()
        array([[ 0,  0,  0,  0,  0,  0,  0],
               [ 0,  0,  0,  0,  0,  0,  0],
               [ 0,  0,  0,  0,  0,  1,  0],
               [ 0,  0,  0,  0,  2,  3,  0],
               [ 0,  0,  0,  0,  4,  5,  0],
               [ 0,  0,  0,  0,  6,  7,  0],
               [ 0,  0,  0,  0,  8,  9,  0],
               [ 0,  0,  0,  0, 10, 11,  0],
               [ 0,  0,  0,  0, 12, 13,  0],
               [ 0,  0,  0,  0, 14, 15,  0],
               [ 0,  0,  0,  0, 16, 17,  0],
               [ 0,  0,  0,  0, 18, 19,  0],
               [ 0,  0,  0,  0, 20, 21,  0],
               [ 0,  0,  0,  0, 22, 23,  0],
               [ 0,  0,  0,  0, 24, 25,  0],
               [ 0,  0,  0,  0, 26, 27,  0],
               [ 0,  0,  0,  0, 28, 29,  0],
               [ 0,  0,  0,  0, 30, 31,  0],
               [ 0,  0,  0,  0, 32, 33,  0],
               [ 0,  0,  0,  0, 34, 35,  0],
               [ 0,  0,  0,  0,  0,  0,  0],
               [ 0,  0,  0,  0,  0,  0,  0],
               [ 0,  0,  0,  0,  0,  0,  0]])
        >>> # padding a vector
        >>> x = np.full(3, 1)
        >>> lpx = pad(x, (2, 3))
        >>> lpx
        <8x1 LazyLinOp with dtype=int64>
        >>> lpx.toarray().ravel()
        array([0, 0, 1, 1, 1, 0, 0, 0])
        >>> lpx1 = pad(x, (2, 3), constant_values=(-1, 2))
        >>> lpx1.toarray().ravel()
        array([-1, -1,  1,  1,  1,  2,  2,  2])


        .. seealso::
            `numpy.pad <https://numpy.org/doc/stable/reference/generated/
            numpy.pad.html>`_
        """
    if (len(pad_width) == 2 and
        isinstance(pad_width[0], (tuple, list)) and
            isinstance(pad_width[1], (tuple, list))):
        op_shape = (X.shape[0] + np.sum(pad_width[0]), X.shape[1] +
                    np.sum(pad_width[1]))
    elif len(pad_width) == 2 and isinstance(pad_width, (tuple, list)):
        if X.ndim == 1:
            X = X.reshape(X.size, 1)
        if X.ndim == 2:
            op_shape = (X.shape[0] + np.sum(pad_width), X.shape[1])
            pad_width = (pad_width, (0, 0))
        else:
            raise ValueError("X must be 1d or 2d dimensional only")
    else:
        raise ValueError('pad_width is not valid; (before, after) or'
                         ' ((before1, after1), (before2, after2))')
    return LazyLinOp(op_shape,
                        matmat=lambda M: (ppadder(
                            X.shape,
                            pad_width,
                            constant_values=constant_values) @ X) @ M,
                        rmatmat=lambda M: X @ M, dtype=X.dtype)


def padder(X_shape, pad_width):
    """
    Returns a :py:class:`LazyLinOp` for row dimension zero padding of any X.

    The :py:class:`LazyLinOp` ``L`` returned is also able to unpad the
    padded result ``(L @ x)`` to get back the original ``x``.
    See unpadding examples below.

    Args:
        X:
            Operator to apply the padding to.
        pad_width: (tuple[int, int]/list[int, int])
            A pair of integers. pad_width[0] is the "before"
            padding size and pad_width[1] is the "after" padding size.

    Example:
        >>> from lazylinop import padder
        >>> from numpy import arange
        >>> A = arange(18*2).reshape((18, 2))
        >>> A
        array([[ 0,  1],
               [ 2,  3],
               [ 4,  5],
               [ 6,  7],
               [ 8,  9],
               [10, 11],
               [12, 13],
               [14, 15],
               [16, 17],
               [18, 19],
               [20, 21],
               [22, 23],
               [24, 25],
               [26, 27],
               [28, 29],
               [30, 31],
               [32, 33],
               [34, 35]])
        >>> lz = padder(A.shape, (2, 3))
        >>> lz
        <46x36 LazyLinOp with unspecified dtype>
        >>> lz @ A
        array([[ 0,  0],
               [ 0,  0],
               [ 0,  1],
               [ 2,  3],
               [ 4,  5],
               [ 6,  7],
               [ 8,  9],
               [10, 11],
               [12, 13],
               [14, 15],
               [16, 17],
               [18, 19],
               [20, 21],
               [22, 23],
               [24, 25],
               [26, 27],
               [28, 29],
               [30, 31],
               [32, 33],
               [34, 35],
               [ 0,  0],
               [ 0,  0],
               [ 0,  0]])
        >>> # padding for a vector
        >>> x = np.full(3, 1.)
        >>> lz2 = padder(x.shape, (2, 3))
        >>> lz2 @ x
        array([0., 0., 1., 1., 1., 0., 0., 0.])

        Unpadding:

        >>> paddedA = (lz @ A).ravel()
        >>> np.allclose(lz.H @ paddedA, A.ravel())
        True
        >>> np.allclose((lz.H @ paddedA).reshape(A.shape), A)
        True

        >>> lz2.H @ (lz2 @ x)
        array([1., 1., 1.])
    """
    return ppadder(X_shape, (pad_width, (0, 0))
                   if len(X_shape) == 2 else pad_width)


def ppadder(x_shape, pad_width, constant_values=0, **kwargs):
    """
    Returns a :py:class:`LazyLinOp` for zero padding of any X.

    .. warning:: this is a permissive padder that allows to break the properly
    defined matrix product because it can pad such that the number of columns
    of input is not the same as output.
    It permits also to pad with nonzero constant values.
    Rather use :py:func:`pad` or :py:func:`padder` for a strict LazyLinOp.

    Note: the LazyLinOp L returned is able to unpad the padded result
    (L @ x) to get back the original x. See unpadding examples below.

    Args:
        x_shape:
             shape of x to apply the padding to.
        pad_width:
             a tuple/list of tuples/pairs of integers. It can be one tuple only
             if x is one-dimensional or a tuple of two tuples if x
             two-dimensional.
        constant_values: one or two tuples of two scalars or scalar.
            ((before0, after0), (before1, after1)), or ((before0, after0)) or
            (constant,) or constant: values for padding before and after on
            each dimension. If not enough values before = after and in case of
            a missing value for a dimension then the same values are used for
            the two dimensions.

    Example:
        >>> from lazylinop import pad
        >>> from numpy import arange
        >>> A = arange(18*2).reshape((18, 2))
        >>> A
        array([[ 0,  1],
               [ 2,  3],
               [ 4,  5],
               [ 6,  7],
               [ 8,  9],
               [10, 11],
               [12, 13],
               [14, 15],
               [16, 17],
               [18, 19],
               [20, 21],
               [22, 23],
               [24, 25],
               [26, 27],
               [28, 29],
               [30, 31],
               [32, 33],
               [34, 35]])
        >>> lz = ppadder(A.shape, ((2, 3), (4, 1)))
        >>> lz
        <161x36 LazyLinOp with unspecified dtype>
        >>> np.round(lz @ A, decimals=2).astype('double')
        array([[ 0.,  0.,  0.,  0.,  0.,  0.,  0.],
               [ 0.,  0.,  0.,  0.,  0.,  0.,  0.],
               [ 0.,  0.,  0.,  0.,  0.,  1.,  0.],
               [ 0.,  0.,  0.,  0.,  2.,  3.,  0.],
               [ 0.,  0.,  0.,  0.,  4.,  5.,  0.],
               [ 0.,  0.,  0.,  0.,  6.,  7.,  0.],
               [ 0.,  0.,  0.,  0.,  8.,  9.,  0.],
               [ 0.,  0.,  0.,  0., 10., 11.,  0.],
               [ 0.,  0.,  0.,  0., 12., 13.,  0.],
               [ 0.,  0.,  0.,  0., 14., 15.,  0.],
               [ 0.,  0.,  0.,  0., 16., 17.,  0.],
               [ 0.,  0.,  0.,  0., 18., 19.,  0.],
               [ 0.,  0.,  0.,  0., 20., 21.,  0.],
               [ 0.,  0.,  0.,  0., 22., 23.,  0.],
               [ 0.,  0.,  0.,  0., 24., 25.,  0.],
               [ 0.,  0.,  0.,  0., 26., 27.,  0.],
               [ 0.,  0.,  0.,  0., 28., 29.,  0.],
               [ 0.,  0.,  0.,  0., 30., 31.,  0.],
               [ 0.,  0.,  0.,  0., 32., 33.,  0.],
               [ 0.,  0.,  0.,  0., 34., 35.,  0.],
               [ 0.,  0.,  0.,  0.,  0.,  0.,  0.],
               [ 0.,  0.,  0.,  0.,  0.,  0.,  0.],
               [ 0.,  0.,  0.,  0.,  0.,  0.,  0.]])
        >>> # padding for a vector
        >>> x = np.full(3, 1)
        >>> lz2 = ppadder(x.shape, ((2, 3)))
        >>> lz2 @ x
        array([0, 0, 1, 1, 1, 0, 0, 0])

    Padding A with arbitrary constant values:
        >>> x = np.full(3, 1)
        >>> lcv = ppadder(x.shape, ((2, 3)), constant_values=(2, 5))
        >>> lcv @ x
        array([2, 2, 1, 1, 1, 5, 5, 5])
        >>> cv = ((2, 5), (3, 6))
        >>> pw = ((2, 3), (4, 1))
        >>> lz3 = ppadder(A.shape, pw, constant_values=cv)
        >>> lz3 @ A
        array([[ 3,  3,  3,  3,  2,  2,  6],
               [ 3,  3,  3,  3,  2,  2,  6],
               [ 3,  3,  3,  3,  0,  1,  6],
               [ 3,  3,  3,  3,  2,  3,  6],
               [ 3,  3,  3,  3,  4,  5,  6],
               [ 3,  3,  3,  3,  6,  7,  6],
               [ 3,  3,  3,  3,  8,  9,  6],
               [ 3,  3,  3,  3, 10, 11,  6],
               [ 3,  3,  3,  3, 12, 13,  6],
               [ 3,  3,  3,  3, 14, 15,  6],
               [ 3,  3,  3,  3, 16, 17,  6],
               [ 3,  3,  3,  3, 18, 19,  6],
               [ 3,  3,  3,  3, 20, 21,  6],
               [ 3,  3,  3,  3, 22, 23,  6],
               [ 3,  3,  3,  3, 24, 25,  6],
               [ 3,  3,  3,  3, 26, 27,  6],
               [ 3,  3,  3,  3, 28, 29,  6],
               [ 3,  3,  3,  3, 30, 31,  6],
               [ 3,  3,  3,  3, 32, 33,  6],
               [ 3,  3,  3,  3, 34, 35,  6],
               [ 3,  3,  3,  3,  5,  5,  6],
               [ 3,  3,  3,  3,  5,  5,  6],
               [ 3,  3,  3,  3,  5,  5,  6]])
        >>> np.allclose(lz3 @ A, np.pad(A, pw, constant_values=cv))
        True

    Unpadding a padded vector:
        >>> lz2.H @ (lz2 @ x)
        array([1, 1, 1])
        >>> lcv.H @ (lcv @ x)
        array([1, 1, 1])
        >>> # in both cases we retrieved the original x

    Unpadding a padded 2d-array:
        >>> (lz3.H @ (lz3 @ A).ravel()).reshape(A.shape)
        array([[ 0,  1],
               [ 2,  3],
               [ 4,  5],
               [ 6,  7],
               [ 8,  9],
               [10, 11],
               [12, 13],
               [14, 15],
               [16, 17],
               [18, 19],
               [20, 21],
               [22, 23],
               [24, 25],
               [26, 27],
               [28, 29],
               [30, 31],
               [32, 33],
               [34, 35]])
        >>> # original A is retrieved

    See also `numpy.pad <https://numpy.org/doc/stable/reference/generated/
    numpy.pad.html>`_
    """
    pad_width = np.array(pad_width).astype('int')
    if pad_width.shape[0] > 2 or pad_width.ndim > 1 and pad_width.shape[1] > 2:
        raise ValueError('Cannot pad zeros on more than two dimensions')
    if len(x_shape) != pad_width.ndim:
        raise ValueError('pad_width number of tuples must be len(x_shape).')
    if pad_width.ndim == 1:
        pad_width_ndim_was_1 = True
        pad_width = np.vstack((pad_width, (0, 0)))
    else:
        pad_width_ndim_was_1 = False
    constant_values = _sanitize_contant_values(constant_values)
    kron_handled_cv = [((0, 0), (0, 0))]
    x_size = np.prod(x_shape)
    x_is_vec = x_size == x_shape[0] or x_size == x_shape[1]
    if 'impl' not in kwargs or kwargs['impl'] != 'nokron':
        if ('impl' in kwargs and 'kron' == kwargs['impl'] or
            'impl' not in kwargs and
                x_is_vec and constant_values in kron_handled_cv):
            if constant_values not in kron_handled_cv:
                raise ValueError('kron impl can only be used in case of'
                                 ' zero-padding but constant_values are not 0')
            if x_is_vec == 1:
                pad_width = tuple(pad_width[0])
            return kron_pad((x_size,), pad_width)
    lop_shape = (np.prod(np.sum(pad_width if len(x_shape) == 2 else
                                pad_width[0], axis=0 if len(x_shape) == 1 else
                                1) +
                         x_shape),
                 np.prod(x_shape))

    def mul(op):
        op_reshaped = False
        if op.ndim == 1:
            # op can't be a LazyLinOp
            if pad_width_ndim_was_1:
                return np.pad(op, pad_width[0], mode="constant",
                              constant_values=constant_values[0])
            else:
                op = op.reshape(x_shape)
                op_reshaped = True
        elif x_shape == op.shape and isinstance(op, np.ndarray):
            if (constant_values == ((0, 0), (0, 0)) and
                    all(pad_width[0] == (0, 0))):
                # particular case opt. (zero padding of columns)
                out = np.zeros((x_shape[0], x_shape[1] + np.sum(pad_width[1])))
                out[:, pad_width[1][0]:pad_width[1][0]+op.shape[1]] = op
                return out
            else:
                return np.pad(op, pad_width, mode='constant',
                              constant_values=constant_values)
        elif x_shape != op.shape:
            out = aslazylinop(np.empty((lop_shape[0], 0)))
            for j in range(op.shape[1]):
                out_v = mul(op[:, j])
                if out_v.ndim == 1:
                    out_v = out_v.reshape((out_v.size, 1))
                out = hstack((out, out_v))
            if isinstance(op, np.ndarray) or issparse(op):
                return out.toarray()
            else:
                return out
        out = aslazylinop(op)
        for i in range(pad_width.shape[0]):
            bw = pad_width[i][0]
            aw = pad_width[i][1]
            bv = constant_values[i][0]
            av = constant_values[i][0]
            if bw > 0:
                if i == 0:
                    out = vstack((_pad_block((bw, out.shape[1]), bv,
                                             dtype=op.dtype), out))
                else:  # i == 1:
                    out = hstack((_pad_block((out.shape[0], bw), bv,
                                             dtype=op.dtype), out))
            if aw > 0:
                if i == 0:
                    out = vstack((out, _pad_block((aw, out.shape[1]), av,
                                                  dtype=op.dtype)))
                else:  # i == 1:
                    out = hstack((out, _pad_block((out.shape[0], aw), av,
                                                  dtype=op.dtype)))
        if isinstance(op, np.ndarray) or issparse(op):
            if op_reshaped:
                return out.toarray().ravel()
            else:
                return out.toarray()
        else:
            return out

    def rmul(op):
        op_reshaped = False
        op_std_2d_shape = tuple(np.sum(pad_width, axis=len(pad_width) - 1) +
                                x_shape)
        if op.ndim == 1:
            if pad_width_ndim_was_1:
                # op can't be a LazyLinOp
                return op[pad_width[0, 0]: pad_width[0, 0] + x_shape[0]]
            else:
                op = op.reshape(op_std_2d_shape)
                op_reshaped = True
        elif op_std_2d_shape != op.shape:
            out = aslazylinop(np.empty((lop_shape[1], 0)))
            for j in range(op.shape[1]):
                out_v = rmul(op[:, j])
                if out_v.ndim == 1:
                    out_v = out_v.reshape((out_v.size, 1))
                out = hstack((out, out_v))
            if isinstance(op, np.ndarray) or issparse(op):
                return out.toarray()
            else:
                return out
        r_offset = pad_width[0][0]
        c_offset = pad_width[1][0]
        out = op[r_offset:r_offset + x_shape[0],
                 c_offset:c_offset + x_shape[1]]
        if op_reshaped:
            return out.ravel()
        else:
            return out
    ret = LazyLinOp(lop_shape, matmat=lambda op: mul(op), rmatmat=lambda
                       op: rmul(op))
    ret.ravel_op = True  # a 2d array can be flatten to be compatible
    # to zpad.shape[1]
    return ret


def zpad(x_shape, pad_width):
    """
    Deprecated alias for :py:func:`pad` with zero as constant value to pad.
    This function might be removed in a next version.
    """
    warn("Don't use [DEPRECATED] zpad, use pad with default constant_values"
         " (zeros)")
    return ppadder(x_shape, pad_width, constant_values=0)


def _sanitize_contant_values(constant_values):
    # TODO: check all cases and remove possible unecessary code
    if np.isscalar(constant_values):
        constant_values = [constant_values, ]
    if isinstance(constant_values, (tuple, np.ndarray)):
        constant_values = list(constant_values)
    if not isinstance(constant_values, list):
        raise TypeError('Invalid constant_values')
    if len(constant_values) == 1:
        constant_values = [constant_values, constant_values]
    if np.isscalar(constant_values[0]) and np.isscalar(constant_values[1]):
        constant_values = [constant_values, constant_values]
    for i in range(2):
        if np.isscalar(constant_values[i]):
            constant_values[i] = [constant_values[i],
                                  constant_values[i]]
        lc = len(constant_values[i])
        if lc == 1:
            constant_values[i] = [constant_values[i][0],
                                  constant_values[i][0]]
        elif lc != 2:
            raise ValueError('constant_values contain sequence of invalid size'
                             ' (valid sizes are 1 or 2)')
        for j in range(2):
            if not np.isscalar(constant_values[i][j]):
                raise ValueError('constant_values contains something that is'
                                 ' not a scalar')
        # convert to tuple
        constant_values[i] = tuple(constant_values[i])
    return tuple(constant_values)


sanitize_const_values = _sanitize_contant_values


def _pad_block(shape, v=0, dtype=None):
    from lazylinop.basicops import zeros, ones
    if v == 0:
        return zeros(shape, dtype=dtype)
    else:
        return ones(shape, dtype=dtype) * v


def kron_pad(shape: tuple, pad_width: tuple):
    """Constructs a lazy linear operator Op for padding.

    If shape is a tuple (X, Y), Op is applied to a 1d array of shape (X * Y, ).
    The output of the padding of the 2d input array is given by
    Op @ input.flatten(order='C').
    You should use output.reshape(X, Y) to get a 2d output array.
    The function uses Kronecker trick vec(M @ X @ N) = kron(M.T, N) @ vec(X)
    to pad both rows and columns.

    Args:
        shape: tuple
            Shape of the input
        pad_width: tuple
            It can be (A, B):
            Add A zero columns and rows before and B zero columns and
            rows after.
            or ((A, B), (C, D)):
            Add A zero rows before and B zero rows after.
            Add C zero columns to the left and D zero columns to the right.
        dtype: str or None
            numpy compliant dtype str (defaultly None).

    Returns:
        LazyLinOp

    Raises:
        ValueError
            pad_width expects (A, B) or ((A, B), (C, D)).
        ValueError
            pad_width expects positive values.
        ValueError
            If len(shape) is 1, pad_width expects a tuple (A, B).

    Examples:
        >>> from lazylinop.basicops.pad import kron_pad
        >>> x = np.arange(1, 4 + 1, 1).reshape(2, 2)
        >>> x
        array([[1, 2],
               [3, 4]])
        >>> y = kron_pad(x.shape, (1, 2)) @ x.flatten()
        >>> y.reshape(5, 5)
        array([[0, 0, 0, 0, 0],
               [0, 1, 2, 0, 0],
               [0, 3, 4, 0, 0],
               [0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0]])
        >>> x = np.arange(1, 6 + 1, 1).reshape(2, 3)
        >>> x
        array([[1, 2, 3],
               [4, 5, 6]])
        >>> y = kron_pad(x.shape, ((2, 1), (2, 3))) @ x.flatten()
        >>> y.reshape(5, 8)
        array([[0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 1, 2, 3, 0, 0, 0],
               [0, 0, 4, 5, 6, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0]])

    References:
        See also `numpy.pad <https://numpy.org/doc/stable/reference/generated/
        numpy.pad.html>`_
    """
    dtype = 'int'
    W = len(pad_width)
    if W != 2:
        raise ValueError("pad_width expects (A, B) or ((A, B), (C, D)).")
    if len(shape) == 1:
        if type(pad_width) is not tuple:
            raise ValueError("If len(shape) is 1, pad_width expects"
                             " a tuple (A, B).")
        if pad_width[0] < 0 or pad_width[1] < 0:
            raise ValueError("pad_width expects positive values.")
        Op = eye(shape[0] + pad_width[0] + pad_width[1], n=shape[0],
                 k=-pad_width[0], dtype=dtype)
        return Op
    elif len(shape) == 2:
        if type(pad_width[0]) is tuple:
            # pad_witdh is ((A, B), (C, D))
            for w in range(W):
                if pad_width[w][0] < 0 or pad_width[w][1] < 0:
                    raise ValueError("pad_width expects positive values.")
                Ww = len(pad_width[w])
                if Ww != 2:
                    raise ValueError("pad_width expects (A, B) or"
                                     " ((A, B), (C, D)).")
                if w == 0:
                    M = eye(shape[0] + pad_width[w][0] + pad_width[w][1],
                            n=shape[0], k=-pad_width[w][0], dtype='int')
                elif w == 1:
                    NT = eye(shape[1] + pad_width[w][0] + pad_width[w][1],
                             n=shape[1], k=-pad_width[w][0], dtype='int')
            Op = kron(M, NT)
            return Op
        else:
            if pad_width[0] < 0 or pad_width[1] < 0:
                raise ValueError("pad_width expects positive values.")
            # pad_witdh is (A, B), pad each dimension
            M = eye(shape[0] + pad_width[0] + pad_width[1], n=shape[0],
                    k=-pad_width[0], dtype=dtype)
            NT = eye(shape[1] + pad_width[0] + pad_width[1], n=shape[1],
                     k=-pad_width[0], dtype=dtype)
            Op = kron(M, NT)
            return Op
    else:
        pass


def mpad2(L: int, X: int, n: int = 1):
    """Return a :py:class:`LazyLinOp` to zero-pad each block of a signal.

    If you apply this operator to a vector of length L * X the output will
    have a length (L + n) * X.

    Args:
        L: int
            Block size
        X: int
            Number of blocks.
        n: int, optional
            Add n zeros to each block.

    Returns:
        LazyLinOp

    Raises:
        ValueError
            Invalid block size and/or number of blocks.

    Examples:
        >>> from lazylinop.wip.signal import mpad
        >>> import numpy as np
        >>> signal = np.full(5, 1.0)
        >>> signal
        array([1., 1., 1., 1., 1.])
        >>> y = mpad(1, 5, 1) @ signal
        >>> y
        array([1., 0., 1., 0., 1., 0., 1., 0., 1., 0.])
    """
    from lazylinop import eye
    if n <= 0:
        # reproducing mpad behaviour
        # (but is that really necessary? why a negative padding size?)
        return eye(X * L, n=X * L, k=0)
    P = ppadder((X, L), ((0, 0), (0, n)), impl='nokron')
    invalid_ndim_e = ValueError("Invalid number of dimensions (must be <= 2)")

    def matmat(x):
        nonlocal P
        ndim = len(x.shape)  # do not use x.ndim in case it is not defined
        if ndim == 1 or x.shape[1] == 1:
            px = P @ x.reshape((X, L))
            return px.ravel() if ndim == 1 else px.reshape(-1,
                                                           1)
        elif ndim == 2:
            xncols = x.shape[1]
            ncols = L * xncols
            mP = ppadder((X, L * x.shape[1]), ((0, 0), (0, n * xncols)),
                         impl='nokron')
            return (mP @ x.reshape(X, ncols)).reshape(-1, xncols)
        else:
            raise invalid_ndim_e

    def rmatmat(x):
        nonlocal P
        ndim = len(x.shape)  # do not use x.ndim in case it is not defined
        if ndim == 1:
            return P.H @ x
        elif ndim == 2:
            xncols = x.shape[1]
            mP = ppadder((X, L * x.shape[1]), ((0, 0), (0, n * xncols)),
                         impl='nokron')
            return (mP.H @ x.ravel()).reshape(-1, x.shape[1])
        else:
            raise invalid_ndim_e
    return LazyLinOp(
        shape=(X * (L + n), X * L),
        # it works the same with matvec and rmatvec but it would be slower for
        # x a matrix (LazyLinOp loops on matvec to compute LazyLinOp @ M)
        #        matvec=lambda x: (P @ x.reshape((X, L))).ravel(),
        #        rmatvec=lambda x: (P.H @ x.ravel())
        matmat=matmat,
        rmatmat=rmatmat
    )


def mpad(L: int, X: int, n: int = 1):
    """Returns a :py:class:`LazyLinOp` to zero-pad each signal block.

    If you apply this operator to a vector of length L * X the output will have
    a length (L + n) * X.

    Args:
        L: int
            Block size
        X: int
            Number of blocks.
        n: int, optional
            Add n zeros to each block.

    Returns:
        LazyLinOp

    Raises:
        ValueError
            Invalid block size and/or number of blocks.

    Examples:
        >>> from lazylinop.wip.signal import mpad
        >>> import numpy as np
        >>> signal = np.full(5, 1.0)
        >>> signal
        array([1., 1., 1., 1., 1.])
        >>> y = mpad(1, 5, 1) @ signal
        >>> y
        array([1., 0., 1., 0., 1., 0., 1., 0., 1., 0.])
    """
    from warnings import warn
    warn("This function is deprecated and should not be used anymore, use"
         " mpad2 -- see issue #57. It will be deleted in a next version.")
    if n <= 0:
        return eye(X * L, n=X * L, k=0)

    def _matmat(x):
        if (X * L) != x.shape[0]:
            raise ValueError("Invalid block size and/or number of blocks.")
        if x.ndim == 1:
            is_1d = True
            x = x.reshape(x.shape[0], 1)
        else:
            is_1d = False
        # add n zeros to each block
        y = np.zeros((X * (L + n), x.shape[1]), dtype=x.dtype)
        for i in range(X):
            y[(i * (L + n)):(i * (L + n) + L), :] = x[(i * L):((i + 1) * L), :]
        return y.ravel() if is_1d else y

    def _rmatmat(x):
        if x.ndim == 1:
            is_1d = True
            x = x.reshape(x.shape[0], 1)
        else:
            is_1d = False
        # keep L elements every n + 1 elements
        y = np.zeros((X * L, x.shape[1]), dtype=x.dtype)
        for i in range(X):
            y[(i * L):((i + 1) * L), :] = x[(i * (L + n)):(i * (L + n) + L), :]
        return y.ravel() if is_1d else y
    return LazyLinOp(
        shape=(X * (L + n), X * L),
        matmat=lambda x: _matmat(x),
        rmatmat=lambda x: _rmatmat(x)
    )
