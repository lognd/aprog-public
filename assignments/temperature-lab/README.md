# Temperature Lab

method-trinity and self-cls-court taught you three method kinds --
instance methods, classmethods, staticmethods -- and how `@property`
turns a method into a validated, computed attribute. This assignment
asks you to combine all of it into one class: `Temperature`, storing a
value internally in degrees Celsius, with two alternate constructors
that build from Fahrenheit or Kelvin, a pure helper that checks whether a
value is physically possible, a property that rejects impossible values,
two read-only computed properties, and three dunder methods that make
`Temperature` objects printable, comparable for equality, and orderable.

## Learning goals

- Write classmethod alternate constructors (`from_fahrenheit`,
  `from_kelvin`) that build the right type even when called through a
  subclass
- Write a staticmethod helper that needs neither `self` nor `cls`
- Write a property with a validating setter that raises `ValueError` on
  an invalid assignment, and read-only properties with no setter at all
- Practice `__repr__`, `__eq__`, and `__lt__` with an exact output format
  and a floating-point tolerance for equality
- Use a class attribute (`absolute_zero`) shared across every instance

## Task

Implement a `Temperature` class in a file named `temperature.py`, with
exactly the following members.

### Class attribute

```python
absolute_zero: float = -273.15
```

The coldest physically possible temperature, in degrees Celsius. This
must be a class attribute (defined directly in the class body, not
inside `__init__`), so it is shared by the class itself and every
instance and subclass that does not override it.

### Constructor

```python
def __init__(self, celsius: float) -> None:
```

Stores `celsius` as the temperature's value, through the `celsius`
property described below (so construction is subject to the same
validation an assignment would be).

### Alternate constructors

```python
@classmethod
def from_fahrenheit(cls, f: float) -> "Temperature":
    """C = (F - 32) * 5 / 9"""

@classmethod
def from_kelvin(cls, k: float) -> "Temperature":
    """C = K - 273.15"""
```

Both must build and return `cls(...)`, not a hardcoded `Temperature(...)`
-- called through a subclass, they must construct an instance of that
subclass, exactly like `named_fido` in method-trinity.

- **Example (freezing point):** `Temperature.from_fahrenheit(32.0).celsius == 0.0`.
- **Example (scales agree):** `Temperature.from_fahrenheit(-40.0).celsius == -40.0` (the one temperature where the two scales agree).
- **Edge case (absolute zero):** `Temperature.from_kelvin(0.0).celsius == -273.15` (still physical since the check is `>=`).

### Physical-range check

```python
@staticmethod
def is_physical(celsius: float) -> bool:
    """True if celsius >= absolute_zero."""
```

A pure function of its `celsius` argument. It needs neither `self` nor
`cls` -- it is grouped inside `Temperature` purely for organization.

- **Edge case (boundary):** `Temperature.is_physical(-273.15) == True` (**the boundary itself counts as physical**).
- **Edge case (just past boundary):** `Temperature.is_physical(-273.16) == False` (anything colder does not).
- **Example:** `Temperature.is_physical(100.0) == True`.

### The `celsius` property

```python
@property
def celsius(self) -> float:
    ...

@celsius.setter
def celsius(self, value: float) -> None:
    ...
```

The getter returns the stored value. The setter must raise
`ValueError` if `value` is not physical (use `is_physical` to check), and
otherwise store it. Because `__init__` assigns through this property,
constructing a `Temperature` with an impossible value must also raise
`ValueError`.

- **Example:** `Temperature(0.0).celsius == 0.0`.
- **Error case (impossible value):** `Temperature(-300.0)` raises `ValueError` (colder than absolute zero, so **the object is never even constructed**).
- **Tricky case (boundary vs. past it):** after `t = Temperature(0.0)`, `t.celsius = -273.15` succeeds (the boundary is allowed) but `t.celsius = -273.16` raises `ValueError` and **leaves `t.celsius` unchanged** at whatever it was before the failed assignment.

### Read-only computed properties

```python
@property
def fahrenheit(self) -> float:
    """F = C * 9 / 5 + 32"""

@property
def kelvin(self) -> float:
    """K = C + 273.15"""
```

Both are computed from the stored Celsius value on every read. Neither
has a setter -- assigning to `t.fahrenheit` or `t.kelvin` must raise
`AttributeError`.

- **Example:** `Temperature(0.0).fahrenheit == 32.0`; `Temperature(0.0).kelvin == 273.15`.
- **Example (boiling point):** `Temperature(100.0).fahrenheit == 212.0`.
- **Error case (no setter):** assigning `Temperature(0.0).fahrenheit = 100.0` raises `AttributeError` because **there is no setter at all**, not even one that rejects the value.

