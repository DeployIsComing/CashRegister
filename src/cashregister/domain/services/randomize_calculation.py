# Core idea: The app should randomly generate the change denominations
# but the math still needs to be right.
import random
from decimal import Decimal
from cashregister.domain.entities.change import ChangeLine, ChangeResult
from cashregister.domain.entities.money import Money


def randomize_change(amount: Decimal, money: Money) -> ChangeResult:
    if amount < 0:
        raise ValueError("Error (CR-03): amount must be >= 0")

    remaining = amount
    lines: list[ChangeLine] = []

    for unit in money.currency_units[:-1]:
        # getting the integer part and use it in randon
        quantity = random.randint(0, int(remaining // unit.value))

        if quantity:
            lines.append(ChangeLine(currency_unit=unit, quantity=quantity))
            remaining -= unit.value * quantity

    smallest = money.currency_units[-1]
    quantity = int(remaining // smallest.value) # ignoring decimal part

    if quantity:
        lines.append(ChangeLine(currency_unit=smallest, quantity=quantity))

    return ChangeResult(lines=lines)
