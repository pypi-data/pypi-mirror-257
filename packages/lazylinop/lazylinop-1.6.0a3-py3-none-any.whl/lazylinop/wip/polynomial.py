"""
Module for polynomial related :py:class:`.LazyLinOp`-s.

It provides "polynomial as :py:class:`.LazyLinOp`" functions for which
the polynomial variable is itself a linear operator (especially a
:py:class:`.LazyLinOp`). Below are the provided functions:

    - :py:func:`.polyval` for evaluating general polynomials.
    - :py:func:`.chebval` which is specialized for Chebyshev polynomials.
    - :py:func:`.polyvalfromroots` and :py:func:`.chebvalfromroots` do the same
      but defining the polynomial from its roots.
    - :py:func:`.power` for the n-th power of any linear operator.

Besides, the two classes :py:class:`.poly` and :py:class:`.cheb` allow
to make computations with respectively general polynomials or in particular
with Chebyshev's. With ``p1`` and ``p2`` two polynomial instances, one can:

    - add/substract: ``(p1 + p2)(Op)``, ``(p1 - p2)(Op)`` with ``Op`` the
      polynomial variable (a :py:class:`.LazyLinOp`, :py:class:`.poly` or
      :py:class:`.cheb`). Evaluating and applying the polynomials on the
      fly is also possible: ``(p1 + p2)(Op) @ x``.
    - The same is possible to multiply (``@``), divide (``//``) and modulo
      (``%``) two polynomials (``(p1 @ p2)(Op)``, ``(p1 // p2)(Op)``,
      ``(p1 % p2)(Op)``.
    - And compose two polynomials: ``(p1(p2))(Op)`` .

.. admonition:: More details about implementation and features

   The classes :py:class:`.poly` and :py:class:`cheb` extend
   :py:class:`numpy.polynomial.Polynomial` and
   :py:class:`numpy.polynomial.Chebyshev`.
   They override the method :py:meth:`__call__` to implement the polynomial
   evaluation and calculate on the fly the available operations.
   Under the hood :py:func:`polyval`, :py:func:`chebval`,
   :py:func:`hermval`, :py:func:`lagval` or :py:func:`legval` are called
   depending on the polynomial form.
.. You can also use :py:func:`chebvalfromroots` that consider polynomial
   in monomial form before to convert into Chebyshev form.
   To compute n-th power of a LazyLinOp use :py:func:`power` or
   create :py:class:`poly` instance such that only n-th coefficient
   is equal to one while the others are equal to zero.

"""

import numpy as np
from numpy.polynomial import Polynomial as P
from numpy.polynomial import Chebyshev as T
from numpy.polynomial import Hermite as H
from numpy.polynomial import Laguerre as La
from numpy.polynomial import Legendre as Le
from lazylinop import binary_dtype, islazylinop, LazyLinOp
import warnings
from warnings import warn
warnings.simplefilter(action='always')


def Xpoly(coef, domain=[-1.0, 1.0], window=[-1.0, 1.0],
          symbol='x', kind: str='monomial'):
    r"""Return instance amongst P, T, H, La or Le according to kind.

    Args:
        coef: list
            List of coefficients
        domain: list, optional
            see :py:class:`numpy.polynomial.Polynomial`
        window: list, optional
            see :py:class:`numpy.polynomial.Polynomial`
        symbol: str, optional
            see :py:class:`numpy.polynomial.Polynomial`
        kind: str, optional
            Representation of the polynomial.
            It could be 'monomial' (default), 'chebyshev',
            'hermite' (physicist), 'laguerre', 'legendre' and 'roots'.
            If kind is 'roots', coef is considered to be
            the roots of the polynomial. Leading coefficient is the
            last element coef[:-1] of coef argument while the first
            values are the roots of the polynomial.
            Because of :math:`(Op - r_0Id)\cdots (Op - r_nId)`
            coefficient :math:`c_n` of the highest power :math:`c_nOp^n`
            is always 1.

    Raises:
        ValueError
            coef size must be > 0.
        ValueError
            kind must be either monomial, chebyshev, hermite, laguerre, legendre or roots.

    Examples:
        >>> from lazylinop.wip.polynomial import Xpoly
        >>> p = Xpoly([1.0, 2.0, 3.0])

    .. seealso::
        `numpy.polynomial package
        <https://numpy.org/doc/stable/reference/routines.polynomials.html>`_.
    """
    if type(coef) is list:
        coef = np.asarray(coef)
    if coef.shape[0] < 1:
        raise ValueError("coef size must be > 0.")
    if kind == 'monomial':
        return poly(coef, domain, window, symbol, form='x')
    elif kind == 'chebyshev':
        return cheb(coef, domain, window, symbol)
    elif kind == 'hermite':
        return herm(coef, domain, window, symbol)
    elif kind == 'laguerre':
        return lag(coef, domain, window, symbol)
    elif kind == 'legendre':
        return leg(coef, domain, window, symbol)
    elif kind == 'roots':
        if coef.shape[0] == 1:
            return poly(coef, domain, window, symbol, form='x')
        else:
            return poly(coef, domain, window, symbol, form='roots')
    else:
        raise ValueError("kind must be either monomial, chebyshev, hermite, laguerre, legendre or roots.")


