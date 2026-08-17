# Core idea: The app should randomly generate the change denominations
# but the math still needs to be right.
from decimal import Decimal
from cashregister.domain.services.change_method import ChangeMethod
from cashregister.domain.services.minimum_coins import  calc_minimum_change
from cashregister.domain.services.randomize_calculation import randomize_change


def select_change_strategy(owed: Decimal, random_divisor: int) -> ChangeMethod:
    owed_cents = int(owed * 100)
    if owed_cents % random_divisor == 0:
        return randomize_change
    return calc_minimum_change
