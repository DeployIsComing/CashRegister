# money change - result of change calculation
from pydantic import BaseModel, Field
from cashregister.domain.entities.currency_unit import CurrencyUnit

class ChangeLine(BaseModel):
    """"
    Output the change the cashier should return to the customer
        1. The return string should look like: 1 dollar,2 quarters,1 nickel, etc ...
        2. Each new line in the input file should be a new line in the output file
    """
    currency_unit: CurrencyUnit
    quantity: int = Field(gt=0)


class ChangeResult(BaseModel):
    # list of changes.
    lines: list[ChangeLine]
