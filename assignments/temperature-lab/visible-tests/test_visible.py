"""Visible tests for Temperature Lab.

Run locally:
    python -m pytest visible-tests/test_visible.py -v
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from temperature import Temperature  # noqa: E402


def test_init_stores_celsius():
    t = Temperature(21.5)
    assert t.celsius == 21.5


def test_repr_one_decimal_place():
    assert repr(Temperature(21.5)) == "Temperature(21.5C)"


def test_repr_rounds_to_one_decimal():
    assert repr(Temperature(21.55)) == "Temperature(21.6C)"


def test_from_fahrenheit_freezing_point():
    t = Temperature.from_fahrenheit(32.0)
    assert abs(t.celsius - 0.0) < 1e-9


def test_from_fahrenheit_body_temp():
    t = Temperature.from_fahrenheit(98.6)
    assert abs(t.celsius - 37.0) < 1e-6


def test_from_kelvin_absolute_zero():
    t = Temperature.from_kelvin(0.0)
    assert abs(t.celsius - (-273.15)) < 1e-9


def test_is_physical_true_at_absolute_zero():
    assert Temperature.is_physical(-273.15) is True


def test_is_physical_false_below_absolute_zero():
    assert Temperature.is_physical(-273.16) is False


def test_fahrenheit_property_computed():
    t = Temperature(0.0)
    assert abs(t.fahrenheit - 32.0) < 1e-9


def test_kelvin_property_computed():
    t = Temperature(0.0)
    assert abs(t.kelvin - 273.15) < 1e-9


def test_celsius_setter_rejects_impossible_value():
    t = Temperature(0.0)
    try:
        t.celsius = -300.0
    except ValueError:
        pass
    else:
        assert False, "expected ValueError for celsius below absolute zero"
    assert t.celsius == 0.0


def test_fahrenheit_is_read_only():
    t = Temperature(0.0)
    try:
        t.fahrenheit = 100.0
    except AttributeError:
        pass
    else:
        assert False, "expected AttributeError assigning to fahrenheit"


def test_kelvin_is_read_only():
    t = Temperature(0.0)
    try:
        t.kelvin = 100.0
    except AttributeError:
        pass
    else:
        assert False, "expected AttributeError assigning to kelvin"


def test_eq_same_celsius():
    assert Temperature(10.0) == Temperature(10.0)


def test_eq_within_tolerance():
    assert Temperature(10.0) == Temperature(10.0 + 1e-12)


def test_eq_outside_tolerance():
    assert Temperature(10.0) != Temperature(10.1)


def test_lt_ordering():
    assert Temperature(10.0) < Temperature(20.0)
    assert not (Temperature(20.0) < Temperature(10.0))


def test_absolute_zero_is_class_attribute():
    assert Temperature.absolute_zero == -273.15
    assert Temperature(0.0).absolute_zero == -273.15


def test_subclass_from_fahrenheit_returns_subclass():
    class Kelvinator(Temperature):
        pass

    k = Kelvinator.from_fahrenheit(32.0)
    assert isinstance(k, Kelvinator)
    assert abs(k.celsius - 0.0) < 1e-9


def test_from_kelvin_matches_celsius_plus_absolute_zero_magnitude():
    t = Temperature.from_kelvin(373.15)
    assert abs(t.celsius - 100.0) < 1e-9
