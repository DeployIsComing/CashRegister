# vo for currency unit
from decimal import Decimal
from pydantic import BaseModel, ConfigDict, Field


class CurrencyUnit(BaseModel):
    model_config = ConfigDict(frozen=True)
    name: str
    plural: str
    # As the system is a small app, I decided for decimal here to simplify the process.
    # but for production ready system I would think to add something more complex.
    value: Decimal = Field(gt=0)

