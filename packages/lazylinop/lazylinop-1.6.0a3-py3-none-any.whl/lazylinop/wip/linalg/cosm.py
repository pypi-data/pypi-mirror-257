from lazylinop import islazylinop, LazyLinOp
import scipy as sp
import numpy as np


def cosm(L, scale: float=1.0, nmax: int=8, backend: str='scipy'):
    """Constructs a cosinus of linear operator L as a lazy linear operator C(L).
    It uses the equation expm(i * scale * L) = cos(scale * L) + i * sin(scale * L)
    where i^2 = -1 and returns real part.
    Of note, it is only an approximation (see nmax argument).

    Args:
        L: 2d array
        Linear operator.
        scale: float, optional
        Scale factor cosm(scale * L) (default is 1).
        nmax: int, optional
        Stop the serie expansion after nmax (default is 8).
        backend: str, optional
        It can be 'scipy' (default) to use scipy.linalg.cosm function.
        nmax parameter is useless if backend is 'scipy'.
        It can be 'serie' to use a serie expansion of cosm(scale * L).

    Returns:
        LazyLinOp

    Raises:
        ValueError
            L @ x does not work because # of columns of L is not equal to the # of rows of x.
        ValueError
            backend value is either 'scipy' or 'serie'.
        ValueError
            If L is a 2d array, backend must be 'scipy'.

    Examples:
        >>> import numpy as np
        >>> import scipy as sp
        >>> from lazylinop import eye
        >>> from lazylinop.wip.linear_algebra import cosm
        >>> scale = 0.01
        >>> coefficients = np.array([1.0, scale, 0.5 * scale ** 2])
        >>> N = 10
        >>> L = np.eye(N, n=N, k=0)
        >>> E1 = cosm(L, scale=scale, nmax=4)
        >>> E2 = sp.linalg.cosm(scale * L)
        >>> np.allclose(E1.toarray(), E2)
        >>> E3 = eye(N, n=N, k=0)
        >>> X = np.random.rand(N, 2 * N)
        >>> np.allclose(E2 @ X, E3 @ X)

    References:
        See also `scipy.linalg.cosm function <https://docs.scipy.org/doc/scipy/reference/generated/scipy.linalg.cosm.html>`_.
        See also :py:func:`expm`.
        See also :py:func:`lazylinop.wip.polynomial.polyval`.
    """
    if backend == 'scipy':
        if islazylinop(L):#type(L) is np.ndarray:
            raise ValueError("If L is a 2d array, backend must be 'scipy'.")
        return LazyLinOp(
            shape=L.shape,
            matmat=lambda X: sp.linalg.cosm(scale * L) @ X,
            rmatmat=lambda X: sp.linalg.cosm(scale * L.T.conj()) @ X
        )
    elif backend == 'serie':
        from lazylinop.wip.polynomial import polyval
        coefficients = np.empty(nmax + 1, dtype=np.float64)
        factor = 1.0
        sign = 1
        for i in range(nmax + 1):
            if (i % 2) == 0:
                coefficients[i] = sign * factor
                sign *= -1
            else:
                coefficients[i] = 0.0
            factor *= scale / (i + 1)
        return polyval(L, coefficients)
    else:
        raise ValueError("backend value is either 'scipy' or 'serie'.")
