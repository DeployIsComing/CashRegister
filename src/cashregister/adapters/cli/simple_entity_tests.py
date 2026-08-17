# Simple testing script to check VOs during development
from decimal import Decimal
from cashregister.domain.entities.money import Money
from cashregister.domain.entities.currency_unit import CurrencyUnit

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
