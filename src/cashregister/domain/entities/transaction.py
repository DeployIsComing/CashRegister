# The idea is to tell the cashier how much change is owed and paid
from decimal import Decimal
from pydantic import BaseModel, Field, model_validator


class Transaction(BaseModel):
    owed: Decimal = Field(ge=0)
    paid: Decimal = Field(ge=0)

    @model_validator(mode="after")
    def paid_covers_owed(self) -> "Transaction":
        if self.paid < self.owed:
            raise ValueError("Error (CR-02): paid must be >= owed")
        return self

    @property
    def change(self) -> Decimal:
        return self.paid - self.owed
