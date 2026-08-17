from decimal import Decimal

import pytest

from cashregister.domain.entities.money import Money
from cashregister.domain.services.minimum_coins import calc_minimum_change


def test_negative_amount_raises_value_error(brl: Money) -> None:
    # Scenario 2.1: Negative Amount Validation
    with pytest.raises(ValueError, match=r"Error \(CR-01\): amount must be >= 0"):
        calc_minimum_change(Decimal("-10.00"), brl)


def test_greedy_minimum_change_calculation(brl: Money) -> None:
    # Scenario 2.2: Greedy Minimum Coins/Notes Calculation
    result = calc_minimum_change(Decimal("181.80"), brl)

    breakdown = {line.currency_unit.value: line.quantity for line in result.lines}

    assert breakdown == {
        Decimal("50.00"): 3,
        Decimal("20.00"): 1,
        Decimal("10.00"): 1,
        Decimal("1.00"): 1,
        Decimal("0.50"): 1,
        Decimal("0.25"): 1,
        Decimal("0.05"): 1,
    }


def test_zero_amount_returns_empty_lines(brl: Money) -> None:
    # Scenario 2.3: Zero Amount Edge Case
    result = calc_minimum_change(Decimal("0.00"), brl)

    assert result.lines == []
    assert len(result.lines) == 0
