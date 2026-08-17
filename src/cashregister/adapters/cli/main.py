#                _                      _     _
#   ___ __ _ ___| |__    _ __ ___  __ _(_)___| |_ ___ _ __
#  / __/ _` / __| '_ \  | '__/ _ \/ _` | / __| __/ _ \ '__|
# | (_| (_| \__ \ | | | | | |  __/ (_| | \__ \ ||  __/ |
#  \___\__,_|___/_| |_| |_|  \___|\__, |_|___/\__\___|_|
#                                |___/

# Version 0.0.1
# Cash Register System
# Author: Carlos Eduardo da Silva <carlosedasilva@gmail.com>

import time
import argparse
from pathlib import Path
from cashregister.adapters.config.parse_currency_format import load_currency
from cashregister.adapters.file.method_reader import read_transactions
from cashregister.adapters.file.output import format_change
from cashregister.application.process import process_transactions
from cashregister.adapters.cli.simple_entity_tests import (
    test_money_entity,
    test_minimum_change,
)

RANDOM_DIV = 3

def prompt_args() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="cashregister",
        description="Reads money transactions and outputs the change for each line.",
    )
    parser.add_argument("input", type=Path, help="Path to the input flat file")
    parser.add_argument("-o", "--output", type=Path, default=None, help="Output file (default: stdout)")
    parser.add_argument("-c", "--currency", default="USD", help="Currency code (default: USD)")
    parser.add_argument("-t", "--test", action="store_true", help="Run basic tests (default: false)")
    return parser


def main() -> None:
    """
    Cash register initial flow
    """
    print("Cash Register [Version 0.0.1]")
    print("(c) 2026 Carlos Corporation No rights reserved.")
    time.sleep(1)
    print("🤖 Initializing system [OK]\n\n")
    time.sleep(1)

    # starting transaction process
    args            = prompt_args().parse_args()
    currency        = load_currency(args.currency)
    transactions    = read_transactions(args.input)
    results         = process_transactions(transactions, currency, RANDOM_DIV)
    lines           = [format_change(result) for result in results]
    output_text     = "\n".join(lines)

    # display information
    if args.output:
        args.output.write_text(output_text + "\n")
    else:
        print(output_text)

    # system additional options
    if args.test:  # testing entities if true
        print("\n\n FIRST TEST")
        test_money_entity()
        print("\n\nSECOND TEST")
        test_minimum_change()

    # TODO - thinking about in creating an output data for api consumption or mcp
    # TODO - add jupyter or something related to reports to provide information
    # TODO - for internationalization avoid -> if coin == "quarter":


if __name__ == "__main__":
    main()
