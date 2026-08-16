# Version 0.0.1
# Cash Register System
# Author: Carlos Eduardo da Silva <carlosedasilva@gmail.com>
import time
import sys
from cashregister.adapters.cli.simple_entity_tests import test_money_entity


def main() -> None:
    """
    Cash register initial flow
    """
    print("Cash Register [Version 0.0.1]")
    print("(c) 2026 Carlos Corporation No rights reserved.")
    print("Connecting to Skynet...")
    time.sleep(2)

    # system additional options
    args = sys.argv[1]
    if args:
        if args == "--simple-test": # testing entities if true
            print("Testing Money entity...")
            test_money_entity()

if __name__ == "__main__":
    main()
