from collections import namedtuple
import numba
import numpy as np
from .utils import CACHE

Optim = namedtuple('Optim', 'preinit init update metric')

@numba.njit(cache=CACHE)
def compute_update(level, grp, X, Xi_star, plot_sizes, c, betas=None, betas_inv=None):
    """
    Compute the update to the information matrix after making
    a single coordinate adjustment. This update is expressed
    in the form: :math:`M^* = M + U^T D U`. D is a diagonal
    matrix in this case.

    .. note::
        This function is Numba accelerated

    Parameters
    ----------
    level : int
        The level at which to make the adjustment
    grp : int
        The group to update (relative to the level)
    X : np.array(2d)
        The model matrix of the current design
    Xi_star : np.array(2d)
        The updated part of the model matrix (full rows where atleast one factor changed)
    plot_sizes : np.array(1d)
        The plot sizes of the generalized split-plot
    c : np.array(1d)
        The c-coefficients of the inverse observation variance matrix
    betas : np.array(1d)
        The beta values, precomputed, or None
    betas_inv : np.array(1d)
        The inverse beta values, precomputed, or None

    Returns
    -------
    U : np.array(2d)
        The U matrix of the update formula
    D : np.array(1d)
        The diagonal D matrix of the update formula.
        It is returned as a 1D array
    """
    # Extract state
    if betas is None:
        betas = np.cumprod(np.concatenate((np.array([1]), plot_sizes)))
    if betas_inv is None:
        betas_inv = np.cumsum(np.concatenate((np.array([0], dtype=np.float64), 1/betas[1:])))

    # First runs
    jmp = betas[level]
    runs = slice(grp*jmp, (grp+1)*jmp)
    
    # Extract level-section
    Xi = X[runs]

    # Initialize U and D
    star_offset = int(Xi.shape[0] * (1 + betas_inv[level])) + (plot_sizes.size - level - 1)
    U = np.zeros((2*star_offset, Xi.shape[1]))
    D = np.zeros(2*star_offset)

    # Store level-0 results
    U[:Xi.shape[0]] = Xi
    U[star_offset: star_offset + Xi.shape[0]] = Xi_star
    D[:Xi.shape[0]] = -np.ones(Xi.shape[0])
    D[star_offset: star_offset + Xi.shape[0]] = np.ones(Xi.shape[0])
    co = Xi.shape[0]

    # Loop before (= summations)
    if level != 0:
        # Reshape for summation
        Xi = Xi.reshape((-1, plot_sizes[0], Xi.shape[1]))
        Xi_star = Xi_star.reshape((-1, plot_sizes[0], Xi_star.shape[1]))
        for i in range(1, level):
            # Sum all smaller sections
            Xi_sum = np.sum(Xi, axis=1)
            Xi_star_sum = np.sum(Xi_star, axis=1)
            
            # Store entire matrix
            coe = co + Xi_sum.shape[0]
            U[co:coe] = Xi_sum
            U[star_offset+co: star_offset+coe] = Xi_star_sum
            D[co:coe] = -c[i]
            D[star_offset+co: star_offset+coe] = c[i]
            co = coe

            # Reshape for next iteration
            Xi = Xi_sum.reshape((-1, plot_sizes[i], Xi_sum.shape[1]))
            Xi_star = Xi_star_sum.reshape((-1, plot_sizes[i], Xi_star_sum.shape[1]))

        # Sum level-section
        Xi = np.sum(Xi, axis=1)
        Xi_star = np.sum(Xi_star, axis=1)

        # Store results
        U[co] = Xi
        U[star_offset+co] = Xi_star
        D[co] = -c[level]
        D[star_offset+co] = c[level]
        co += 1

    # Flatten the arrays for the next step
    Xi = Xi.flatten()
    Xi_star = Xi_star.flatten()

    # Loop after (= updates)
    for j in range(level, plot_sizes.size - 1):
        # Adjust group one level higher
        jmp *= plot_sizes[j]
        grp = grp // plot_sizes[j]

        # Compute section sum
        r = np.sum(X[grp*jmp: (grp+1)*jmp], axis=0)
        r_star = r - Xi + Xi_star

        # Store the results
        U[co] = r
        U[star_offset+co] = r_star
        D[co] = -c[j+1]
        D[star_offset+co] = c[j+1]
        co += 1

        # Set variables for next iteration
        Xi = r
        Xi_star = r_star

    # Return values
    return U, D

@numba.njit(cache=CACHE)
def det_update(U, D, Minv):
    """
    Compute the determinant adjustment as a factor.
    In other words: :math:`|M^*|=\\alpha*|M|`. The new
    information matrix originates from the following update
    formula: :math:`M^* = M + U^T D U`.

    The actual update is described as

    .. math::

        \\alpha = |D| |P| = |D| |D^{-1} + U M^{-1} U.T|

    .. note::
        This function is Numba accelerated

    Parameters
    ----------
    U : np.array(2d)
        The U matrix in the update
    D : np.array(1d)
        The diagonal D matrix in the update. It is
        inserted as a 1d array representing the diagonal.
    Minv : np.array(2d)
        The current inverse of the information matrix.

    Returns
    -------
    alpha : float
        The update factor
    P : np.array(2d)
        The P matrix of the update
    """
    # Compute P
    P = U @ Minv @ U.T
    for i in range(P.shape[0]):
        P[i, i] += 1/D[i]

    # Compute determinant update
    return np.linalg.det(P) * np.prod(D), P

@numba.njit(cache=CACHE)
def inv_update(U, D, Minv, P):
    """
    Compute the update of the inverse of the information matrix.
    In other words: :math:`M^{*-1} = M^{-1} - M_{up}`. The new
    information matrix originates from the following update
    formula: :math:`M^* = M + U^T D U`.

    The actual update is described as

    .. math::

        M_{up} = M^{-1} U^T P^{-1} U M^{-1}

    .. math::
        P = D^{-1} + U M^{-1} U.T

    .. note::
        This function is Numba accelerated

    Parameters
    ----------
    U : np.array(2d)
        The U matrix in the update
    D : np.array(1d)
        The diagonal D matrix in the update. It is
        inserted as a 1d array representing the diagonal.
    Minv : np.array(2d)
        The current inverse of the information matrix.
    P : np.array(1d)
        The P matrix if already pre-computed.

    Returns
    -------
    Mup : np.array(2d)
        The update to the inverse matrix.
    """
    return (Minv @ U.T) @ np.linalg.solve(P, U @ Minv)

@numba.njit(cache=CACHE)
def inv_update_no_P(U, D, Minv):
    """
    Same function as :py:func:`inv_update`, except it computes the
    P matrix beforehand.

    .. note::
        This function is Numba accelerated
    """
    P = U @ Minv @ U.T
    for i in range(P.shape[0]):
        P[i, i] += 1/D[i]
    return inv_update(U, D, Minv, P)

