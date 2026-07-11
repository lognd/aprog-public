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

### Physical-range check

```python
@staticmethod
def is_physical(celsius: float) -> bool:
    """True if celsius >= absolute_zero."""
```

A pure function of its `celsius` argument. It needs neither `self` nor
`cls` -- it is grouped inside `Temperature` purely for organization.

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
- A clean run of [ty](https://docs.astral.sh/ty/) (a fast, modern Python
  type checker, run over `temperature.py`) earns a bonus.

## Grading

| Component                           | Points |
|--------------------------------------|--------|
| Import constraints (gate)            | 5      |
| Visible correctness tests            | 35     |
| Hidden correctness tests             | 50     |
| Clean `ty` type-check (bonus)        | 10     |
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
