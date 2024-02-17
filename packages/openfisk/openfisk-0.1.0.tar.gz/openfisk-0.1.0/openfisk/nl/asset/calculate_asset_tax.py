"""Functions to calculate the tax on the return of an asset based on the 2024 taxation model."""

import numpy as np


class NegativeValueError(ValueError):
    """Exception raised when the given asset_value contains negative values."""

    def __init__(self) -> None:
        super().__init__("Negative values in asset_value are not allowed.")


def calculate_asset_tax(
    asset_value: np.ndarray,
    expected_return_rate: float,
    tax_rate: float,
    tax_free_amount: float,
) -> np.ndarray:
    """
    Calculate the tax on the return of an asset based on the 2024 taxation model.

    Parameters
    ----------
    asset_value : np.ndarray
        The value of the asset.
    expected_return_rate : float
        The expected return rate of the asset.
    tax_rate : float
        The tax rate.
    tax_free_amount : float
        The amount of the asset value that is tax free.

    Returns
    -------
    np.ndarray
        The tax on the return of the asset.

    Raises
    ------
    NegativeValueError
        If there are negative values in `asset_value`.
    """
    if np.any(asset_value < 0):
        raise NegativeValueError

    taxable_return = asset_value * expected_return_rate
    basis_rate = (asset_value - tax_free_amount) / asset_value

    return np.where(basis_rate > 0, taxable_return * basis_rate * tax_rate, 0.0)
