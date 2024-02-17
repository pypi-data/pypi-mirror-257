"""
This module defines the general lazy linear operator and basic specializations.
It provides also utility functions.
"""

import numpy as np
from scipy.sparse.linalg import LinearOperator
HANDLED_FUNCTIONS = {'ndim'}


class LazyLinOp(LinearOperator):
    """
    The ``LazyLinOp`` class is a specialization of a
    `scipy.linalg.LinearOperator <https://docs.scipy.org/
    doc/scipy/reference/generated/scipy.sparse.linalg.LinearOperator.html>`_.

    .. admonition:: The lazy principle
        :class: admonition note

        The evaluation of any defined operation on a ``LazyLinOp`` is
        delayed until a multiplication by a matrix/vector or a call of
        :py:func:`LazyLinOp.toarray` is made.


    .. admonition:: Two ways to instantiate
        :class: admonition note

        - Using :py:func:`lazylinop.aslazylinop` or
        - Using this constructor (:py:func:`lazylinop.LazyLinOp`) to define
          ``matmat``, ``matvec`` functions.

    .. admonition:: Available operations
        :class: admonition note

        ``+`` (addition), ``-`` (subtraction),
        ``@`` (matrix product), ``*`` (scalar multiplication),
        ``**`` (matrix power for square operators),
        indexing, slicing and others.
        For a nicer introduction you might look at `these tutorials
        <https://faustgrp.gitlabpages.inria.fr/lazylinop/tutorials.html>`_.

    .. admonition:: Recursion limit
        :class: admonition warning

        Repeated "inplace" modifications of a :py:class:`LazyLinOp`
        through any operation like a concatenation
        (``op = vstack((op, anything))``)
        are subject to a :py:class:`RecursionError` if the number of recursive
        calls exceeds :py:func:`sys.getrecursionlimit`. You might change this
        limit if needed using :py:func:`sys.setrecursionlimit`.
    """

    def __init__(self, shape, matvec=None, matmat=None, rmatvec=None,
                 rmatmat=None, dtype=None, **kwargs):
        """
        A ``LazyLinOp`` instance is defined by a shape and at least
        a function ``matvec`` or ``matmat``.
        Additionally the functions ``rmatvec`` and ``rmatmat`` can be
        defined through the following parameters.


        Parameters
        ----------
            shape: (``tuple[int, int]``)
                 Operator $L$ dimensions $(M, N)$.
            matvec: (callable)
                 Returns $y = L * v$ with $v$ a vector of size $N$.
                 $y$ size is $M$ with the same number of dimension(s) as $v$.
            rmatvec: (callable)
                 Returns $y = L^H * v$ with $v$ a vector of size $M$.
                 $y$ size is $N$ with the same number of dimension(s) as $v$.
            matmat: (callable)
                 Returns $L * V$.
                 The output matrix shape is $(M, K)$.
            rmatmat: (``callable``)
                 Returns $L^H * V$.
                 The output matrix shape is $(N, K)$.
            dtype: (numpy ``dtype`` or ``NoneType``)
                 Data type of the ``LazyLinOp`` (default is ``None``).

        .. admonition:: Auto-implemented operations
            :class: admonition note

            - If only ``matvec`` is defined and not ``matmat``, an
              automatic naive ``matmat`` will be defined upon the given
              ``matvec`` but note that it might be suboptimal (in which
              case a ``matmat`` is useful).
            - No need to handle the multiplication by a :class:`LazyLinOp`
              or a numpy array of ``ndim > 2`` because both of them are
              auto-implemented. For the latter operation, it is computed as in
              `numpy.__matmul__ <https://numpy.org/doc/stable/reference/
              generated/numpy.matmul.html>`_.


        Return:
            ``LazyLinOp``

        Example:
            >>> # In this example we create a LazyLinOp
            >>> # for the DFT using the fft from scipy
            >>> import numpy as np
            >>> from scipy.fft import fft, ifft
            >>> from lazylinop import LazyLinOp
            >>> fft_mm = lambda x: fft(x, norm='ortho')
            >>> fft_rmm = lambda x: ifft(x, norm='ortho')
            >>> n = 16
            >>> F = LazyLinOp((n, n), matmat=fft_mm, rmatmat=fft_rmm)
            >>> x = np.random.rand(n)
            >>> y = F * x
            >>> np.allclose(y, fft(x, norm='ortho'))
            True
            >>> np.allclose(x, F.H * y)
            True

        .. seealso::
            `SciPy linear Operator
            <https://docs.scipy.org/doc/scipy/reference/generated/
            scipy.sparse.linalg.LinearOperator.html>`_.
            :py:func:`.check_op`
            `scipy fft
            <https://docs.scipy.org/doc/scipy/reference/generated/
            scipy.fft.fft.html>`_
        """
        if 'internal_call' in kwargs and kwargs['internal_call']:
            self.shape = shape
            self.dtype = dtype
            super(LazyLinOp, self).__init__(self.dtype, self.shape)
            return

        def check_matfunc(f, fn):
            if f is not None and not callable(f):
                raise TypeError(f+' must be a callable/function')

        for fn in ['matvec', 'rmatvec', 'matmat', 'rmatmat']:
            f = eval(fn)
            check_matfunc(f, fn)

        if matvec is None and matmat is None:
            raise ValueError('At least a matvec or a matmat function must be'
                             ' passed to the constructor.')

        def _matmat(M, _matvec, shape):
            nonlocal dtype
            if len(M.shape) == 1:
                return _matvec(M)
            first_col = _matvec(M[:, 0])
            dtype = first_col.dtype
            out = np.empty((shape[0], M.shape[1]), dtype=dtype)
            out[:, 0] = first_col
            for i in range(1, M.shape[1]):
                out[:, i] = _matvec(M[:, i])
            return out

        if matmat is None:
            def matmat(M): return _matmat(M, matvec, shape)

        if rmatmat is None and rmatvec is not None:
            def rmatmat(M): return _matmat(M, rmatvec, (shape[1], shape[0]))

        # MX = lambda X: matmat(np.eye(shape[1])) @ X
        def MX(X): return matmat(X)
        # MTX = lambda X: rmatmat(X.T).T
        def MHX(X): return rmatmat(X)

        def MTX(X):
            # computes L.T @ X # L LazyLinOp, X anything compatible
            L_possibly_cplx = 'complex' in str(dtype) or dtype is None
            X_possibly_cplx = 'complex' in str(X.dtype) or X.dtype is None
            if L_possibly_cplx:
                if X_possibly_cplx:
                    return rmatmat(X.real).conj() - rmatmat(1j * X.imag).conj()
                else:
                    # X is real
                    return rmatmat(X).conj()
            else:  # L is real
                return rmatmat(X)

        def MCX(X):
            # computes L.conj() @ X # L LazyLinOp, X anything compatible
            L_possibly_cplx = 'complex' in str(dtype) or dtype is None
            X_possibly_cplx = 'complex' in str(X.dtype) or X.dtype is None
            if L_possibly_cplx:
                if X_possibly_cplx:
                    return matmat(X.real).conj() + matmat(1j * X.imag)
                else:
                    # X is real
                    return matmat(X).conj()
            else:  # L is real
                return MX(X)

        lambdas = {'@': MX}
        lambdasT = {'@': MTX}
        lambdasH = {'@': MHX}
        lambdasC = {'@': MCX}
        # set lambdas temporarily to None (to satisfy the ctor)
        # they'll be initialized later
        for func in [lambdas, lambdasT, lambdasH, lambdasC]:
            func['T'] = None
            func['H'] = None
            func['slice'] = None

        lop = LazyLinOp._create_LazyLinOp(lambdas, shape,
                                          dtype=dtype,
                                          self=self)
        super(LazyLinOp, lop).__init__(lop.dtype, lop.shape)
        lopT = LazyLinOp._create_LazyLinOp(
            lambdasT, (shape[1], shape[0]), dtype=dtype)
        super(LazyLinOp, lopT).__init__(lopT.dtype, lopT.shape)
        lopH = LazyLinOp._create_LazyLinOp(
            lambdasH, (shape[1], shape[0]), dtype=dtype)
        super(LazyLinOp, lopH).__init__(lopH.dtype, lopH.shape)
        lopC = LazyLinOp._create_LazyLinOp(lambdasC, shape, dtype=dtype)
        super(LazyLinOp, lopC).__init__(lopC.dtype, lopC.shape)

        LazyLinOp._set_matching_lambdas(
            lambdas, lambdasT, lambdasH,
            lambdasC, lop, lopT, lopH, lopC)
        self = lop

    @staticmethod
    def _create_LazyLinOp(lambdas, shape, root_obj=None, dtype=None,
                          self=None):
        """
        Low-level constructor. Not meant to be used directly.

        Args:
            lambdas: starting operations.
            shape: (``tuple[int, int]``)
                the initial shape of the operator.
            root_obj: the initial object the operator is based on.

        .. seealso:: :py:func:`lazylinop.aslazylinop`.
        """
        if root_obj is not None:
            if not hasattr(root_obj, 'shape'):
                raise TypeError('The starting object to initialize a'
                                ' LazyLinOp must possess a shape'
                                ' attribute.')
            if len(root_obj.shape) != 2:
                raise ValueError('The starting object to initialize'
                                 ' a LazyLinOp must have two dimensions,'
                                 ' not: '+str(len(root_obj.shape)))

        if self is None:
            self = LazyLinOp(shape, dtype=dtype, internal_call=True)
        else:
            self.shape = shape
            self.dtype = dtype
        self.lambdas = lambdas
        self._check_lambdas()
        self._root_obj = root_obj
        return self

    def _check_lambdas(self):
        """
        Internal function for checking self.lambdas is well-formed
        (dict type and proper keys).
        """
        if not isinstance(self.lambdas, dict):
            raise TypeError('lambdas must be a dict')
        keys = self.lambdas.keys()
        for k in ['@', 'H', 'T', 'slice']:
            if k not in keys:
                raise ValueError(k+' is a mandatory lambda, it must be set in'
                                 ' self.lambdas')

    @staticmethod
    def _create_from_op(obj, shape=None):
        """
        See :py:func:`lazylinop.aslazylinop`.
        """
        if shape is None:
            oshape = obj.shape
        else:
            oshape = shape
        lambdas = {'@': lambda op: obj @ op}
        lambdasT = {'@': lambda op: obj.T @ op}
        lambdasH = {'@': lambda op: obj.T.conj() @ op}
        lambdasC = {'@': lambda op:
                    obj.conj() @ op if 'complex' in
                    str(obj.dtype) or obj.dtype is None
                    else obj @ op}
        # set lambdas temporarily to None (to satisfy the ctor)
        # they'll be initialized later
        for func in [lambdas, lambdasT, lambdasH, lambdasC]:
            func['T'] = None
            func['H'] = None
            func['slice'] = None  # TODO: rename slice to index

        lop = LazyLinOp._create_LazyLinOp(lambdas,
                                          oshape,
                                          obj,
                                          dtype=obj.dtype)
        lopT = LazyLinOp._create_LazyLinOp(lambdasT,
                                           (oshape[1], oshape[0]),
                                           obj,
                                           dtype=obj.dtype)
        lopH = LazyLinOp._create_LazyLinOp(lambdasH,
                                           (oshape[1], oshape[0]),
                                           obj,
                                           dtype=obj.dtype)
        lopC = LazyLinOp._create_LazyLinOp(lambdasC, oshape, obj,
                                           dtype=obj.dtype)

        LazyLinOp._set_matching_lambdas(
            lambdas, lambdasT, lambdasH, lambdasC,
            lop, lopT, lopH, lopC)

        return lop

    @staticmethod
    def _set_matching_lambdas(lambdas, lambdasT, lambdasH, lambdasC,
                              lop, lopT, lopH, lopC):
        """
        Internal function.
        Set the corresponding relations for operations/LazyLinOp-s.
        """
        lambdas['T'] = lambda: lopT
        lambdas['H'] = lambda: lopH
        lambdas['slice'] = lambda indices: (
            LazyLinOp._index_lambda(lop, indices)())
        lambdasT['T'] = lambda: lop
        lambdasT['H'] = lambda: lopC
        lambdasT['slice'] = lambda indices: (
            LazyLinOp._index_lambda(lopT, indices)())
        lambdasH['T'] = lambda: lopC
        lambdasH['H'] = lambda: lop
        lambdasH['slice'] = lambda indices: (
            LazyLinOp._index_lambda(lopH, indices)())
        lambdasC['T'] = lambda: lopH
        lambdasC['H'] = lambda: lopT
        lambdasC['slice'] = lambda indices: (
            LazyLinOp._index_lambda(lopC, indices)())

    @staticmethod
    def _create_from_scalar(s, shape):
        """
        Returns a :class:`LazyLinOp` ``L`` created scalar ``s``.

        ``L`` is such that ``l @ x == s * x``
        """
        if not np.isscalar(s):
            raise TypeError('s must be a scalar')

        def matmat(M): return M * s

        def rmatmat(M): return M * np.conj(s)

        scalar_op = LazyLinOp(shape, matmat=matmat,
                              rmatmat=rmatmat,
                              dtype=str(np.array([s]).dtype))
        return scalar_op

    def _checkattr(self, attr):
        if self._root_obj is not None and not hasattr(self._root_obj, attr):
            raise TypeError(attr+' is not supported by the root object of this'
                            ' LazyLinOp')

    def _index_lambda(lop, indices):
        from scipy.sparse import eye as seye

        def s():
            return (
                LazyLinOp._create_from_op(
                    seye(lop.shape[0], format='csr')[indices[0]])
                @ lop
                @ LazyLinOp._create_from_op(
                    seye(lop.shape[1], format='csr')[:, indices[1]])
            )
        return s

    @property
    def _shape(self):
        """
        The shape (``tuple[int, int]``) of the :class:`LazyLinOp`.
        """
        return self.shape

    @property
    def ndim(self):
        """
        The number of dimensions of the :class:`LazyLinOp`
        (it is always 2).
        """
        return 2

    def transpose(self):
        """
        Returns the :class:`LazyLinOp` transpose.
        """
        self._checkattr('transpose')
        return self.lambdas['T']()

    @property
    def T(self):
        """
        The :py:class:`LazyLinOp` transpose.
        """
        return self.transpose()

    def conj(self):
        """
        Returns the :py:class:`LazyLinOp` conjugate.
        """
        self._checkattr('conj')
        return self.H.T

    def conjugate(self):
        """
        Returns the :py:class:`LazyLinOp` conjugate.
        """
        return self.conj()

    def getH(self):
        """
        Returns the :py:class:`LazyLinOp` adjoint/transconjugate.
        """
        # self._checkattr('getH')
        return self.lambdas['H']()

    @property
    def H(self):
        """
        The :py:class:`LazyLinOp` adjoint/transconjugate.
        """
        return self.getH()

    def _adjoint(self):
        """
        Returns the LazyLinOp adjoint/transconjugate.
        """
        return self.H

    def _slice(self, indices):
        return self.lambdas['slice'](indices)

    def __add__(self, op):
        """
        Returns the LazyLinOp for self + op.

        Args:
            op: an object compatible with self for this binary operation.

        """
        self._checkattr('__add__')
        if not LazyLinOp.islazylinop(op):
            op = LazyLinOp._create_from_op(op)
        if op.shape != self.shape:
            raise ValueError('Dimensions must agree')
        lambdas = {'@': lambda o: self @ o + op @ o,
                   'H': lambda: self.H + op.H,
                   'T': lambda: self.T + op.T,
                   'slice': lambda indices:
                   self._slice(indices) + op._slice(indices)}
        new_op = LazyLinOp._create_LazyLinOp(lambdas=lambdas,
                                             shape=tuple(self.shape),
                                             root_obj=None)
        return new_op

    def __radd__(self, op):
        """
        Returns the LazyLinOp for op + self.

        Args:
            op: an object compatible with self for this binary operation.

        """
        return self.__add__(op)

    def __iadd__(self, op):
        """
        Not Implemented self += op.
        """
        raise NotImplementedError(LazyLinOp.__name__+".__iadd__")

    def __sub__(self, op):
        """
        Returns the LazyLinOp for self - op.

        Args:
            op: an object compatible with self for this binary operation.

        """
        self._checkattr('__sub__')
        if not LazyLinOp.islazylinop(op):
            op = LazyLinOp._create_from_op(op)
        lambdas = {'@': lambda o: self @ o - op @ o,
                   'H': lambda: self.H - op.H,
                   'T': lambda: self.T - op.T,
                   'slice': lambda indices:
                   self._slice(indices) - op._slice(indices)}
        new_op = LazyLinOp._create_LazyLinOp(lambdas=lambdas,
                                             shape=tuple(self.shape),
                                             root_obj=None)
        return new_op

    def __rsub__(self, op):
        """
        Returns the LazyLinOp for op - self.

        Args:
            op: an object compatible with self for this binary operation.

        """
        self._checkattr('__rsub__')
        if not LazyLinOp.islazylinop(op):
            op = LazyLinOp._create_from_op(op)
        lambdas = {'@': lambda o: op @ o - self @ o,
                   'H': lambda: op.H - self.H,
                   'T': lambda: op.T - self.T,
                   'slice': lambda indices:
                   op._slice(indices) - self._slice(indices)}
        new_op = LazyLinOp._create_LazyLinOp(lambdas=lambdas,
                                             shape=self.shape,
                                             root_obj=None)
        return new_op

    def __isub__(self, op):
        """
        Not implemented self -= op.
        """
        raise NotImplementedError(LazyLinOp.__name__+".__isub__")

    def __truediv__(self, s):
        """
        Returns the LazyLinOp for self / s.

        Args:
            s: a scalar.

        """
        new_op = self * (1/s)
        return new_op

    def __itruediv__(self, op):
        """
        Not implemented self /= op.
        """
        raise NotImplementedError(LazyLinOp.__name__+".__itruediv__")

    def __idiv__(self, op):
        """
        Not implemented self //= op.
        """
        raise NotImplementedError(LazyLinOp.__name__+".__idiv__")

    def _sanitize_matmul(self, op, swap=False):
        self._checkattr('__matmul__')
        sanitize_op(op)
        dim_err = ValueError('dimensions must agree')
        if (hasattr(self, 'ravel_op') and self.ravel_op and
                len(op.shape) >= 2):
            # see lazylinop.pad
            # array flattening is authorized for self LazyLinOp
            if ((not swap and
                 self.shape[1] != op.shape[-2] and
                 np.prod(op.shape) != self.shape[1])
                or
                (swap and self.shape[0] != op.shape[-2] and
                 np.prod(op.shape) != self.shape[0])):
                raise dim_err
            return  # flattened op is compatible to self
            # TODO: it should be made more properly
        if (len(op.shape) == 1 and
            self.shape[(int(swap) + 1) % 2] != op.shape[-1]
            or
            len(op.shape) >= 2 and
            (swap and op.shape[-1] != self.shape[0] or
             not swap and self.shape[1] != op.shape[-2])):
            raise dim_err

    def __matmul__(self, op):
        """
        Computes self @ op.

        Args:
            op: an object compatible with self for this binary operation.

        Returns:
            If op is an numpy array or a scipy matrix the function returns
            (``self @ op``) as a numpy array or a scipy matrix. Otherwise
            it returns the :class:`LazyLinOp` for the multiplication
            ``self @ op``.

        """
        from scipy.sparse import issparse
        self._sanitize_matmul(op)
        sanitize_op(op)
        if isinstance(op, np.ndarray) or issparse(op):
            if op.ndim == 1 and self._root_obj is not None:
                res = self.lambdas['@'](op.reshape(op.size, 1)).ravel()
            elif op.ndim > 2:
                from itertools import product
                # op.ndim > 2
                dtype = _binary_dtype(self.dtype, op.dtype)
                res = np.empty((*op.shape[:-2], self.shape[0], op.shape[-1]),
                               dtype=dtype)
                idl = [list(range(op.shape[i])) for i in range(op.ndim-2)]
                for t in product(*idl):
                    tr = (*t, slice(0, res.shape[-2]), slice(0, res.shape[-1]))
                    to = (*t, slice(0, op.shape[-2]), slice(0, op.shape[-1]))
                    R = self.lambdas['@'](op.__getitem__(to))
                    res.__setitem__(tr, R)
                # parallelization would not necessarily be faster because
                # successive matrix products are themselves parallelized
            else:
                res = self.lambdas['@'](op)
        else:
            if not LazyLinOp.islazylinop(op):
                op = LazyLinOp._create_from_op(op)
            lambdas = {'@': lambda o: self @ (op @ o),
                       'H': lambda: op.H @ self.H,
                       'T': lambda: op.T @ self.T,
                       'slice': lambda indices:
                       self._slice((indices[0], slice(0, self.shape[1])))
                       @ op._slice((slice(0, op.shape[0]), indices[1]))}
            res_shape = (self.shape[0], op.shape[1])
            res = LazyLinOp._create_LazyLinOp(lambdas=lambdas,
                                              shape=res_shape,
                                              root_obj=None,
                                              dtype=binary_dtype(self.dtype,
                                                                 op.dtype))
