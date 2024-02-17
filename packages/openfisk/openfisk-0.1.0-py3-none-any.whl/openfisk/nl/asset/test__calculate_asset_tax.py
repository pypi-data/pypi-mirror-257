"""Tests for the calculate_asset_tax function."""

import numpy as np
import pytest

from .calculate_asset_tax import NegativeValueError, calculate_asset_tax


@pytest.mark.parametrize(
    ("asset_value", "expected_return_rate", "tax_rate", "tax_free_amount", "expected_tax"),
    [
        # Base case
        (np.array([0, 57000, 150000]), 0.0103, 0.36, 57000, np.array([0, 0, 344.844])),
        # Zero expected return rate
        (np.array([0, 57000, 150000]), 0.0, 0.36, 57000, np.array([0, 0, 0])),
        # Zero tax rate
        (np.array([0, 57000, 150000]), 0.0103, 0.0, 57000, np.array([0, 0, 0])),
        # Zero tax-free amount
        (np.array([0, 57000, 150000]), 0.0103, 0.36, 0, np.array([0, 211.356, 556.2])),
    ],
)
def test__calculate_asset_tax(
    asset_value: np.ndarray,
    expected_return_rate: float,
    tax_rate: float,
    tax_free_amount: float,
    expected_tax: np.ndarray,
) -> None:
    """
    Test the calculate_asset_tax function based on various input parameters.

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
    expected_tax : np.ndarray
        The expected tax on the return of the asset.

    Asserts
    -------
    - The calculated tax on the return of the asset is almost equal to the expected tax.
    """
    actual_tax = calculate_asset_tax(
        asset_value,
        expected_return_rate,
        tax_rate,
        tax_free_amount,
    )
    np.testing.assert_array_almost_equal(actual_tax, expected_tax)


def test__negative_asset_value_error() -> None:
    """
    Test the calculate_asset_tax function with a negative asset value.

    Asserts
    -------
    - A NegativeValueError is raised.
    """
    asset_value = np.array([0, -57000, 15000])  # Contains a negative value
    expected_return_rate = 0.103
    tax_rate = 0.36
    tax_free_amount = 57000

    with pytest.raises(NegativeValueError):
        calculate_asset_tax(asset_value, expected_return_rate, tax_rate, tax_free_amount)
