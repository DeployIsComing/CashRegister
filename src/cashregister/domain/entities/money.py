# Money entity class acting as VO.
from dataclasses import dataclass
from decimal import Decimal
from pydantic import BaseModel, field_validator
from cashregister.domain.entities.currency_unit import CurrencyUnit


class Money(BaseModel):
    code: str
    symbol: str
    currency_units: list[CurrencyUnit]

    @field_validator("currency_units")
    @staticmethod
    def sorted_desc(m_unit: list[CurrencyUnit]) -> list[CurrencyUnit]:
        """"
        Highest value first
        """
        def get_value(value: CurrencyUnit) -> Decimal:
            return value.value
        return sorted(m_unit, key=get_value, reverse=True)
