# any change method we define what is the input and what is the result
from decimal import Decimal
from typing import Callable
from cashregister.domain.entities.money import Money
from cashregister.domain.entities.change import ChangeResult

ChangeMethod = Callable[[Decimal, Money], ChangeResult]
