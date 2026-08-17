from decimal import Decimal

import pytest

from cashregister.domain.entities.currency_unit import CurrencyUnit
from cashregister.domain.entities.money import Money


@pytest.fixture
def brl() -> Money:
    units = [
        CurrencyUnit(name="Um Real", plural="reais", value=Decimal("1.00")),
        CurrencyUnit(name="Cinquenta Reais", plural="reais", value=Decimal("50.00")),
        CurrencyUnit(name="Vinte Reais", plural="reais", value=Decimal("20.00")),
        CurrencyUnit(name="Dez Reais", plural="reais", value=Decimal("10.00")),
        CurrencyUnit(name="Cinquenta Centavos", plural="reais", value=Decimal("0.50")),
        CurrencyUnit(name="Vinte e Cinco Centavos", plural="reais", value=Decimal("0.25")),
        CurrencyUnit(name="Cinco Centavos", plural="reais", value=Decimal("0.05")),
    ]
    return Money(code="BRL", symbol="R$", currency_units=units)
