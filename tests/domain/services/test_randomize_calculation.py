import random
from decimal import Decimal

import pytest

from cashregister.domain.entities.money import Money
from cashregister.domain.services.randomize_calculation import randomize_change


def test_negative_amount_raises_value_error(brl: Money) -> None:
    # Scenario 3.1: Negative Amount Validation
    with pytest.raises(ValueError, match=r"Error \(CR-03\): amount must be >= 0"):
        randomize_change(Decimal("-10.00"), brl)


def test_zero_amount_returns_empty_lines(brl: Money) -> None:
    # Scenario 3.2: Zero Amount Edge Case
    result = randomize_change(Decimal("0.00"), brl)

    assert result.lines == []


def test_upper_bound_matches_greedy_minimum_change(
    brl: Money, monkeypatch: pytest.MonkeyPatch
) -> None:
    # Scenario 3.3: Deterministic Upper Bound (random always picks the max affordable quantity)
    monkeypatch.setattr(
        "cashregister.domain.services.randomize_calculation.random.randint",
        lambda _low, high: high,
    )

    result = randomize_change(Decimal("181.80"), brl)
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


def test_lower_bound_pushes_everything_into_smallest_unit(
    brl: Money, monkeypatch: pytest.MonkeyPatch
) -> None:
    # Scenario 3.4: Deterministic Lower Bound (random always picks zero)
    monkeypatch.setattr(
        "cashregister.domain.services.randomize_calculation.random.randint",
        lambda _low, _high: 0,
    )

    result = randomize_change(Decimal("181.80"), brl)

    assert len(result.lines) == 1
    line = result.lines[0]
    assert line.currency_unit.value == Decimal("0.05")
    assert line.quantity == 3636


def test_total_value_matches_amount_across_random_outcomes(brl: Money) -> None:
    # Scenario 3.5: Total Value Invariant Across Random Outcomes
    amount = Decimal("181.80")

    for seed in range(20):
        random.seed(seed)
        result = randomize_change(amount, brl)
        total = sum(
            (line.currency_unit.value * line.quantity for line in result.lines),
            start=Decimal("0"),
        )
        assert total == amount
        assert all(line.quantity > 0 for line in result.lines)