#            res = LazyLinOp._create_from_op(super(LazyLinOp,
#                                                     self).__matmul__(op))
        return res

    def dot(self, op):
        """
        Alias of LazyLinOp.__matmul__.
        """
        return self.__matmul__(op)

    def matvec(self, op):
        """
        This function is an alias of self @ op, where the multiplication might
        be specialized for op a vector (depending on how self has been defined
        ; upon on a operator object or through a matvec/matmat function).


        .. seealso:: lazylinop.LazyLinOp.
        """
        sanitize_op(op)
        if op.ndim != 1 and op.shape[0] != 1 and op.shape[1] != 1:
            raise ValueError('op must be a vector -- attribute ndim to 1 or'
                             ' shape[0] or shape[1] to 1')
        return self.__matmul__(op)

    def _rmatvec(self, op):
        """
        Returns self^H @ op, where self^H is the conjugate transpose of A.

        Returns:
            It might be a LazyLinOp or an array depending on the op type
            (cf. lazylinop.LazyLinOp.__matmul__).
        """
        # LinearOperator need.
        return self.T.conj() @ op

    def _matmat(self, op):
        """
        Alias of LazyLinOp.__matmul__.
        """
        return self.__matmul__(op)

    def _rmatmat(self, op):
        """
        Returns self^H @ op, where self^H is the conjugate transpose of A.

        Returns:
            It might be a LazyLinOp or an array depending on the op type
            (cf. lazylinop.LazyLinOp.__matmul__).
        """
        # LinearOperator need.
        return self.T.conj() @ op

    def __imatmul__(self, op):
        """
        Not implemented self @= op.
        """
        raise NotImplementedError(LazyLinOp.__name__+".__imatmul__")

    def __rmatmul__(self, op):
        """
        Returns op @ self.

        Args:
            op: an object compatible with self for this binary operation.

        Returns:
            a :class:`LazyLinOp` or an array depending on op type.

        .. seealso::
            :py:func:`LazyLinOp.__matmul__`
        """
        self._checkattr('__rmatmul__')
        from scipy.sparse import issparse
        self._sanitize_matmul(op, swap=True)
        if isinstance(op, np.ndarray) or issparse(op):
            res = (self.H @ op.T.conj()).T.conj()
        else:
            # this code doesn't make sense because:
            # - either op has implemented __matmul__ and then
            # it would have been called on op @ something/LazyLinOp
            # - or op hasn't __matmul__ implemented and we end up here but
            # the lambdas['@'] below relies on __matmul__ so it would fail
            # anyway

            # if not LazyLinOp.islazylinop(op):
            # op = LazyLinOp._create_from_op(op)
            # lambdas = {'@': lambda o: (op @ self) @ o,
            # 'H': lambda: self.H @ op.H,
            # 'T': lambda: self.T @ op.T,
            # 'slice': lambda indices: (op @ self)._slice(indices)}
            # res_shape = (op.shape[0], self.shape[1])
            # res = LazyLinOp._create_LazyLinOp(lambdas=lambdas,
            # shape=res_shape,
            # root_obj=None)
            raise TypeError(str(op)+" has no __matmul__ operation.")
        return res

    def __mul__(self, other):
        """
        Returns the LazyLinOp for self * other if other is a scalar
        otherwise returns self @ other.

        Args:
            other: a scalar or a vector/array.

        .. seealso:: lazylinop.LazyLinOp.__matmul__)
        """
        self._checkattr('__mul__')
        if np.isscalar(other):
            Dshape = (self.shape[1], self.shape[1])
            new_op = self @ LazyLinOp._create_from_scalar(other, Dshape)
        else:
            new_op = self @ other
        return new_op

    def __rmul__(self, other):
        """
        Returns other * self.

        Args:
            other: a scalar or a vector/array.

        """
        if np.isscalar(other):
            return self * other
        else:
            return other @ self

    def __imul__(self, op):
        """
        Not implemented self *= op.
        """
        raise NotImplementedError(LazyLinOp.__name__+".__imul__")

    def toarray(self):
        """
        Returns self as a numpy array.
        """
        # from scipy.sparse import eye
        # return self @ eye(self.shape[1], self.shape[1], format='csr')
        # don't use csr because of function based LazyLinOp
        # (e.g. scipy fft receives only numpy array)
        return self @ np.eye(self.shape[1], order='F', dtype=self.dtype)

    def __getitem__(self, indices):
        """
        Returns the LazyLinOp for slicing/indexing.

        Args:
            indices:
                array of length 1 or 2 which elements must be slice, integer or
                Ellipsis (...). Note that using Ellipsis for more than two
                indices is normally forbidden.

        """
        self._checkattr('__getitem__')
        if isinstance(indices, int):
            indices = (indices, slice(0, self.shape[1]))
        if (isinstance(indices, tuple) and len(indices) == 2 and
                isinstance(indices[0], int) and isinstance(indices[1], int)):
            return self.toarray().__getitem__(indices)
        elif isinstance(indices, slice) or isinstance(indices[0], slice) and \
                isinstance(indices[0], slice):
            return self._slice(indices)
        else:
            return self._slice(indices)

    def concatenate(self, *ops, axis=0):
        """
        Returns the LazyLinOp for the concatenation of self and op.

        Args:
            axis: axis of concatenation (0 for rows, 1 for columns).
        """
        out = self
        for op in ops:
            if axis == 0:
                out = out.vstack(op)
            elif axis == 1:
                out = out.hstack(op)
            else:
                raise ValueError('axis must be 0 or 1')
        return out

    def _vstack_slice(self, op, indices):
        rslice = indices[0]
        if isinstance(rslice, int):
            rslice = slice(rslice, rslice+1, 1)
        if rslice.step is not None and rslice.step != 1:
            raise ValueError('Can\'t handle non-contiguous slice -- step > 1')
        if rslice.start is None:
            rslice = slice(0, rslice.stop, rslice.step)
        if rslice.stop is None:
            rslice = slice(rslice.start, self.shape[0] + op.shape[0],
                           rslice.step)
        if rslice.stop > self.shape[0] + op.shape[0]:
            raise ValueError('Slice overflows the row dimension')
        if rslice.start >= 0 and rslice.stop <= self.shape[0]:
            # the slice is completly in self
            return lambda: self._slice(indices)
        elif rslice.start >= self.shape[0]:
            # the slice is completly in op
            return lambda: op._slice((slice(rslice.start - self.shape[0],
                                            rslice.stop - self.shape[0]),
                                      indices[1]))
        else:
            # the slice is overlapping self and op
            self_slice = self._slice((slice(rslice.start, self.shape[0]),
                                      indices[1]))
            op_slice = self._slice((slice(0, rslice.stop - self.shape[0]),
                                    indices[1]))
            return lambda: self_slice.vstack(op_slice)

    def _vstack_mul_lambda(self, op, o):
        from scipy.sparse import issparse

        def mul_mat(o):
            return np.vstack((self @ o, op @ o))

        def mul_vec(o):
            # self.shape[1] == op.shape[1] == vcat(self, op).shape[1]
            return mul_mat(o.reshape(self.shape[1], 1)).ravel()

        def mul_mat_vec():
            return mul_vec(o) if len(o.shape) == 1 else mul_mat(o)

        def mul():
            return (mul_mat_vec() if isinstance(o, np.ndarray)
                    or issparse(o) else self.vstack(op) @ o)

        return mul

    def vstack(self, op):
        """
        See lazylinop.vstack.
        """
        if self.shape[1] != op.shape[1]:
            raise ValueError('self and op numbers of columns must be the'
                             ' same')
        if not LazyLinOp.islazylinop(op):
            op = LazyLinOp._create_from_op(op)
        lambdas = {'@': lambda o: self._vstack_mul_lambda(op, o)(),
                   'H': lambda: self.H.hstack(op.H),
                   'T': lambda: self.T.hstack(op.T),
                   'slice': lambda indices: self._vstack_slice(op, indices)()}
        new_shape = (self.shape[0] + op.shape[0], self.shape[1])
        new_op = LazyLinOp._create_LazyLinOp(lambdas=lambdas,
                                             shape=new_shape,
                                             root_obj=None,
                                             dtype=binary_dtype(self.dtype,
                                                                op.dtype))
        return new_op

    def _hstack_slice(self, op, indices):
        cslice = indices[1]
        if isinstance(cslice, int):
            cslice = slice(cslice, cslice+1, 1)
        if cslice.step is not None and cslice.step != 1:
            raise ValueError('Can\'t handle non-contiguous slice -- step > 1')
        if cslice.stop is None:
            cslice = slice(cslice.start, self.shape[1] + op.shape[1],
                           cslice.step)
        if cslice.start is None:
            cslice = slice(0, cslice.stop, cslice.step)
        if cslice.stop > self.shape[1] + op.shape[1]:
            raise ValueError('Slice overflows the row dimension')
        if cslice.start >= 0 and cslice.stop <= self.shape[1]:
            # the slice is completly in self
            return lambda: self._slice(indices)
        elif cslice.start >= self.shape[1]:
            # the slice is completly in op
            return lambda: op._slice((indices[0],
                                      slice(cslice.start - self.shape[1],
                                            cslice.stop - self.shape[1])))
        else:
            # the slice is overlapping self and op
            self_slice = self._slice((indices[0], slice(cslice.start,
                                                        self.shape[1])))
            op_slice = self._slice((indices[0], slice(0, cslice.stop -
                                                      self.shape[1])))
            return lambda: self_slice.hstack(op_slice)

    def _hstack_mul_lambda(self, op, o):
        from scipy.sparse import issparse

        def mul_mat(o):
            s_ncols = self.shape[1]
            return self @ o[:s_ncols] + op @ o[s_ncols:]

        def mul_vec(o):
            return mul_mat(o.reshape(op.shape[1] + self.shape[1], 1)).ravel()

        def mul_mat_vec():
            return mul_vec(o) if len(o.shape) == 1 else mul_mat(o)

        def mul():
            return (mul_mat_vec() if isinstance(o, np.ndarray)
                    or issparse(o) else self.hstack(op) @ o)

        return mul

    def hstack(self, op):
        """
        See lazylinop.hstack.
        """
        if self.shape[0] != op.shape[0]:
            raise ValueError('self and op numbers of rows must be the'
                             ' same')
        if not LazyLinOp.islazylinop(op):
            op = LazyLinOp._create_from_op(op)
        lambdas = {'@': lambda o: self._hstack_mul_lambda(op, o)(),
                   'H': lambda: self.H.vstack(op.H),
                   'T': lambda: self.T.vstack(op.T),
                   'slice': lambda indices: self._hstack_slice(op, indices)()}
        new_op = LazyLinOp._create_LazyLinOp(
            lambdas=lambdas,
            shape=(self.shape[0], self.shape[1] + op.shape[1]),
            root_obj=None,
            dtype=binary_dtype(self.dtype, op.dtype))
        return new_op

    @property
    def real(self):
        """
        The :py:class:`LazyLinOp` for real part of this
        :py:class:`LazyLinOp`.
        """
        from scipy.sparse import issparse
        lambdas = {'@': lambda o: (self @ o.real).real +
                   (self @ o.imag * 1j).real if isinstance(o, np.ndarray)
                   or issparse(o) else (self @ o).real,
                   'H': lambda: self.T.real,
                   'T': lambda: self.T.real,
                   'slice': lambda indices: self._slice(indices).real}
        new_op = LazyLinOp._create_LazyLinOp(lambdas=lambdas,
                                             shape=tuple(self.shape),
                                             root_obj=None)
        return new_op

    @property
    def imag(self):
        """
        The :py:class:`LazyLinOp` for the imaginary part of this
        :py:class:`LazyLinOp`.
        """
        from scipy.sparse import issparse
        lambdas = {'@': lambda o: (self @ o.real).imag +
                   (self @ (1j * o.imag)).imag if isinstance(o, np.ndarray)
                   or issparse(o) else (self @ o).imag,
                   'H': lambda: self.T.imag,
                   'T': lambda: self.T.imag,
                   'slice': lambda indices: self._slice(indices).imag}
        new_op = LazyLinOp._create_LazyLinOp(lambdas=lambdas,
                                             shape=tuple(self.shape),
                                             root_obj=None)
        return new_op

    def __neg__(self):
        """
        Returns the negative ::py:class:`LazyLinOp` of self.

        Example:
            >>> from lazylinop import aslazylinop
            >>> import numpy as np
            >>> M = np.random.rand(10, 12)
            >>> lM = aslazylinop(M)
            >>> - lM
            <10x12 LazyLinOp with dtype=float64>
        """
        return self * -1

    def __pos__(self):
        """
        Returns the positive ::py:class:`LazyLinOp` of self.

        Example:
            >>> from lazylinop import aslazylinop
            >>> import numpy as np
            >>> M = np.random.rand(10, 12)
            >>> lM = aslazylinop(M)
            >>> +lM
            <10x12 LazyLinOp with dtype=float64>
        """
        return self

    def __pow__(self, n):
        """
        Returns the :py:class:`LazyLinOp` for the n-th power of self.

        .. warning::

            self must be square or this operation raises an exception.
        """
        from lazylinop.wip.polynomial import power
        return power(self, n)

    @staticmethod
    def islazylinop(obj):
        """
        Returns ``True`` if ``obj`` is a ``LazyLinOp``, ``False`` otherwise.
        """
        return isinstance(obj, LazyLinOp)

    def check(self):
        """
        Verifies validity assertions on any :py:class:`LazyLinOp`.

        **Notations**:

        - Let ``op`` a :py:class:`LazyLinOp`,
        - ``u``, ``v`` vectors such that ``u.shape[0] == op.shape[1]``
          and ``v.shape[0] == op.shape[0]``,
        - ``X``, ``Y`` 2d-arrays such that ``X.shape[0] == op.shape[1]``
          and ``Y.shape[0] == op.shape[0]``.

        The function verifies that:

            1. ``(op @ u).shape == (op.shape[0],)``,
            2. ``(op.H @ v).shape == (op.shape[1],)``,
            3. ``(op @ u).conj().T @ v == u.conj().T @ op.H @ v``,
            4. ``op @ X @ Y.H == (Y @ (X.H @ op.H)).H``,
            5. ``op.H @ Y`` is equal to the horizontal concatenation of all
               ``op.H @ Y[:, j]`` for j in {0, ..., ``Y.shape[1]-1``}.
            6. ``op @ X`` is equal to the horizontal concatenation of all
               ``op @ X[:, j]`` for j in {0, ..., ``X.shape[1]-1``}.


        .. warning:: This function has a computational cost of several
                     matrix products.
                     It shouldn't be used into an efficient implementation but
                     only to test a :py:class:`.LazyLinOp` works properly.

        Args:
            op: (:py:class:`LazyLinOp`)
                Operator to test.

        Example:
            >>> from numpy.random import rand
            >>> from lazylinop import aslazylinop, LazyLinOp
            >>> M = rand(12, 14)
            >>> # numpy array M is OK as a LazyLinOp
            >>> aslazylinop(M).check()
            >>> # the next LazyLinOp is not
            >>> L2 = LazyLinOp((5, 2), matmat=lambda x: np.ones((6, 7)))
            >>> L2.check()
            Traceback (most recent call last):
            ...
            Exception: Wrong operator dimension

        .. seealso::
            :py:func:`aslazylinop`,
            :py:class:`LazyLinOp`
        """
        u = np.random.randn(self.shape[1])
        v = np.random.randn(self.shape[0])
        X = np.random.randn(self.shape[1], 3)
        Y = np.random.randn(self.shape[0], 3)
        # Check operator - vector product dimension
        if (self @ u).shape != (self.shape[0],):
            raise Exception("Wrong operator dimension")
        # Check operator adjoint - vector product dimension
        if (self.H @ v).shape != (self.shape[1],):
            raise Exception("Wrong operator adjoint dimension")
        # Check operator - matrix product consistency
        AX = self @ X
        for i in range(X.shape[1]):
            if not np.allclose(AX[:, i], self @ X[:, i]):
                raise Exception("Wrong operator matrix product")
