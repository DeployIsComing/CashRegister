# format final values into output format
from cashregister.domain.entities.change import ChangeResult


def format_change(result: ChangeResult) -> str:
    parts = []

    for line in result.lines:
        name = line.denomination.name if line.quantity == 1 else line.denomination.plural # set singular or plural
        parts.append(f"{line.quantity} {name}")
    return ",".join(parts)