def composition(p, op):
    """Return composition p(op).

    Args:
        p: poly, cheb, herm, lag or leg
        op: P, T, H, La or Le

    Raises:
        Exception
            op must be an instance of either P, T, H, La or Le.
        Exception
            p must be an instance of either poly, cheb, herm, lag or leg.

    .. seealso::
        `numpy.polynomial package
        <https://numpy.org/doc/stable/reference/routines.polynomials.html>`_.
    """
    if not isinstance(p, poly) and not isinstance(p, cheb) \
        and not isinstance(p, herm) and not isinstance(p, lag) \
        and not isinstance(p, leg):
        raise Exception(
            "p must be an instance of either poly, cheb, herm, lag or leg.")
    if isinstance(op, P):
        tmp = P.__call__(p, op)
        return poly(tmp.coef, domain=tmp.domain, window=tmp.window)
    elif isinstance(op, T):
        tmp = T.__call__(p, op)
        return cheb(tmp.coef, domain=tmp.domain, window=tmp.window)
    elif isinstance(op, H):
        tmp = H.__call__(p, op)
        return herm(tmp.coef, domain=tmp.domain, window=tmp.window)
    elif isinstance(op, La):
        tmp = La.__call__(p, op)
        return lag(tmp.coef, domain=tmp.domain, window=tmp.window)
    elif isinstance(op, Le):
        tmp = Le.__call__(p, op)
        return leg(tmp.coef, domain=tmp.domain, window=tmp.window)
    else:
        raise Exception("op must be an instance of either P, T, H, La or Le.")
        

class poly(P):
    """This class implements a polynomial class derived from
    :py:class:`numpy.polynomial.Polynomial` and so relies on NumPy polynomial
    package to manipulate polynomials.

    See :py:mod:`lazylinop.wip.polynomial` for an introduction to implemented
    operations and their basic use.
    """

    def __init__(self, coef, domain=[-1.0, 1.0], window=[-1.0, 1.0],
                 symbol='x', form: str='x'):
        """Init instance of poly.

        Args:
            coef: list
                List of coefficients
            domain: list, optional
                see :py:class:`numpy.polynomial.Polynomial`
            window: list, optional
                see :py:class:`numpy.polynomial.Polynomial`
            symbol: str, optional
                see :py:class:`numpy.polynomial.Polynomial`
            form: str, optional
            If form is 'x' use polynomial coefficients.
            If form is 'roots' computes polynomial coefficients
            from roots. Last element coef[-1] of coef is the
            leading coefficient.

        Raises:
            ValueError
                form must be either 'x' or 'roots'.

        Examples:
            >>> from lazylinop.wip.polynomial import poly
            >>> p = poly([1.0, 2.0, 3.0])

        .. seealso::
            `numpy.polynomial package
            <https://numpy.org/doc/stable/reference/routines.polynomials.html>`_.
        """
        if form == 'x' or coef.shape[0] == 1:
            # If coef.shape is (1, ) there is only leading coefficient
            self.roots = None
            self.leading_coef = coef[-1]
            P.__init__(self, coef, domain, window, symbol)
        elif form == 'roots':
            self.roots = coef[:-1]
            self.leading_coef = coef[-1]
            # Last element coef[-1] of coef is the leading coefficient.
            # np.polynomial.polynomial.polyfromroots does not use it.
            P.__init__(self, np.polynomial.polynomial.polyfromroots(self.roots),
                       domain, window, symbol)
        else:
            raise ValueError("form must be either 'x' or 'roots'.")

    def __call__(self, op):
        """
        Thanks to Python :py:meth:`__call__` instance behaves like function.
        If op is a LazyLinOp, return polynomial of op applied to a 1d or
        2d array.
        If op is a P, T, H, La or Le instance, return a poly instance.

        Args:
            op: LazyLinOp, P, T, H, La or Le

        Raises:
            TypeError
                Unexpected op.

        Examples:
            >>> from lazylinop import eye, islazylinop
            >>> from lazylinop.wip.polynomial import poly
            >>> p = poly([1.0, 2.0, 3.0])
            >>> L = eye(3, n=3, k=0)
            >>> islazylinop(p(L))
            True
            >>> x = np.random.randn(3)
            >>> np.allclose(6.0 * x, p(L) @ x)
            True
        """
        if islazylinop(op):
            if self.roots is None:
                return polyval(op, self.coef)
            else:
                return polyvalfromroots(op, self.roots)
        elif isinstance(op, P) or isinstance(op, T) or isinstance(op, H) \
             or isinstance(op, La) or isinstance(op, Le):
            return composition(self, op)
        else:
            raise TypeError('Unexpected op.')


class cheb(T):
    """This class implements a Chebyshev polynomial class derived from
    :py:class:`numpy.polynomial.Chebyshev` and so relies on NumPy polynomial
    package to manipulate polynomials.

    See :py:mod:`lazylinop.wip.polynomial` for an introduction to implemented
    operations and their basic use.
    """

    def __init__(self, coef, domain=[-1.0, 1.0], window=[-1.0, 1.0],
                 symbol='x'):
        """Init instance of cheb.

        Args:
            coef: list
                List of coefficients
            domain: list, optional
                see :py:class:`numpy.polynomial.Chebyshev`
            window: list, optional
                see :py:class:`numpy.polynomial.Chebyshev`
            symbol: str, optional
                see :py:class:`numpy.polynomial.Chebyshev`

        Examples:
            >>> from lazylinop.wip.polynomial import cheb
            >>> t = cheb([1.0, 2.0, 3.0])

        .. seealso::
            `numpy.polynomial package
            <https://numpy.org/doc/stable/reference/routines.polynomials.html>`_.
        """
        T.__init__(self, coef, domain, window, symbol)

    def __call__(self, op):
        """
        Thanks to Python :py:meth:`__call__` instance behaves like function.
        If op is a LazyLinOp, return polynomial of op applied to a 1d or
        2d array.
        If op is a P, T, H, La or Le instance, return a poly instance.

        Args:
            op: LazyLinOp, P, T, H, La or Le

        Raises:

        Examples:
            >>> from lazylinop import eye, islazylinop
            >>> from lazylinop.wip.polynomial import cheb
            >>> t = poly([1.0, 2.0, 3.0])
            >>> L = eye(3, n=3, k=0)
            >>> islazylinop(t(L))
            True
        """
        if islazylinop(op):
            return chebval(op, self.coef)
        elif isinstance(op, P) or isinstance(op, T) or isinstance(op, H) \
             or isinstance(op, La) or isinstance(op, Le):
            return composition(self, op)
        else:
            raise TypeError('Unexpected op.')


