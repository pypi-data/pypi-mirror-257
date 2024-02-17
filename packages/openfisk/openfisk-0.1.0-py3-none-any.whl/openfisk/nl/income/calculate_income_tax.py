"""Income tax calculation for the Netherlands in 2024."""

import numpy as np


class UnsortedTaxBandsError(ValueError):
    """Exception raised when the given tax_bands are not sorted in ascending order."""

    def __init__(self) -> None:
        super().__init__("tax_bands must be sorted in ascending order.")


class InvalidTaxRatesError(ValueError):
    """Exception raised when the given tax_rates are not one less than the length of tax_bands."""

    def __init__(self) -> None:
        super().__init__("The length of tax_rates must be one less than the length of tax_bands.")


class NegativeValueError(ValueError):
    """Exception raised when the given taxable_income or tax_bands contain negative values."""

    def __init__(self) -> None:
        super().__init__("Negative values in taxable_income or tax_bands are not allowed.")


def calculate_income_tax(
    taxable_income: np.ndarray,
    tax_bands: np.ndarray,
    tax_rates: np.ndarray,
) -> np.ndarray:
    """
    Calculate the income tax based on the 2024 taxation model.

    The function computes the tax for each entry in `taxable_income` by applying the corresponding
    tax rates for the amounts within each tax band. It assumes that `tax_bands` are sorted in
    ascending order and that the length of `tax_rates` is one less than the length of `tax_bands`.

    Parameters
    ----------
    taxable_income : np.ndarray
        A 1D array containing the taxable income amounts for which the tax is to be calculated.
    tax_bands : np.ndarray
        A 1D array containing the tax band thresholds. Must be sorted in ascending order.
        The first element is typically `0`, representing the tax-free threshold.
        The upper (unbounded) tax bracket can be represented using `np.inf`.
    tax_rates : np.ndarray
        A 1D array containing the tax rates corresponding to the intervals defined by `tax_bands`.
        The rate at index `i` applies to the income between `tax_bands[i]` and `tax_bands[i+1]`.

    Returns
    -------
    np.ndarray
        A 1D array containing the calculated tax for each taxable income in `taxable_income`.

    Raises
    ------
    UnsortedTaxBandsError
        If the `tax_bands` are not sorted in ascending order.
    InvalidTaxRatesError
        If the length of `tax_rates` is not one less than the length of `tax_bands`.
    NegativeValueError
        If the `taxable_income` or `tax_bands` contain negative values.

    Examples
    --------
    >>> taxable_income = np.array([10000, 30000, 50000])
    >>> tax_bands = np.array([0, 20000, 40000, 60000])
    >>> tax_rates = np.array([0.1, 0.2, 0.3])
    >>> calculate_income_tax(taxable_income, tax_bands, tax_rates)
    array([1000., 4000., 9000.])
    """
    if not np.all(tax_bands[:-1] <= tax_bands[1:]):
        raise UnsortedTaxBandsError

    if len(tax_rates) != len(tax_bands) - 1:
        raise InvalidTaxRatesError

    if np.any(taxable_income < 0) or np.any(tax_bands < 0):
        raise NegativeValueError

    amounts_in_bands = (
        np.broadcast_to(
            taxable_income,
            (tax_bands.shape[0] - 1, taxable_income.shape[0]),
        )
        .transpose()
        .clip(tax_bands[:-1], tax_bands[1:])
        - tax_bands[:-1]
    )

    return (tax_rates * amounts_in_bands).sum(axis=1)
