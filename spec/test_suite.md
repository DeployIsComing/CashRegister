# Test Suite Specification (Pytest) - Cash Register Domain

## Core Guidelines
- Framework: `pytest`
- Monetary Values: MUST always use `Decimal` (never `float`) to avoid precision bugs.
- Design Principles: Test entities as immutable Value Objects where applicable.

---

## 1. Entity: Money (`cashregister.domain.entities.money.py`)

### Scenarios
- **Scenario 1.1: Automatic Sorting on Initialization**
  - **Given** an unsorted list of `CurrencyUnit` objects (e.g., 1.00, 50.00, 0.50, 20.00).
  - **When** initializing the `Money` entity.
  - **Then** the validator should automatically reorder `currency_unit` in descending order by value (50.00, 20.00, 1.00, 0.50).

- **Scenario 1.2: Value Object Structural Equality**
  - **Given** two distinct instances of `Money` with identical `code`, `symbol`, and `currency_unit` contents.
  - **When** comparing them using `==`.
  - **Then** they should be considered equal (`money_a == money_b`).

---

## 2. Domain Service: Minimum Change (`cashregister.domain.services.minimum_coins.py`)

### Scenarios
- **Scenario 2.1: Negative Amount Validation**
  - **Given** a negative change amount (e.g., `Decimal("-10.00")`).
  - **When** calling `calc_minimum_change(amount, currency)`.
  - **Then** it must raise a `ValueError` with the message `"Error (CR-01): amount must be >= 0"`.

- **Scenario 2.2: Greedy Minimum Coins/Notes Calculation**
  - **Given** a standard BRL currency setup (50.00, 20.00, 10.00, 1.00, 0.50, 0.25, 0.05).
  - **When** requesting change for `Decimal("181.80")`.
  - **Then** the service should return a `ChangeResult` containing exactly:
    - 3x 50.00
    - 1x 20.00
    - 1x 10.00
    - 1x 1.00
    - 1x 0.50
    - 1x 0.25
    - 1x 0.05

- **Scenario 2.3: Zero Amount Edge Case**
  - **Given** a change amount of `Decimal("0.00")`.
  - **When** calling `calc_minimum_change(amount, currency)`.
  - **Then** it should return a valid `ChangeResult` with an empty `lines` list (`len(result.lines) == 0`).
