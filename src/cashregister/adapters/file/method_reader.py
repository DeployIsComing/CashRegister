# Reads the transactions input file no need to change core idea in domain
from decimal import Decimal
from pathlib import Path
from cashregister.domain.entities.transaction import Transaction


def read_transactions(path: Path) -> list[Transaction]:
    transactions: list[Transaction] = []

    for line in path.read_text().splitlines():
        line = line.strip()
        if not line:
            continue
        owed, paid = line.split(",")
        transactions.append(Transaction(owed=Decimal(owed), paid=Decimal(paid)))
    return transactions