class herm(H):
    """This class implements a Hermite (physicist) polynomial class derived from
    :py:class:`numpy.polynomial.Hermite` and so relies on NumPy polynomial package
    to manipulate polynomials.

    See :py:mod:`lazylinop.wip.polynomial` for an introduction to implemented
    operations and their basic use.
    """

    def __init__(self, coef, domain=[-1.0, 1.0], window=[-1.0, 1.0],
                 symbol='x'):
        """Init instance of herm.

        Args:
            coef: list
                List of coefficients
            domain: list, optional
                see :py:class:`numpy.polynomial.Hermite`
            window: list, optional
                see :py:class:`numpy.polynomial.Hermite`
            symbol: str, optional
                see :py:class:`numpy.polynomial.Hermite`

        Examples:
            >>> from lazylinop.wip.polynomial import herm
            >>> h = herm([1.0, 2.0, 3.0])

        .. seealso::
            `numpy.polynomial package
            <https://numpy.org/doc/stable/reference/routines.polynomials.html>`_.
        """
        H.__init__(self, coef, domain, window, symbol)

    def __call__(self, op):
        """
        Thanks to Python :py:meth:`__call__` instance behaves like function.
        If op is a LazyLinOp, return polynomial of op applied to a 1d or
        2d array.
        If op is a P, T, H, La or Le instance, return a poly instance.

        Args:
            op: LazyLinOp, P, T, H, La or Le

        Raises:

        Examples:
            >>> from lazylinop import eye, islazylinop
            >>> from lazylinop.wip.polynomial import herm
            >>> h = herm([1.0, 2.0, 3.0])
            >>> L = eye(3, n=3, k=0)
            >>> islazylinop(h(L))
            True
        """
        if islazylinop(op):
            return hermval(op, self.coef)
        elif isinstance(op, P) or isinstance(op, T) or isinstance(op, H) \
             or isinstance(op, La) or isinstance(op, Le):
            return composition(self, op)
        else:
            raise TypeError('Unexpected op.')


class lag(H):
    """This class implements a Laguerre polynomial class derived from
    :py:class:`numpy.polynomial.Laguerre` and so relies on NumPy polynomial package
    to manipulate polynomials.

    See :py:mod:`lazylinop.wip.polynomial` for an introduction to implemented
    operations and their basic use.
    """

    def __init__(self, coef, domain=[-1.0, 1.0], window=[-1.0, 1.0],
                 symbol='x'):
        """Init instance of lag.

        Args:
            coef: list
                List of coefficients
            domain: list, optional
                see :py:class:`numpy.polynomial.Laguerre`
            window: list, optional
                see :py:class:`numpy.polynomial.Laguerre`
            symbol: str, optional
                see :py:class:`numpy.polynomial.Laguerre`

        Examples:
            >>> from lazylinop.wip.polynomial import lag
            >>> la = lag([1.0, 2.0, 3.0])

        .. seealso::
            `numpy.polynomial package
            <https://numpy.org/doc/stable/reference/routines.polynomials.html>`_.
        """
        H.__init__(self, coef, domain, window, symbol)

    def __call__(self, op):
        """
        Thanks to Python :py:meth:`__call__` instance behaves like function.
        If op is a LazyLinOp, return polynomial of op applied to a 1d or
        2d array.
        If op is a P, T, H, La or Le instance, return a poly instance.

        Args:
            op: LazyLinOp, P, T, H, La or Le

        Raises:

        Examples:
            >>> from lazylinop import eye, islazylinop
            >>> from lazylinop.wip.polynomial import lag
            >>> la = lag([1.0, 2.0, 3.0])
            >>> L = eye(3, n=3, k=0)
            >>> islazylinop(la(L))
            True
        """
        if islazylinop(op):
            return lagval(op, self.coef)
        elif isinstance(op, P) or isinstance(op, T) or isinstance(op, H) \
             or isinstance(op, La) or isinstance(op, Le):
            return composition(self, op)
        else:
            raise TypeError('Unexpected op.')


class leg(H):
    """This class implements a Legendre polynomial class derived from
    :py:class:`numpy.polynomial.Legendre` and so relies on NumPy polynomial package
    to manipulate polynomials.

    See :py:mod:`lazylinop.wip.polynomial` for an introduction to implemented
    operations and their basic use.
    """

    def __init__(self, coef, domain=[-1.0, 1.0], window=[-1.0, 1.0],
                 symbol='x'):
        """Init instance of leg.

        Args:
            coef: list
                List of coefficients
            domain: list, optional
                see :py:class:`numpy.polynomial.Legendre`
            window: list, optional
                see :py:class:`numpy.polynomial.Legendre`
            symbol: str, optional
                see :py:class:`numpy.polynomial.Legendre`

        Examples:
            >>> from lazylinop.wip.polynomial import leg
            >>> le = leg([1.0, 2.0, 3.0])

        .. seealso::
            `numpy.polynomial package
            <https://numpy.org/doc/stable/reference/routines.polynomials.html>`_.
        """
        H.__init__(self, coef, domain, window, symbol)

    def __call__(self, op):
        """
        Thanks to Python :py:meth:`__call__` instance behaves like function.
        If op is a LazyLinOp, return polynomial of op applied to a 1d or
        2d array.
        If op is a P, T, H, La or Le instance, return a poly instance.

        Args:
            op: LazyLinOp, P, T, H, La or Le

        Raises:

        Examples:
            >>> from lazylinop import eye, islazylinop
            >>> from lazylinop.wip.polynomial import leg
            >>> le = leg([1.0, 2.0, 3.0])
            >>> L = eye(3, n=3, k=0)
            >>> islazylinop(le(L))
            True
        """
        if islazylinop(op):
            return legval(op, self.coef)
        elif isinstance(op, P) or isinstance(op, T) or isinstance(op, H) \
             or isinstance(op, La) or isinstance(op, Le):
            return composition(self, op)
        else:
            raise TypeError('Unexpected op.')