### Dunder methods

```python
def __repr__(self) -> str:
    """Exactly "Temperature(<celsius>C)", celsius formatted to one decimal place."""

def __eq__(self, other: object) -> bool:
    """Equal if other is a Temperature and abs(self.celsius - other.celsius) < 1e-9."""

def __lt__(self, other: "Temperature") -> bool:
    """True if self.celsius < other.celsius."""
```

`__repr__("Temperature(21.5C)")` uses Python's normal `:.1f` rounding
behavior -- do not hand-write your own rounding logic. `__eq__` must
return `False` (not raise) when compared against a non-`Temperature`
object. `__lt__`, by contrast, must **raise `TypeError`** when compared
against a non-`Temperature` object -- ordering a temperature against an
arbitrary object is a programmer error, not a silent inequality.

Do not implement this with an `isinstance` check that raises `TypeError`
yourself. Instead, use Python's own comparison protocol: have `__eq__`
and `__lt__` each `return NotImplemented` (not `False`) when `other` is
not a `Temperature`. Python then retries the comparison from the other
object's side, and once both sides give up, it raises `TypeError` for
you for `<` (and falls back to identity/`False` for `==`, which is why
`__eq__` still appears to "return False" to the caller even though your
code never writes `return False` for that branch). This is why the
signatures above are typed `-> bool` even though the real return value
in that branch is `NotImplemented` -- type checkers special-case `__eq__`
and `__lt__` to allow this.

**`__repr__` examples:**

