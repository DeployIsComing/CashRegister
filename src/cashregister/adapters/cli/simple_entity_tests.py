# Simple testing script to check VOs during development
from decimal import Decimal
from cashregister.domain.entities.money import Money
from cashregister.domain.entities.currency_unit import CurrencyUnit
from cashregister.domain.services.minimum_coins import calc_minimum_change


def test_money_entity() -> None:
    print("--- Testing Money entity ---")

    # playing with brazilian money
    m_units = [
        CurrencyUnit(name="Um Real", value=Decimal("1.00"), plural="real"),
        CurrencyUnit(name="Cinquenta Reais", value=Decimal("50.00"), plural="reais"),
        CurrencyUnit(name="Cinquenta Centavos", value=Decimal("0.50"), plural="reais"),
        CurrencyUnit(name="Vinte Reais", value=Decimal("20.00"), plural="reais"),
    ]

    money = Money(code="BRL", symbol="R$", currency_units=m_units)

    print("-----------------------------------------------")
    print(f"Currency: {money.code} ({money.symbol} = {money.currency_units})")
    print("\nCurrency units, should show highest value first:")
    print("-----------------------------------------------")

    for unit in money.currency_units:
        print(f" - {unit.name}: {money.symbol} {unit.value}")


def test_minimum_change() -> None:
    print("--- Testing minimum change ---")

    # playing with brazilian money
    m_units = [
        CurrencyUnit(name="Um Real", value=Decimal("1.00"), plural="real"),
        CurrencyUnit(name="Cinquenta Reais", value=Decimal("50.00"), plural="real"),
        CurrencyUnit(name="Vinte Reais", value=Decimal("20.00"), plural="reais"),
        CurrencyUnit(name="Dez Reais", value=Decimal("10.00"), plural="reais"),
        CurrencyUnit(name="Cinquenta Centavos", value=Decimal("0.50"), plural="reais"),
        CurrencyUnit(
            name="Vinte e Cinco Centavos", value=Decimal("0.25"), plural="real"
        ),
        CurrencyUnit(name="Cinco Centavos", value=Decimal("0.05"), plural="real"),
    ]

    brl = Money(code="BRL", symbol="R$", currency_units=m_units)

    # set a change value
    target_change = Decimal("181.80")
    print(f"Calculating change for: {brl.symbol} {target_change}\n")
    result = calc_minimum_change(target_change, brl)

    print("Result:")
    for line in result.lines:
        print(
            f" - {line.quantity}x {line.currency_unit.name} ({brl.symbol} {line.currency_unit.value})"
        )

    print("❌ Incorrect values")
    try:
        calc_minimum_change(Decimal("-10.00"), brl)
    except ValueError as e:
        print(f"Error found: {e}")
