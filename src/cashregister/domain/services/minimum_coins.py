# minimum amount of physical change using the high currency unit
from decimal import Decimal
from cashregister.domain.entities.change import ChangeResult, ChangeLine
from cashregister.domain.entities.money import Money

def calc_minimum_change(amount: Decimal, money: Money) -> ChangeResult:
    if amount < 0:
        raise ValueError("Error (CR-01): amount must be >= 0")

    remaining = amount
    lines: list[ChangeLine] = []

    for unit in money.currency_units:
        quantity = int(remaining // unit.value) # getting just the int part
        if quantity > 0:
            lines.append(ChangeLine(currency_unit=unit, quantity=quantity))
            remaining -= unit.value * quantity # using only the multiplication of what has already been deducted

    return ChangeResult(lines=lines)
