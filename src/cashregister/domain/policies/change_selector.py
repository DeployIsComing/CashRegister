# Core idea: The app should randomly generate the change denominations
# but the math still needs to be right.
from decimal import Decimal
from cashregister.domain.services.change_method import ChangeMethod


def select_change_strategy(owed: Decimal, random_divisor: int) -> ChangeMethod:
    owed_cents = int(owed * 100)
    if owed_cents % random_divisor == 0:
        return calculate_random_change
    return calculate_minimum_change