- **Example:** `repr(Temperature(21.5)) == 'Temperature(21.5C)'`.
- **Example (rounding):** `repr(Temperature(21.55)) == 'Temperature(21.6C)'` (Python's own `:.1f` rounding, not anything you write by hand).
- **Tricky case (float representation):** `repr(Temperature(-273.15)) == 'Temperature(-273.1C)'` -- this one looks like it should round to `-273.2`, but `-273.15` is **not exactly representable in binary floating point**: the actual stored value is a hair above `-273.15`, so `:.1f` rounds it toward `-273.1`. This is exactly why the spec says "Python's normal `:.1f` rounding behavior," not a hand-rolled rounding rule.

**`__eq__` examples:**

- **Example:** `Temperature(10.0) == Temperature(10.0)` is `True`.
- **Tricky case (within tolerance):** `Temperature(10.0) == Temperature(10.0 + 1e-12)` is `True` (well within the `1e-9` tolerance).
- **Example (outside tolerance):** `Temperature(10.0) == Temperature(10.1)` is `False` (the difference is `0.1`, far outside tolerance).
- **Tricky case (non-`Temperature`):** `Temperature(10.0) == 5` is `False`, not a raised exception (`__eq__` returns `NotImplemented`, and Python **falls back to `False`** once neither side knows how to compare).

**`__lt__` examples:**

- **Example:** `Temperature(10.0) < Temperature(20.0)` is `True`; `Temperature(20.0) < Temperature(10.0)` is `False`.
- **Error case (non-`Temperature`):** `Temperature(10.0) < 5` raises **`TypeError`** (`__lt__` returns `NotImplemented` for a non-`Temperature`, and unlike `==`, Python has no fallback for `<` once both sides give up).

## Examples at a glance

To make every member concrete at once, here is **one** representative
`Temperature`, `t = Temperature(100.0)` (the boiling point of water at
sea level, in Celsius), and what every member returns for it or for a
nearby edge case.

| Call | Returns | Why |
|------|---------|-----|
| `t.celsius`                              | `100.0`  | the getter just returns the stored value |
| `t.fahrenheit`                           | `212.0`  | `F = C * 9/5 + 32` = `100 * 9/5 + 32` = `180 + 32` |
| `t.kelvin`                               | `373.15` | `K = C + 273.15` = `100 + 273.15` |
| `repr(t)`                                | `'Temperature(100.0C)'` | `:.1f` formats a whole number with one trailing zero decimal |
| `Temperature.is_physical(-273.15)`       | `True`   | the check is `>=`, so absolute zero itself is physical, not just above it |
| `Temperature.is_physical(-273.16)`       | `False`  | anything colder than absolute zero is not physically possible |
| `Temperature(-300.0)`                    | raises `ValueError` | `__init__` assigns through the `celsius` setter, which rejects non-physical values before the object even exists |
| `Temperature.from_fahrenheit(212.0).celsius` | `100.0` | `(212 - 32) * 5/9 = 180 * 5/9 = 100.0`, the boiling point round-trips exactly |
| `Temperature.from_kelvin(373.15).celsius`    | `100.0` | `373.15 - 273.15 = 100.0` |
| `Temperature(10.0) == Temperature(10.0 + 1e-12)` | `True` | the two values differ by far less than the `1e-9` tolerance, so they still compare equal |
| `Temperature(10.0) < 5`                  | raises `TypeError` | `__lt__` returns `NotImplemented` for a non-`Temperature`; once both sides give up, Python raises `TypeError` for you |

## Worked example: watch `Temperature.from_fahrenheit(98.6)` build a `Temperature`, step by step

This traces the classmethod that most people get wrong first (forgetting
to subtract 32 before multiplying), using human body temperature as the
input, ending exactly where `t.celsius == 37.0`.

| Step | Expression | Value | Why |
|------|-----------|-------|-----|
| 1 | `f` | `98.6` | the Fahrenheit value passed in |
| 2 | `f - 32.0` | `66.6` | subtract 32 first -- this is the step that is easy to skip |
| 3 | `(f - 32.0) * 5.0` | `333.0` | multiply by 5 before dividing, to match the exact formula `(F - 32) * 5 / 9` |
| 4 | `(f - 32.0) * 5.0 / 9.0` | `37.0` | divide by 9 last; this is the Celsius value that gets passed to `cls(...)` |
| 5 | `cls(37.0)` runs `__init__`, which assigns `self.celsius = 37.0` | -- | assignment goes through the `celsius` property setter, not a bare attribute write |
| 6 | the setter calls `Temperature.is_physical(37.0)` | `True` | `37.0 >= -273.15`, so the value is accepted and stored in `self._celsius` |
| end | `Temperature.from_fahrenheit(98.6).celsius` | `37.0` | the classmethod returns the new instance; reading `.celsius` gives back the stored value |

### Examples

```python
>>> t = Temperature(21.5)
>>> repr(t)
'Temperature(21.5C)'
>>> t.fahrenheit
70.7
>>> Temperature.from_fahrenheit(32.0).celsius
0.0
>>> Temperature.from_fahrenheit(-40.0).celsius
-40.0
>>> Temperature.is_physical(-273.15)
True
>>> Temperature.is_physical(-273.16)
False
>>> t.celsius = -1000.0
Traceback (most recent call last):
    ...
ValueError: celsius cannot be below absolute zero (-273.15)
>>> Temperature(10.0) == Temperature(10.0 + 1e-12)
True
>>> Temperature(10.0) < Temperature(20.0)
True
```

## Files

| File | Purpose |
|------|---------|
| `temperature.py` | Write your implementation here |

## Compilation and Testing

```bash
python -m pytest visible-tests/test_visible.py -v
```

## Constraints

- Do not rename `temperature.py`, or rename/remove any method.
- Type hints are required on every method's parameters and return type.
- `temperature.py` must not import `dataclasses`, `functools`,
  `collections`, `enum`, `attr`/`attrs`, or `pint` -- write the property,
  classmethod, staticmethod, and dunder logic yourself rather than
  reaching for a shortcut that generates it for you.
- **Type-annotation bonus (10 pts):** every method and function must annotate all of its parameters (except a leading `self`/`cls`) and its return type. The bonus is awarded only when everything is fully annotated; a separate, informational [ty](https://docs.astral.sh/ty/) check then flags any annotation on `temperature.py` that does not hold up.

## Grading

| Component                           | Points |
|--------------------------------------|--------|
| Import constraints (gate)            | 5      |
| Visible correctness tests            | 35     |
| Hidden correctness tests             | 50     |
| Complete type annotations (bonus)    | 10     |
| **Total**                            | **100** |

## Submission

Submit your implementation as `temperature.py`. Do not rename it.

## Going further

- Add a `Fahrenheit` or `Kelvin` subclass whose `__repr__` reports its
  own unit instead of Celsius, and confirm `from_fahrenheit` /
  `from_kelvin` still build the right subclass when called through it.
- Implement `__le__`, `__gt__`, and `__ge__` by hand, or look up
  `functools.total_ordering` (outside this assignment's constraints) and
  read how it derives the rest from just `__eq__` and `__lt__`.
- What would change if `celsius` were stored as a `Decimal` instead of a
  `float`? Would the `1e-9` equality tolerance still make sense?
