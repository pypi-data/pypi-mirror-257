"""Generate random unitary."""
import numpy as np


def random_unitary(dim: list[int] | int, is_real: bool = False) -> np.ndarray:
    """Generate a random unitary or orthogonal matrix :cite:`Ozols_2009_RandU`.

    Calculates a random unitary matrix (if :code:`is_real = False`) or a random real orthogonal
    matrix (if :code:`is_real = True`), uniformly distributed according to the Haar measure.

    Examples
    ==========

    We may generate a random unitary matrix. Here is an example of how we may be able to generate a
    random :math:`2`-dimensional random unitary matrix with complex entries.

    >>> from toqito.rand import random_unitary
    >>> complex_dm = random_unitary(2)
    >>> complex_dm # doctest: +SKIP
    [[0.40563696+0.18092721j, 0.00066868+0.89594841j],
     [0.4237286 +0.78941628j, 0.27157521-0.35145826j]]

    .. note::
        We use `doctest` to check if our examples are working as expected. ` # doctest: +SKIP` is used here
        to skip comparing the expected output to the calculated output because this function is supposed to
        generate a random matrix.

    We can verify that this is in fact a valid unitary matrix using the :code:`is_unitary` function
    from :code:`toqito` as follows

    >>> from toqito.matrix_props import is_unitary
    >>> is_unitary(complex_dm)
    True

    We can also generate random unitary matrices that are real-valued as follows.

    >>> from toqito.rand import random_unitary
    >>> real_dm = random_unitary(2, True)
    >>> real_dm # doctest: +SKIP
    [[ 0.01972681, -0.99980541],
     [ 0.99980541,  0.01972681]]

    .. note::
        We use `doctest` to check if our examples are working as expected. ` # doctest: +SKIP` is used here
        to skip comparing the expected output to the calculated output because this function is supposed to
        generate a random matrix.

    Again, verifying that this is a valid unitary matrix can be done as follows.

    >>> from toqito.matrix_props import is_unitary
    >>> is_unitary(real_dm)
    True

    We may also generate unitaries such that the dimension argument provided is a :code:`list` as
    opposed to an :code:`int`. Here is an example of a random unitary matrix of dimension :math:`4`.

    >>> from toqito.rand import random_unitary
    >>> mat = random_unitary([4, 4], True)
    >>> mat # doctest: +SKIP
    [[ 0.48996358, -0.20978392,  0.56678587, -0.62823576],
     [ 0.62909119, -0.35852051, -0.68961425, -0.01181086],
     [ 0.38311399,  0.90865415, -0.1209574 , -0.11375677],
     [ 0.46626562, -0.04244265,  0.4342295 ,  0.76957113]]

    As before, we can verify that this matrix generated is a valid unitary matrix.

    >>> from toqito.matrix_props import is_unitary
    >>> is_unitary(mat)
    True

    References
    ==========
    .. bibliography::
        :filter: docname in docnames


    :param dim: The number of rows (and columns) of the unitary matrix.
    :param is_real: Boolean denoting whether the returned matrix has real
                    entries or not. Default is :code:`False`.
    :return: A :code:`dim`-by-:code:`dim` random unitary matrix.

    """
    if isinstance(dim, int):
        dim = [dim, dim]

    if dim[0] != dim[1]:
        raise ValueError("Unitary matrix must be square.")

    # Construct the Ginibre ensemble.
    gin = np.random.rand(dim[0], dim[1])

    if not is_real:
        gin = gin + 1j * np.random.rand(dim[0], dim[1])

    # QR decomposition of the Ginibre ensemble.
    q_mat, r_mat = np.linalg.qr(gin)

    # Compute U from QR decomposition.
    r_mat = np.sign(np.diag(r_mat))

    # Protect against potentially zero diagonal entries.
    r_mat[r_mat == 0] = 1

    return q_mat @ np.diag(r_mat)
