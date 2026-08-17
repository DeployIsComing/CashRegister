from cashregister.domain.entities.change import ChangeResult
from cashregister.domain.entities.money import Money
from cashregister.domain.entities.transaction import Transaction
from cashregister.domain.policies.change_selector import select_change_strategy


def process_transactions(
    transactions: list[Transaction],
    currency: Money,
    random_divisor: int,
) -> list[ChangeResult]:
    results: list[ChangeResult] = []

    for transaction in transactions:
        strategy = select_change_strategy(transaction.owed, random_divisor)
        results.append(strategy(transaction.change, currency))
    return results
