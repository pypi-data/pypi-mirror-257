"""Tests for the calculate_income_tax function."""

import numpy as np
import pytest

from .calculate_income_tax import (
    InvalidTaxRatesError,
    NegativeValueError,
    UnsortedTaxBandsError,
    calculate_income_tax,
)


@pytest.mark.parametrize(
    ("taxable_income", "tax_bands", "tax_rates", "expected_tax"),
    [
        # Single tax band
        (
            np.array([5000, 15000, 25000]),
            np.array([0, 30000]),
            np.array([0.1]),
            np.array([500, 1500, 2500]),
        ),
        # Multiple tax bands
        (
            np.array([10000, 30000, 50000]),
            np.array([0, 20000, 40000, 60000]),
            np.array([0.1, 0.2, 0.3]),
            np.array([1000, 4000, 9000]),
        ),
        # Unbounded tax band
        (
            np.array([70000, 90000, 110000]),
            np.array([0, 50000, 100000, np.inf]),
            np.array([0.1, 0.2, 0.3]),
            np.array([9000, 13000, 18000]),
        ),
        # Non-zero tax-free threshold
        (
            np.array([70000, 90000, 110000]),
            np.array([10000, 50000, 100000, np.inf]),
            np.array([0.1, 0.2, 0.3]),
            np.array([8000, 12000, 17000]),
        ),
        # Exact band thresholds
        (
            np.array([20000, 40000, 60000]),
            np.array([0, 20000, 40000, 60000]),
            np.array([0.1, 0.2, 0.3]),
            np.array([2000, 6000, 12000]),
        ),
        # Zero income
        (
            np.array([0]),
            np.array([0, 10000, 20000, 30000]),
            np.array([0.1, 0.2, 0.3]),
            np.array([0]),
        ),
    ],
)
def test__calculate_income_tax(
    taxable_income: np.ndarray,
    tax_bands: np.ndarray,
    tax_rates: np.ndarray,
    expected_tax: np.ndarray,
) -> None:
    """
    Test the calculate_income_tax function based on various input parameters.

    Parameters
    ----------
    taxable_income : float
        The taxable income.
    tax_bands : np.ndarray
        The tax band thresholds.
    tax_rates : np.ndarray
        The tax rates.
    expected_tax : float
        The expected tax.

    Asserts
    -------
    - The calculated tax is almost equal to the expected tax.
    """
    actual_tax = calculate_income_tax(
        taxable_income,
        tax_bands,
        tax_rates,
    )
    np.testing.assert_array_almost_equal(actual_tax, expected_tax)


def test__negative_taxable_income_error() -> None:
    """
    Test the calculate_income_tax function with a negative taxable income.

    Asserts
    -------
    - A NegativeValueError is raised.
    """
    with pytest.raises(NegativeValueError):
        calculate_income_tax(
            np.array([-1, 0, 10000]),
            np.array([0, 10000, 20000]),
            np.array([0.1, 0.2]),
        )


def test__unsorted_tax_bands_error() -> None:
    """
    Test the calculate_income_tax function with unsorted tax bands.

    Asserts
    -------
    - An UnsortedTaxBandsError is raised.
    """
    with pytest.raises(UnsortedTaxBandsError):
        calculate_income_tax(
            np.array([0, 10000, 20000]),
            np.array([0, 20000, 10000]),
            np.array([0.1, 0.2]),
        )


def test__invalid_tax_rates_error() -> None:
    """
    Test the calculate_income_tax function with invalid tax rates.

    Asserts
    -------
    - An InvalidTaxRatesError is raised.
    """
    with pytest.raises(InvalidTaxRatesError):
        calculate_income_tax(
            np.array([0, 10000, 20000]),
            np.array([0, 10000, 20000]),
            np.array([0.1, 0.2, 0.3]),
        )