def chebval(L, c):
    r"""Constructs a :py:class:`.LazyLinOp` Chebysev polynomial ``P(L)`` of
    linear operator ``L``.

    ``P(L)`` is equal to :math:`c_0Id + c_1T_1(L) + \cdots + c_nT_n(L)`.

    The k-th Chebyshev polynomial can be computed by recurrence:

    .. math::

        \begin{eqnarray}
        T_0(L) &=& 1\\
        T_1(L) &=& L\\
        T_{k+1}(L) &=& 2LT_k(L) - T_{k-1}(L)
        \end{eqnarray}

    The Clenshaw's method is used to compute ``P(L) @ X``.

    ``Y = P(L) @ X`` shape is ``(L.shape[0], X.shape[1])``.


    Args:
        L: 2d array
            Linear operator.
        c: 1d array
            List of Chebyshev polynomial(s) coefficients.
            If the size of the 1d array is n + 1 then the largest power of the
            polynomial is n.

    Returns:
        LazyLinOp

    Raises:
        Exception
            Matrix representation of L is not square.
        ValueError
            L @ x does not work because # of columns of L is not equal to the
            # of rows of x.
        ValueError
            List of coefficients has zero size.

    Examples:
        >>> import numpy as np
        >>> from lazylinop import eye
        >>> from lazylinop.wip.polynomial import chebval
        >>> x = np.random.randn(3)
        >>> L = eye(3, n=3, k=0)
        >>> y = chebval(L, [1.0, 2.0, 3.0]) @ x
        >>> np.allclose(6.0 * x, y)
        True

    .. seealso::
        - `Wikipedia <https://en.wikipedia.org/wiki/Chebyshev_polynomials>`_,
        - `Polynomial magic web page
          <https://francisbach.com/chebyshev-polynomials/>`_,
        - `NumPy polynomial class <https://docs.scipy.org/doc//numpy-1.9.3/
          reference/generated/numpy.polynomial.chebyshev.chebval.html>`_.
    """

    if L.shape[0] != L.shape[1]:
        raise Exception("Matrix representation of L is not square.")

    if type(c) is list:
        c = np.asarray(c)

    if c.ndim == 2:
        # Only one polynomial
        c = np.copy(c[:, 0].flatten())
    D = c.shape[0]
    if D == 0:
        raise ValueError("List of coefficients has zero size.")

    def _matmat(L, x, c):
        if L.shape[1] != x.shape[0]:
            raise ValueError("L @ x does not work because # of columns of L is"
                             " not equal to the # of rows of x.")
        if x.ndim == 1:
            is_1d = True
            x = x.reshape(x.shape[0], 1)
        else:
            is_1d = False
        batch_size = x.shape[1]
        output = np.empty((L.shape[0], batch_size),
                          dtype=binary_dtype(c.dtype, x.dtype))
        T0x = np.empty((L.shape[0], batch_size),
                       dtype=binary_dtype(c.dtype, x.dtype))
        T1x = np.empty((L.shape[0], batch_size),
                       dtype=binary_dtype(c.dtype, x.dtype))
        T2x = np.empty((L.shape[0], batch_size),
                       dtype=binary_dtype(c.dtype, x.dtype))
        np.copyto(T0x, x)
        np.copyto(output[:, :], np.multiply(c[0], T0x))
        if D > 1:
            # loop over the coefficients
            for i in range(1, D):
                if i == 1:
                    np.copyto(T1x, L @ x)
                    if c[i] == 0.0:
                        continue
                    else:
                        np.add(output, np.multiply(c[i], T1x), out=output)
                else:
                    np.copyto(T2x, np.subtract(np.multiply(2.0, L @ T1x), T0x))
                    # Recurrence
                    np.copyto(T0x, T1x)
                    np.copyto(T1x, T2x)
                    if c[i] == 0.0:
                        continue
                    else:
                        np.add(output, np.multiply(c[i], T2x), out=output)
        return output.ravel() if is_1d else output

    return LazyLinOp(
        shape=L.shape,
        matmat=lambda x: _matmat(L, x, c),
        rmatmat=lambda x: _matmat(L.T.conj(), x, c)
    )