#        if not np.allclose(
#                self @ X,
#                np.hstack([(self @ X[:, i]).reshape(-1, 1)
#                           for i in range(X.shape[1])])):
#            raise Exception("Wrong operator matrix product")
        # Dot test to check forward - adjoint consistency
        if not np.allclose((self @ u).conj().T @ v, u.conj().T @ (self.H @ v)):
            raise Exception("Operator and its adjoint do not match")
        if (self.T @ Y).shape[0] != self.shape[1]:
            raise Exception("Wrong operator transpose dimension"
                            " (when multiplying an array)")
        if not np.allclose(AX @ Y.T.conj(), (Y @ AX.T.conj()).T.conj()):
            raise Exception("Wrong operator on (Y @ X.H @ self.H).H")
        del AX
        # Check operator transpose dimension
        AY = self.H @ Y
        if AY.shape[0] != self.shape[1]:
            raise Exception("Wrong operator transpose dimension"
                            " (when multiplying an array)")
        # Check operator adjoint on matrix product
        for i in range(X.shape[1]):
            if not np.allclose(AY[:, i], self.H @ Y[:, i]):
                raise Exception("Wrong operator adjoint on matrix product")
#        if not np.allclose(self.H @ Y,
#                           np.hstack([(self.H @ Y[:, i]).reshape(-1, 1)
#                                      for i in range(X.shape[1])])):
#             raise Exception("Wrong operator adjoint on matrix product")
        del AY


