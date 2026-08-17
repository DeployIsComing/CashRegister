# The idea here is to parse the selected (country) json file and make data available for the system
import json
from pathlib import Path
from cashregister.domain.entities.money import Money

DEFAULT_MONEY_DIR = Path(__file__).resolve().parents[4] / "config" / "i18n" / "currencies"


def load_currency(code: str, currencies_dir: Path = DEFAULT_MONEY_DIR) -> Money:
    path = currencies_dir / f"{code}.json"
    data = json.loads(path.read_text())
    return Money.model_validate(data)