def chebvalfromroots(L, r):
    r"""Constructs a :py:class:`.LazyLinOp` Chebyshev polynomial
    ``P(L)`` of linear operator ``L`` from the polynomial roots.

    ``P(L)`` is equal to :math:`(L - r_0Id)(L - r_1Id)\cdots (L - r_nId)`.

    ``Y = P(L) @ X`` shape is ``(L.shape[0], X.shape[1])``.

    Args:
        L: 2d array
            Linear operator.
        r: 1d array
            List of Chebyshev polynomial roots.
            If the size of the list is n + 1 then the largest power of the
            polynomial is n.

    Returns:
        LazyLinOp

    Raises:
        ValueError
            List of coefficients has zero size.

    Examples:
        >>> import numpy as np
        >>> from lazylinop import eye
        >>> from lazylinop.wip.polynomial import chebvalfromroots
        >>> x = np.random.randn(3)
        >>> L = eye(3, n=3, k=0)
        >>> y = chebvalfromroots(L, [1.0, 1.0]) @ x
        >>> np.allclose(0.0 * x, y)
        True

    .. seealso::
        - `Wikipedia <https://en.wikipedia.org/wiki/Chebyshev_polynomials>`_,
        - `Polynomial magic web page
          <https://francisbach.com/chebyshev-polynomials/>`_,
        - `NumPy polynomial cheval
          <https://docs.scipy.org/doc//numpy-1.9.3/reference/generated/numpy.polynomial.chebyshev.chebval.html>`_,
        - `NumPy polynomial chebfromroots
          <https://docs.scipy.org/doc//numpy-1.9.3/reference/generated/numpy.polynomial.chebyshev.chebfromroots.html>`_,
        - :py:func:`chebval`.
    """
    if type(r) is list:
        r = np.asarray(r)
    if r.ndim == 2:
        # Only one polynomial
        r = np.copy(r[:, 0].flatten())
    if r.shape[0] == 0:
        raise ValueError("List of roots has zero size.")
    return chebval(L, np.polynomial.chebyshev.chebfromroots(r))


def hermval(L, c):
    r"""Constructs a :py:class:`.LazyLinOp` Hermite (physicist)
    polynomial ``P(L)`` of linear operator ``L``.

    ``P(L)`` is equal to :math:`c_0Id + c_1H_1(L) + \cdots + c_nH_n(L)`.

    The k-th Hermite (physicist) polynomial can be computed by recurrence:

    .. math::

        \begin{eqnarray}
        H_0(L) &=& Id\\
        H_1(L) &=& 2L\\
        H_{k+1}(L) &=& 2LH_k(L) - 2kH_{k-1}(L)
        \end{eqnarray}

    The Clenshaw's method is used to compute ``P(L) @ X``.

    ``Y = P(L) @ X`` shape is ``(L.shape[0], X.shape[1])``.


    Args:
        L: 2d array
            Linear operator.
        c: 1d array
            List of Hermite (physicist) polynomial(s) coefficients.
            If the size of the 1d array is n + 1 then the largest power of the
            polynomial is n.

    Returns:
        LazyLinOp

    Raises:
        Exception
            Matrix representation of L is not square.
        ValueError
            L @ x does not work because # of columns of L is not equal to the
            # of rows of x.
        ValueError
            List of coefficients has zero size.

    Examples:
        >>> import numpy as np
        >>> from lazylinop import eye
        >>> from lazylinop.wip.polynomial import hermval
        >>> x = np.array([1.0, 0.0, 0.0])
        >>> L = eye(3, n=3, k=0)
        >>> y = hermval(L, [1.0, 2.0, 3.0]) @ x
        >>> z = np.polynomial.hermite.hermval(x[0], [1.0, 2.0, 3.0])
        >>> np.allclose(y[0], z)
        True

    .. seealso::
        - `Wikipedia <https://en.wikipedia.org/wiki/Hermite_polynomials>`_,
        - `NumPy polynomial class <https://docs.scipy.org/doc//numpy-1.9.3/
          reference/generated/numpy.polynomial.hermite.hermval.html>`_.
    """

    if L.shape[0] != L.shape[1]:
        raise Exception("Matrix representation of L is not square.")

    if type(c) is list:
        c = np.asarray(c)

    if c.ndim == 2:
        # Only one polynomial
        c = np.copy(c[:, 0].flatten())
    D = c.shape[0]
    if D == 0:
        raise ValueError("List of coefficients has zero size.")

    def _matmat(L, x, c):
        if L.shape[1] != x.shape[0]:
            raise ValueError("L @ x does not work because # of columns of L is"
                             " not equal to the # of rows of x.")
        if x.ndim == 1:
            is_1d = True
            x = x.reshape(x.shape[0], 1)
        else:
            is_1d = False
        batch_size = x.shape[1]
        output = np.empty((L.shape[0], batch_size),
                          dtype=binary_dtype(c.dtype, x.dtype))
        H0x = np.empty((L.shape[0], batch_size),
                       dtype=binary_dtype(c.dtype, x.dtype))
        H1x = np.empty((L.shape[0], batch_size),
                       dtype=binary_dtype(c.dtype, x.dtype))
        H2x = np.empty((L.shape[0], batch_size),
                       dtype=binary_dtype(c.dtype, x.dtype))
        np.copyto(H0x, x)
        np.copyto(output[:, :], np.multiply(c[0], H0x))
        if D > 1:
            # loop over the coefficients
            for i in range(1, D):
                if i == 1:
                    np.copyto(H1x, np.multiply(2.0, L @ x))
                    if c[i] == 0.0:
                        continue
                    else:
                        np.add(output, np.multiply(c[i], H1x), out=output)
                else:
                    np.copyto(H2x, np.subtract(np.multiply(2.0, L @ H1x), np.multiply(2 * (i - 1), H0x)))
                    # Recurrence
                    np.copyto(H0x, H1x)
                    np.copyto(H1x, H2x)
                    if c[i] == 0.0:
                        continue
                    else:
                        np.add(output, np.multiply(c[i], H2x), out=output)
        return output.ravel() if is_1d else output

    return LazyLinOp(
        shape=L.shape,
        matmat=lambda x: _matmat(L, x, c),
        rmatmat=lambda x: _matmat(L.T.conj(), x, c)
    )