def binary_dtype(A_dtype, B_dtype):
    """
    Returns the "greatest" dtype in size between A_dtype and B_dtype.
    If one dtype is complex the returned dtype is too.
    """
    if isinstance(A_dtype, str):
        A_dtype = np.dtype(A_dtype)
    if isinstance(B_dtype, str):
        B_dtype = np.dtype(B_dtype)
    if A_dtype is None and B_dtype is None:
        return None
    # ('complex', None) always gives 'complex'
    # because whatever None is hiding
    # the binary op result will be complex
    # but (real, None) gives None
    # because a None might or might not hide
    # a complex type
    if A_dtype is None:
        if 'complex' in str(B_dtype):
            return B_dtype
        return None
    if B_dtype is None:
        if 'complex' in str(A_dtype):
            return A_dtype
        return None
    # simply rely on numpy dtype
    np_res = (np.array([1], dtype=A_dtype) * np.array([1], dtype=B_dtype))
    return np_res.dtype


_binary_dtype = binary_dtype  # temporary private alias for retro-compat.


def sanitize_op(op, op_name='op'):
    if not hasattr(op, 'shape') or not hasattr(op, 'ndim'):
        raise TypeError(op_name+' must have shape and ndim attributes')


_sanitize_op = sanitize_op  # temporary private alias for retro-compat.


