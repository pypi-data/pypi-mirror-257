"""Maximally mixed state."""
import numpy as np
from scipy import sparse


def max_mixed(dim: int, is_sparse: bool = False) -> [np.ndarray, sparse.dia_matrix]:
    r"""Produce the maximally mixed state :cite:`Aaronson_2018_MaxMixed`.

    Produces the maximally mixed state on of :code:`dim` dimensions. The maximally mixed state is defined as

    .. math::
        \omega = \frac{1}{d} \begin{pmatrix}
                        1 & 0 & \ldots & 0 \\
                        0 & 1 & \ldots & 0 \\
                        \vdots & \vdots & \ddots & \vdots \\
                        0 & 0 & \ldots & 1
                    \end{pmatrix},

    or equivalently, it is defined as

    .. math::
        \omega = \frac{\mathbb{I}}{\text{dim}(\mathcal{X})}

    for some complex Euclidean space :math:`\mathcal{X}`. The maximally mixed state is sometimes also referred to as the
    tracial state.

    The maximally mixed state is returned as a sparse matrix if :code:`is_sparse = True` and is full if :code:`is_sparse
    = False`.

    Examples
    ==========

    Using :code:`toqito`, we can generate the :math:`2`-dimensional maximally mixed state

    .. math::
        \omega_2 = \frac{1}{2}
        \begin{pmatrix}
            1 & 0 \\
            0 & 1
        \end{pmatrix}

    as follows.

    >>> from toqito.states import max_mixed
    >>> max_mixed(2, is_sparse=False)
    array([[0.5, 0. ],
           [0. , 0.5]])


    One may also generate a maximally mixed state returned as a sparse matrix

    >>> from toqito.states import max_mixed
    >>> max_mixed(2, is_sparse=True) # doctest: +ELLIPSIS, +NORMALIZE_WHITESPACE
    <2x2 sparse matrix of type '<class 'numpy.float64'>'
        with 2 stored elements (1 diagonals) in DIAgonal format>

    .. note::
        We use `#doctest` to verify our examples work as expected.

        `# doctest: +ELLIPSIS, +NORMALIZE_WHITESPACE` is used here to make sure doctest matches the
        calculated output to be close to the expected output instead of making sure both match exactly.

    References
    ==========
    .. bibliography::
        :filter: docname in docnames


    :param dim: Dimension of the entangled state.
    :param is_sparse: `True` if vector is spare and `False` otherwise.
    :return: The maximally mixed state of dimension `dim`.

    """
    if is_sparse:
        return 1 / dim * sparse.eye(dim)
    return 1 / dim * np.eye(dim)
