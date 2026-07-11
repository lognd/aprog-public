# temperature-lab -- starter file.
#
# Implement a Temperature class that stores a temperature internally in
# degrees Celsius, with two alternate constructors, a physical-range
# check, a validated property, two read-only computed properties, and
# three dunder methods. See README.md for the exact spec of each member.
#
# Do not rename this file. Do not import anything except (optionally)
# typing -- every function here is implementable with plain Python, no
# standard-library modules required (the reference solution uses none).
#
# The signatures below are left UNANNOTATED on purpose: the type-annotation
# bonus asks you to add the parameter and return-type hints yourself (the
# exact types are in the README). A classmethod that returns its own class
# annotates its return as "Temperature" (a string, because the class is not
# finished being defined at that point).


class Temperature:
    """A physical temperature, stored internally in degrees Celsius."""

    # TODO: a class attribute, absolute_zero, holding -273.15.

    def __init__(self, celsius):
        """Construct from a Celsius value; rejects anything below absolute zero."""
        raise NotImplementedError

    @classmethod
    def from_fahrenheit(cls, f):
        """Build a Temperature from a Fahrenheit value: C = (F - 32) * 5/9."""
        raise NotImplementedError

    @classmethod
    def from_kelvin(cls, k):
        """Build a Temperature from a Kelvin value: C = K - 273.15."""
        raise NotImplementedError

    @staticmethod
    def is_physical(celsius):
        """Return True if celsius is at or above absolute zero (-273.15)."""
        raise NotImplementedError

    # TODO: a celsius property (getter + setter). The setter must raise
    # ValueError for any value that is not physical (below absolute zero).

    # TODO: a read-only fahrenheit property: F = C * 9/5 + 32.

    # TODO: a read-only kelvin property: K = C + 273.15.

    def __repr__(self):
        """Exact format: Temperature(<celsius to one decimal place>C)."""
        raise NotImplementedError

    def __eq__(self, other):
        """Equal if both are Temperature and their celsius values differ by < 1e-9."""
        raise NotImplementedError

    def __lt__(self, other):
        """Ordered by celsius value."""
        raise NotImplementedError