def lagval(L, c):
    r"""Constructs a :py:class:`.LazyLinOp` Laguerre polynomial ``P(L)``
    of linear operator ``L``.

    ``P(L)`` is equal to :math:`c_0Id + c_1L_{a,1}(L) + \cdots + c_nL_{a,n}(L)`.

    The k-th Laguerre polynomial can be computed by recurrence:

    .. math::

        \begin{eqnarray}
        L_{a,0}(L) &=& Id\\
        L_{a,1}(L) &=& Id - L\\
        L_{a,k+1}(L) &=& \frac{(2k + 1 - L)L_{a,k}(L) - kL_{a,k-1}(L)}{k + 1}
        \end{eqnarray}

    The Clenshaw's method is used to compute ``P(L) @ X``.

    ``Y = P(L) @ X`` shape is ``(L.shape[0], X.shape[1])``.


    Args:
        L: 2d array
            Linear operator.
        c: 1d array
            List of Laguerre polynomial(s) coefficients.
            If the size of the 1d array is n + 1 then the largest power
            of the polynomial is n.

    Returns:
        LazyLinOp

    Raises:
        Exception
            Matrix representation of L is not square.
        ValueError
            L @ x does not work because # of columns of L is not equal to the
            # of rows of x.
        ValueError
            List of coefficients has zero size.

    Examples:
        >>> import numpy as np
        >>> from lazylinop import eye
        >>> from lazylinop.wip.polynomial import lagval
        >>> x = np.array([1.0, 0.0, 0.0])
        >>> L = eye(3, n=3, k=0)
        >>> y = lagval(L, [1.0, 2.0, 3.0]) @ x
        >>> z = np.polynomial.laguerre.lagval(x[0], [1.0, 2.0, 3.0])
        >>> np.allclose(y[0], z)
        True

    .. seealso::
        - `Wikipedia <https://en.wikipedia.org/wiki/Laguerre_polynomials>`_,
        - `NumPy polynomial class <https://docs.scipy.org/doc//numpy-1.9.3/
          reference/generated/numpy.polynomial.laguerre.lagval.html>`_.
    """

    if L.shape[0] != L.shape[1]:
        raise Exception("Matrix representation of L is not square.")

    if type(c) is list:
        c = np.asarray(c)

    if c.ndim == 2:
        # Only one polynomial
        c = np.copy(c[:, 0].flatten())
    D = c.shape[0]
    if D == 0:
        raise ValueError("List of coefficients has zero size.")

    def _matmat(L, x, c):
        if L.shape[1] != x.shape[0]:
            raise ValueError("L @ x does not work because # of columns of L is"
                             " not equal to the # of rows of x.")
        if x.ndim == 1:
            is_1d = True
            x = x.reshape(x.shape[0], 1)
        else:
            is_1d = False
        batch_size = x.shape[1]
        output = np.empty((L.shape[0], batch_size),
                          dtype=binary_dtype(c.dtype, x.dtype))
        La0x = np.empty((L.shape[0], batch_size),
                       dtype=binary_dtype(c.dtype, x.dtype))
        La1x = np.empty((L.shape[0], batch_size),
                       dtype=binary_dtype(c.dtype, x.dtype))
        La2x = np.empty((L.shape[0], batch_size),
                       dtype=binary_dtype(c.dtype, x.dtype))
        np.copyto(La0x, x)
        np.copyto(output[:, :], np.multiply(c[0], La0x))
        if D > 1:
            # loop over the coefficients
            for i in range(1, D):
                if i == 1:
                    np.copyto(La1x, np.subtract(x, L @ x))
                    if c[i] == 0.0:
                        continue
                    else:
                        np.add(output, np.multiply(c[i], La1x), out=output)
                else:
                    np.copyto(La2x, np.divide(
                        np.subtract(
                            np.subtract(
                                np.multiply(2.0 * (i - 1) + 1.0, La1x),
                                L @ La1x),
                            np.multiply(i - 1, La0x)), i))
                    # Recurrence
                    np.copyto(La0x, La1x)
                    np.copyto(La1x, La2x)
                    if c[i] == 0.0:
                        continue
                    else:
                        np.add(output, np.multiply(c[i], La2x), out=output)
        return output.ravel() if is_1d else output

    return LazyLinOp(
        shape=L.shape,
        matmat=lambda x: _matmat(L, x, c),
        rmatmat=lambda x: _matmat(L.T.conj(), x, c)
    )


