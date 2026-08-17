from decimal import Decimal

import pytest

from cashregister.domain.policies.change_selector import select_change_strategy
from cashregister.domain.services.minimum_coins import calc_minimum_change
from cashregister.domain.services.randomize_calculation import randomize_change


def test_selects_randomize_strategy_when_owed_cents_divisible_by_divisor() -> None:
    # Scenario 4.1: Selects Randomize Strategy When Owed Cents Are Divisible
    strategy = select_change_strategy(Decimal("10.00"), 5)

    assert strategy is randomize_change


def test_selects_minimum_coins_strategy_when_owed_cents_not_divisible() -> None:
    # Scenario 4.2: Selects Minimum Coins Strategy When Not Divisible
    strategy = select_change_strategy(Decimal("10.01"), 5)

    assert strategy is calc_minimum_change


def test_zero_divisor_raises_zero_division_error() -> None:
    # Scenario 4.3: Zero Divisor Is Not Guarded
    with pytest.raises(ZeroDivisionError):
        select_change_strategy(Decimal("10.00"), 0)
