from decimal import Decimal

from cashregister.domain.entities.currency_unit import CurrencyUnit
from cashregister.domain.entities.money import Money


def _unit(name: str, value: str) -> CurrencyUnit:
    return CurrencyUnit(name=name, plural=name, value=Decimal(value))


def test_currency_units_are_sorted_descending_on_init() -> None:
    # Scenario 1.1: Automatic Sorting on Initialization
    unsorted_units = [
        _unit("real", "1.00"),
        _unit("cinquenta reais", "50.00"),
        _unit("cinquenta centavos", "0.50"),
        _unit("vinte reais", "20.00"),
    ]

    money = Money(code="BRL", symbol="R$", currency_units=unsorted_units)

    assert [unit.value for unit in money.currency_units] == [
        Decimal("50.00"),
        Decimal("20.00"),
        Decimal("1.00"),
        Decimal("0.50"),
    ]


def test_instances_with_identical_contents_are_equal() -> None:
    # Scenario 1.2: Value Object Structural Equality
    units_a = [_unit("real", "1.00"), _unit("cinquenta reais", "50.00")]
    units_b = [_unit("real", "1.00"), _unit("cinquenta reais", "50.00")]

    money_a = Money(code="BRL", symbol="R$", currency_units=units_a)
    money_b = Money(code="BRL", symbol="R$", currency_units=units_b)

    assert money_a == money_b
    assert money_a is not money_b