def legval(L, c):
    r"""Constructs a :py:class:`.LazyLinOp` Legendre polynomial ``P(L)``
    of linear operator ``L``.

    ``P(L)`` is equal to :math:`c_0Id + c_1L_{e,1}(L) + \cdots + c_nL_{e,n}(L)`.

    The k-th Legendre polynomial can be computed by recurrence:

    .. math::

        \begin{eqnarray}
        L_{e,0}(L) &=& Id\\
        L_{e,1}(L) &=& L\\
        L_{e,k+1}(L) &=& \frac{(2k + 1)LL_{e,k}(L) - kL_{e,k-1}(L)}{k + 1}
        \end{eqnarray}

    The Clenshaw's method is used to compute ``P(L) @ X``.

    ``Y = P(L) @ X`` shape is ``(L.shape[0], X.shape[1])``.


    Args:
        L: 2d array
            Linear operator.
        c: 1d array
            List of Legendre polynomial(s) coefficients.
            If the size of the 1d array is n + 1 then the largest power
            of the polynomial is n.

    Returns:
        LazyLinOp

    Raises:
        Exception
            Matrix representation of L is not square.
        ValueError
            L @ x does not work because # of columns of L is not equal to the
            # of rows of x.
        ValueError
            List of coefficients has zero size.

    Examples:
        >>> import numpy as np
        >>> from lazylinop import eye
        >>> from lazylinop.wip.polynomial import legval
        >>> x = np.random.randn(3)
        >>> L = eye(3, n=3, k=0)
        >>> y = legval(L, [1.0, 2.0, 3.0]) @ x
        >>> np.allclose(6.0 * x, y)
        True

    .. seealso::
        - `Wikipedia <https://en.wikipedia.org/wiki/Legendre_polynomials>`_,
        - `NumPy polynomial class <https://docs.scipy.org/doc//numpy-1.9.3/
          reference/generated/numpy.polynomial.legendre.legval.html>`_.
    """

    if L.shape[0] != L.shape[1]:
        raise Exception("Matrix representation of L is not square.")

    if type(c) is list:
        c = np.asarray(c)

    if c.ndim == 2:
        # Only one polynomial
        c = np.copy(c[:, 0].flatten())
    D = c.shape[0]
    if D == 0:
        raise ValueError("List of coefficients has zero size.")

    def _matmat(L, x, c):
        if L.shape[1] != x.shape[0]:
            raise ValueError("L @ x does not work because # of columns of L is"
                             " not equal to the # of rows of x.")
        if x.ndim == 1:
            is_1d = True
            x = x.reshape(x.shape[0], 1)
        else:
            is_1d = False
        batch_size = x.shape[1]
        output = np.empty((L.shape[0], batch_size),
                          dtype=binary_dtype(c.dtype, x.dtype))
        Le0x = np.empty((L.shape[0], batch_size),
                       dtype=binary_dtype(c.dtype, x.dtype))
        Le1x = np.empty((L.shape[0], batch_size),
                       dtype=binary_dtype(c.dtype, x.dtype))
        Le2x = np.empty((L.shape[0], batch_size),
                       dtype=binary_dtype(c.dtype, x.dtype))
        np.copyto(Le0x, x)
        np.copyto(output[:, :], np.multiply(c[0], Le0x))
        if D > 1:
            # loop over the coefficients
            for i in range(1, D):
                if i == 1:
                    np.copyto(Le1x, L @ x)
                    if c[i] == 0.0:
                        continue
                    else:
                        np.add(output, np.multiply(c[i], Le1x), out=output)
                else:
                    np.copyto(Le2x, np.divide(
                        np.subtract(
                            np.multiply(2.0 * (i - 1) + 1.0, L @ Le1x),
                            np.multiply(i - 1, Le0x)), i))
                    # Recurrence
                    np.copyto(Le0x, Le1x)
                    np.copyto(Le1x, Le2x)
                    if c[i] == 0.0:
                        continue
                    else:
                        np.add(output, np.multiply(c[i], Le2x), out=output)
        return output.ravel() if is_1d else output

    return LazyLinOp(
        shape=L.shape,
        matmat=lambda x: _matmat(L, x, c),
        rmatmat=lambda x: _matmat(L.T.conj(), x, c)
    )


def polyval(L, c):
    r"""Constructs a :py:class:`.LazyLinOp` polynomial ``P(L)`` of linear
    operator ``L``.

    ``P(L)`` is equal to :math:`c_0Id + c_1L^1 + \cdots + c_nL^n`.

    ``Y = P(L) @ X`` shape is ``(L.shape[0], X.shape[1])``.

    Args:
        L: 2d array
            Linear operator.
        c: 1d array
            List of polynomial coefficients.
            If the size of the 1d array is n + 1 then the largest power of the
            polynomial is n.
            If the array is 2d consider only the first column/polynomial.

    Returns:
        LazyLinOp

    Raises:
        Exception
            Matrix representation of L is not square.
        ValueError
            L @ x does not work because # of columns of L is not equal to the
            # of rows of x.
        ValueError
            List of coefficients has zero size.

    Examples:
        >>> import numpy as np
        >>> from lazylinop import eye
        >>> from lazylinop.wip.polynomial import polyval
        >>> x = np.random.randn(3)
        >>> L = eye(3, n=3, k=0)
        >>> y = polyval(L, [1.0, 2.0, 3.0]) @ x
        >>> np.allclose(6.0 * x, y)
        True

    .. seealso::
        - `NumPy polynomial class <https://docs.scipy.org/doc//numpy-1.9.3/
          reference/generated/numpy.polynomial.polynomial.polyval.html>`_.
        - :py:func:`polyvalfromroots`.
    """

    if L.shape[0] != L.shape[1]:
        raise Exception("Matrix representation of L is not square.")

    if type(c) is list:
        c = np.asarray(c)

    if c.ndim == 2:
        # Only one polynomial
        c = np.copy(c[:, 0].flatten())
    D = c.shape[0]
    if D == 0:
        raise ValueError("List of coefficients has zero size.")

    def _matmat(L, x, c):
        if L.shape[1] != x.shape[0]:
            raise ValueError("L @ x does not work because # of columns of L is"
                             " not equal to the # of rows of x.")
        # x can't be a LazyLinOp here because it's handle before in
        # LazyLinOp.__matmul__
        if x.ndim == 1:
            is_1d = True
            x = x.reshape(x.shape[0], 1)
        else:
            is_1d = False
        output = np.empty((L.shape[0], x.shape[1]),
                          dtype=binary_dtype(c.dtype, x.dtype))
        Lx = np.empty((L.shape[0], x.shape[1]), dtype=binary_dtype(c.dtype,
                                                                   x.dtype))
        output[:, :] = np.multiply(c[0], x)
        if D > 1:
            # Loop over the coefficients
            for i in range(1, D):
                if i == 1:
                    np.copyto(Lx, L @ x)
                else:
                    np.copyto(Lx, L @ Lx)
                if c[i] == 0.0:
                    continue
                else:
                    np.add(output[:, :], np.multiply(c[i], Lx), out=output)
        return output.ravel() if is_1d else output

    return LazyLinOp(
        shape=L.shape,
        matmat=lambda x: _matmat(L, x, c),
        rmatmat=lambda x: _matmat(L.T.conj(), x, c)
    )


