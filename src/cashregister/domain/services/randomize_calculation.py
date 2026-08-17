# Core idea: The app should randomly generate the change denominations
# but the math still needs to be right.
import random
from decimal import Decimal
from cashregister.domain.entities.change import ChangeLine, ChangeResult
from cashregister.domain.entities.money import Money


def randomize_change(amount: Decimal, money: Money) -> ChangeResult:
    """
    For every money unit we need to choose randomly how many coins to use and leave the smaller coin
    to complete what is left.
    """
    if amount < 0:
        raise ValueError("Error (CR-03): amount must be >= 0")

    remaining = amount
    lines: list[ChangeLine] = []

    for unit in money.currency_units[:-1]: # except last element
        # getting the maximum integer value random(0, "max found")
        quantity = random.randint(0, int(remaining // unit.value))

        if quantity:
            lines.append(ChangeLine(currency_unit=unit, quantity=quantity))
            remaining -= unit.value * quantity # what was left

    smallest = money.currency_units[-1]
    quantity = int(remaining // smallest.value) # ignoring decimal part

    if quantity:
        lines.append(ChangeLine(currency_unit=smallest, quantity=quantity))

    return ChangeResult(lines=lines)
