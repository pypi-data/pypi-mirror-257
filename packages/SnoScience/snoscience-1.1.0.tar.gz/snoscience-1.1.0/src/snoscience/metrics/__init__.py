"""
Supported metrics.
"""

# Packages from requirements.
from numpy import round as numpy_round
from numpy import ndarray, count_nonzero

# Source package.
from .._loss import mse


def calculate_mse(calc: ndarray, true: ndarray) -> ndarray:
    """
    Calculate the mean squared error per output from the given arrays.

    Parameters
    ----------
    calc: ndarray
        Array containing all the calculated or predicted values.
    true: ndarray
        Array containing all the true or expected values.

    Returns
    -------
    ndarray:
        Mean squared error per output.
    """
    return numpy_round(mse(calc=calc, true=true), decimals=4)


def calculate_accuracy(calc: ndarray, true: ndarray) -> float:
    """
    Calculate the accuracy from the given arrays.

    Parameters
    ----------
    calc: ndarray
        Array containing all the calculated or predicted values.
    true: ndarray
        Array containing all the true or expected values.

    Returns
    -------
    float:
        Percentage of correct class predictions.
    """
    # Correctly classified rows consist of zeros.
    misses = numpy_round(true - calc, decimals=1)
    # For multiclass count misses per row first (it will be 2 per miss).
    misses = count_nonzero(misses, axis=1)
    # Then sum those non-zero elements to get number of misses.
    misses = count_nonzero(misses)

    accuracy = (1 - (misses / len(true))) * 100
    return float(numpy_round(accuracy, decimals=2))