def polyvalfromroots(L, r):
    r"""Constructs a :py:class:`.LazyLinOp` polynomial
    ``P(L)`` of linear operator ``L`` from the polynomial roots.

    ``P(L)`` is equal to :math:`(L - r_0Id)(L - r_1)\cdots (L - r_nId)`.

    ``Y = P(L) @ X`` shape is ``(L.shape[0], X.shape[1])``.

    Args:
        L: 2d array
            Linear operator.
        r: 1d array
            List of polynomial roots.
            If the size of the 1d array is n + 1 then the largest power of the
            polynomial is n.
            If the array is 2d, the function considers only the first
            column/polynomial.

    Returns:
        LazyLinOp

    Raises:
        Exception
            Matrix representation of L is not square.
        ValueError
            L @ x does not work because # of columns of L is not equal to the #
            of rows of x.
        ValueError
            List of roots has zero size.

    Examples:
        >>> import numpy as np
        >>> from lazylinop import eye
        >>> from lazylinop.wip.polynomial import polyvalfromroots
        >>> x = np.random.randn(3)
        >>> L = eye(3, n=3, k=0)
        >>> y = polyvalfromroots(L, [1.0, 1.0, 1.0]) @ x
        >>> np.allclose(0.0 * x, y)
        True

    .. seealso::
        - `NumPy polynomial class <https://docs.scipy.org/doc/
          numpy-1.9.3/reference/generated/numpy.polynomial.polynomial.
          polyval.html>`_.
        - :py:func:`polyval`.
    """

    if L.shape[0] != L.shape[1]:
        raise Exception("Matrix representation of L is not square.")

    if type(r) is list:
        r = np.asarray(r)

    if r.ndim == 2:
        # Only one polynomial
        r = np.copy(r[:, 0].flatten())
    R = r.shape[0]
    if R == 0:
        raise ValueError("List of roots has zero size.")

    def _matmat(r, L, x):
        if L.shape[1] != x.shape[0]:
            raise ValueError("L @ x does not work because # of columns of L is"
                             " not equal to the # of rows of x.")
        if x.ndim == 1:
            is_1d = True
            x = x.reshape(x.shape[0], 1)
        else:
            is_1d = False
        output = np.empty((L.shape[0], x.shape[1]),
                          dtype=binary_dtype(r.dtype,
                                             x.dtype))
        Lx = np.empty((L.shape[0], x.shape[1]), dtype=binary_dtype(r.dtype,
                                                                   x.dtype))
        if r[R - 1] == 0.0:
            np.copyto(Lx, L @ x)
        else:
            np.copyto(Lx, np.subtract(L @ x, np.multiply(r[R - 1], x)))
        if R > 1:
            for i in range(1, R):
                if r[R - 1 - i] == 0.0:
                    np.copyto(Lx, L @ Lx)
                else:
                    np.copyto(Lx, np.subtract(L @ Lx, np.multiply(r[R - 1 - i],
                                                                  Lx)))
        np.copyto(output[:, :], Lx)
        return output.ravel() if is_1d else output

    return LazyLinOp(
        shape=L.shape,
        matmat=lambda x: _matmat(r, L, x),
        rmatmat=lambda x: _matmat(r, L.T.conj(), x)
    )


def power(L, n):
    r"""Constructs the n-th power :math:`L^n` of linear operator ``L``.

    .. note::
        It is equivalent to create a :py:class:`poly` instance such that
        only n-th coefficient is equal to one while the others are equal
        to zero.

    Args:
        L: 2d array
            Linear operator (e.g. a :py:class:`.LazyLinOp`).
        n: int
            Raise the linear operator to degree n.
            If n is zero, return identity matrix.

    Returns:
        LazyLinOp :math:`L^n`.

    Raises:
        ValueError
            n must be > 0.
        Exception
            Matrix representation of L is not square.

    Examples:
        >>> import numpy as np
        >>> from lazylinop import eye
        >>> from lazylinop.wip.polynomial import power
        >>> L = power(eye(3, n=3, k=0), 3)
        >>> x = np.full(3, 1.0)
        >>> np.allclose(L @ x, x)
        True
        >>> L = power(eye(3, n=3, k=1), 3)
        >>> # Note that L is in fact zero (nilpotent matrix)
        >>> x = np.full(3, 1.0)
        >>> np.allclose(L @ x, np.zeros(3, dtype=np.float_))
        True

    .. seealso::
        `NumPy power function
        <https://numpy.org/doc/stable/reference/generated/numpy.power.html>`_.
    """

    if n < 0:
        raise ValueError("n must be > 0.")

    if L.shape[0] != L.shape[1]:
        raise Exception("Matrix representation of L is not square.")

    if n == 0:
        from lazylinop import eye
        return eye(L.shape[0], n=L.shape[1], k=0)

    def _matmat(L, n, x):
        output = L @ x
        if n > 1:
            for n in range(1, n):
                np.copyto(output, L @ output)
        return output

    return LazyLinOp(
        shape=L.shape,
        matmat=lambda x: _matmat(L, n, x),
        rmatmat=lambda x: _matmat(L.T.conj(), n, x)
    )


if __name__ == '__main__':
    import doctest
    doctest.testmod()