def islazylinop(obj):
    """
    Returns ``True`` if ``obj`` is a ``LazyLinOp``, ``False`` otherwise.
    """
    return LazyLinOp.islazylinop(obj)


def aslazylinop(op, shape=None):
    """
    Creates a :class:`LazyLinOp` based on linear operator ``op``.

    .. note::
        ``op`` must support operations and attributes defined in the
        :class:`LazyLinOp` class. Especially, an implementation of the
        matrix multiplication ``@``.
        Any operation not supported would raise an exception at evaluation
        time.

    Args:
        op: (``object``)
            The linear operator object used to create a :class:`LazyLinOp`.
            (it could be a numpy array, a scipy matrix, or any compatible
            linear operator).
        shape: (``tuple[int, int]``)
            The shape of the resulting :class:`LazyLinOp`.
            If ``None`` the function relies on ``op.shape``.
            This argument allows to overidde ``op.shape`` if for any reason it
            is not well defined (see below, the example of
            ``pylops.Symmetrize`` defective shape).


    Returns:
        A :class:`LazyLinOp` instance based on ``op``.

    **Examples**:

        Creating a :class:`LazyLinOp` based on a numpy array:
            >>> from lazylinop import aslazylinop
            >>> import numpy as np
            >>> M = np.random.rand(10, 12)
            >>> lM = aslazylinop(M)
            >>> twolM = lM + lM
            >>> twolM
            <10x12 LazyLinOp with unspecified dtype>


        Creating a :class:`LazyLinOp` based on a `pyfaust.Faust`_:
            >>> import pyfaust as pf
            >>> F = pf.rand(10, 12)
            >>> lF = aslazylinop(F)
            >>> twolF = lF + lF
            >>> twolF
            <10x12 LazyLinOp with unspecified dtype>

        Using the ``shape`` argument on a "defective" case:
            >>> # To illustrate the use of the optional “shape” parameter,
            >>> # let us consider implementing a lazylinearoperator
            >>> # associated with the pylops.Symmetrize linear operator,
            >>> # (version 2.1.0 is used here)
            >>> # which is designed to symmetrize a vector, or a matrix,
            >>> # along some coordinate axis
            >>> from pylops import Symmetrize
            >>> M = np.random.rand(22, 2)
            >>> # Here we want to symmetrize M
            >>> # vertically (axis == 0), so we build the corresponding
            >>> # symmetrizing operator Sop
            >>> Sop = Symmetrize(M.shape, axis=0)
            >>> # Applying the operator to M works, and the symmetrized matrix
            >>> # has 43 = 2*22-1 rows, and 2 columns (as many as M)
            >>> # as expected!
            >>> (Sop @ M).shape
            (43, 2)
            >>> # Since it maps matrices with 22 rows to matrices with 43 rows,
            >>> # as we intend the “shape” of Sop should be (43,22)
            >>> # however, the “shape” as provided by pylops is inconsistent
            >>> Sop.shape
            (86, 44)
            >>> # To use Sop as a LazyLinOp we cannot rely on the “shape”
            >>> # given by pylops (otherwise the LazyLinOp-matrix product
            >>> # wouldn't be properly defined)
            >>> # Thanks to the optional “shape” parameter of
            >>> # aslazylinop,
            >>> #this can be fixed
            >>> lSop = aslazylinop(Sop, shape=(43, 22))
            >>> # now lSop.shape is consistent
            >>> lSop.shape
            (43, 22)
            >>> (lSop @ M).shape
            (43, 2)
            >>> # Besides, Sop @ M is equal to lSop @ M, so all is fine!
            >>> np.allclose(lSop @ M, Sop @ M)
            True

    .. _pyfaust.Faust:
        https://faustgrp.gitlabpages.inria.fr/faust/last-doc/html/classpyfaust_1_1Faust.html

    .. seealso::
        `pyfaust.rand
        <https://faustgrp.gitlabpages.inria.fr/faust/last-doc/html/namespacepyfaust.html#abceec3d0838435ceb3df1befd1e29acc>`_,
        `pylops.Symmetrize
        <https://pylops.readthedocs.io/en/latest/api/generated/pylops.Symmetrize.html>`_.

    """
    if islazylinop(op):
        return op
    return LazyLinOp._create_from_op(op, shape)

# below are deprecated names


def aslazylinearoperator(op, shape=None):
    from warnings import warn
    warn("aslazylinearoperator is a deprecated name and will disappear in a"
         " next version. Please use aslazylinop.")
    return aslazylinop(op, shape)


def isLazyLinearOp(obj):
    from warnings import warn
    warn("isLazyLinearOp is a deprecated name and will disappear in a"
         " next version. Please use islazylinop.")
    return islazylinop(obj)


class LazyLinearOp(LazyLinOp):

    def __init__(self, *args, **kwargs):
        from warnings import warn
        warn("LazyLinearOp is a deprecated name and will disappear in a"
             " next version. Please use LazyLinOp.")
        super(LazyLinearOp, self).__init__(*args, **kwargs)
