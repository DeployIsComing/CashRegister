# Test Suite Specification (Pytest) - Cash Register Domain

## Core Guidelines
- Framework: `pytest`
- Monetary Values: MUST always use `Decimal` (never `float`) to avoid precision bugs.
- Design Principles: Test entities as immutable Value Objects where applicable.

---

## 1. Entity: Money (`cashregister/domain/entities/money.py`)

`Money` is a pydantic `BaseModel` with fields `code: str`, `symbol: str`, `currency_units: list[CurrencyUnit]`. All three are required to construct an instance.

### Scenarios
- **Scenario 1.1: Automatic Sorting on Initialization**
  - **Given** an unsorted list of `CurrencyUnit` objects (e.g., 1.00, 50.00, 0.50, 20.00).
  - **When** initializing the `Money` entity (with a `code` and `symbol`, e.g. `code="BRL", symbol="R$"`).
  - **Then** the `currency_units` field should automatically be reordered in descending order by value (50.00, 20.00, 1.00, 0.50).

- **Scenario 1.2: Value Object Structural Equality**
  - **Given** two distinct instances of `Money` with identical `code`, `symbol`, and `currency_units` contents.
  - **When** comparing them using `==`.
  - **Then** they should be considered equal (`money_a == money_b`).

---

## 2. Domain Service: Minimum Change (`cashregister/domain/services/minimum_coins.py`)

`calc_minimum_change(amount: Decimal, money: Money) -> ChangeResult` — note the second parameter is named `money`, not `currency`.

### Scenarios
- **Scenario 2.1: Negative Amount Validation**
  - **Given** a negative change amount (e.g., `Decimal("-10.00")`).
  - **When** calling `calc_minimum_change(amount, money)`.
  - **Then** it must raise a `ValueError` with the message `"Error (CR-01): amount must be >= 0"`.

- **Scenario 2.2: Greedy Minimum Coins/Notes Calculation**
  - **Given** a custom BRL `Money` fixture with `currency_units` of value 50.00, 20.00, 10.00, 1.00, 0.50, 0.25, 0.05 (mirrors the fixture already used in `adapters/cli/simple_entity_tests.py`).
  - **When** requesting change for `Decimal("181.80")`.
  - **Then** the service should return a `ChangeResult` whose `lines` contain exactly, each as a `ChangeLine(currency_unit, quantity)`:
    - 3x 50.00
    - 1x 20.00
    - 1x 10.00
    - 1x 1.00
    - 1x 0.50
    - 1x 0.25
    - 1x 0.05

- **Scenario 2.3: Zero Amount Edge Case**
  - **Given** a change amount of `Decimal("0.00")`.
  - **When** calling `calc_minimum_change(amount, money)`.
  - **Then** it should return a valid `ChangeResult` with an empty `lines` list (`len(result.lines) == 0`).

---

## 3. Domain Service: Randomize Change (`cashregister/domain/services/randomize_calculation.py`)

`randomize_change(amount: Decimal, money: Money) -> ChangeResult` — same signature shape as `calc_minimum_change`. For every currency unit except the smallest (`money.currency_units[:-1]`), it picks a uniformly random quantity between 0 and the maximum affordable count (`random.randint(0, remaining // unit.value)`); the smallest unit then absorbs whatever remains via floor division. It relies on `money.currency_units` already being sorted descending, which `Money`'s own validator guarantees (see Scenario 1.1). Because the loop and the random module are used at import time, tests must patch `cashregister.domain.services.randomize_calculation.random.randint` (not the global `random` module in isolation) to make outcomes deterministic.

### Scenarios
- **Scenario 3.1: Negative Amount Validation**
  - **Given** a negative change amount (e.g., `Decimal("-10.00")`).
  - **When** calling `randomize_change(amount, money)`.
  - **Then** it must raise a `ValueError` with the message `"Error (CR-03): amount must be >= 0"` (note: a different error code than `calc_minimum_change`'s `CR-01`).

- **Scenario 3.2: Zero Amount Edge Case**
  - **Given** a change amount of `Decimal("0.00")`.
  - **When** calling `randomize_change(amount, money)`.
  - **Then** it should return a valid `ChangeResult` with an empty `lines` list.

- **Scenario 3.3: Deterministic Upper Bound (random always picks the max)**
  - **Given** the same BRL `Money` fixture and amount used in Scenario 2.2, with `random.randint` monkeypatched to always return its upper bound.
  - **When** calling `randomize_change(Decimal("181.80"), money)`.
  - **Then** the result must be identical to the greedy breakdown from Scenario 2.2 (3x 50.00, 1x 20.00, 1x 10.00, 1x 1.00, 1x 0.50, 1x 0.25, 1x 0.05), since always taking the max affordable quantity degenerates into the greedy algorithm.

- **Scenario 3.4: Deterministic Lower Bound (random always picks zero)**
  - **Given** the same fixture and amount, with `random.randint` monkeypatched to always return `0`.
  - **When** calling `randomize_change(Decimal("181.80"), money)`.
  - **Then** every unit except the smallest contributes a quantity of 0 and is therefore excluded from `lines` (`ChangeLine.quantity` must be `> 0`), and the entire amount is expressed in the smallest unit: a single line of 3636x 0.05.

- **Scenario 3.5: Total Value Invariant Across Random Outcomes**
  - **Given** an amount that is an exact multiple of the smallest currency unit's value (e.g., `Decimal("181.80")` with a smallest unit of 0.05).
  - **When** calling `randomize_change` repeatedly under different `random.seed()` values (no mocking).
  - **Then** `sum(line.currency_unit.value * line.quantity for line in result.lines)` must always equal the requested amount exactly, regardless of the random choices made, and every line's `quantity` must be `> 0`.

---

## 4. Domain Policy: Change Strategy Selector (`cashregister/domain/policies/change_selector.py`)

`select_change_strategy(owed: Decimal, random_divisor: int) -> ChangeMethod` — returns the `randomize_change` function reference when `int(owed * 100) % random_divisor == 0`, otherwise returns the `calc_minimum_change` function reference. It returns the callables themselves (compare with `is`), it does not invoke them.

### Scenarios
- **Scenario 4.1: Selects Randomize Strategy When Owed Cents Are Divisible**
  - **Given** `owed = Decimal("10.00")` and `random_divisor = 5` (so `owed_cents = 1000`, `1000 % 5 == 0`).
  - **When** calling `select_change_strategy(owed, random_divisor)`.
  - **Then** it should return the `randomize_change` function (`strategy is randomize_change`).

- **Scenario 4.2: Selects Minimum Coins Strategy When Not Divisible**
  - **Given** `owed = Decimal("10.01")` and `random_divisor = 5` (so `owed_cents = 1001`, `1001 % 5 == 1`).
  - **When** calling `select_change_strategy(owed, random_divisor)`.
  - **Then** it should return the `calc_minimum_change` function (`strategy is calc_minimum_change`).

- **Scenario 4.3: Zero Divisor Is Not Guarded**
  - **Given** `random_divisor = 0`.
  - **When** calling `select_change_strategy(Decimal("10.00"), 0)`.
  - **Then** it currently raises a `ZeroDivisionError` (the `% random_divisor` operation is unguarded) — this scenario documents existing behavior rather than a validated contract; revisit if the implementation adds input validation.
