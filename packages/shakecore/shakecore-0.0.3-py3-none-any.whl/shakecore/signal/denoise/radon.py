from shakecore.transform import radon_forward, radon_inverse


def radon_cpu(data, filter_matrix, dt, dx, p_vec, kind, method, options):
    """
    Compute radon transform of a 2D array.

    Parameters
    ----------
    data : ndarray
        2D array of shape (nx, nt) containing the data.
    filter_matrix : ndarray
        2D array of shape (nx, nt) containing the filter matrix.
    dt : float
        Sampling rate in seconds.
    dx : float
        Sampling rate in meters.
    p_vec : ndarray
        1D array of shape (np,) containing the p vector.
    kind : str
        Radon transform type. Can be 'linear', 'parabolic', or 'hyperbolic'.
    method : str
        Inversion method. Can be 'CG' or 'LSQR'.
    options : dict
        Dictionary of options for the inversion method.

    Returns
    -------
    filtered_data : ndarray
        2D array of shape (nx, nt) containing the filtered data.
    """

    # compute the radon transform of the data
    model = radon_inverse(data, dt, dx, p_vec, kind, method, options)

    # filter the model
    model_filter = model * filter_matrix

    # transform the model back to the data domain
    x_num = data.shape[0]
    filtered_data = radon_forward(model_filter, dt, dx, x_num, p_vec, kind)

    return filtered_data
