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
# Type hints are REQUIRED on every method signature.


class Temperature:
    """A physical temperature, stored internally in degrees Celsius."""

    # TODO: a class attribute, absolute_zero, holding -273.15.

    def __init__(self, celsius: float) -> None:
        """Construct from a Celsius value; rejects anything below absolute zero."""
        raise NotImplementedError

    @classmethod
    def from_fahrenheit(cls, f: float) -> "Temperature":
        """Build a Temperature from a Fahrenheit value: C = (F - 32) * 5/9."""
        raise NotImplementedError

    @classmethod
    def from_kelvin(cls, k: float) -> "Temperature":
        """Build a Temperature from a Kelvin value: C = K - 273.15."""
        raise NotImplementedError

    @staticmethod
    def is_physical(celsius: float) -> bool:
        """Return True if celsius is at or above absolute zero (-273.15)."""
        raise NotImplementedError

    # TODO: a celsius property (getter + setter). The setter must raise
    # ValueError for any value that is not physical (below absolute zero).

    # TODO: a read-only fahrenheit property: F = C * 9/5 + 32.

    # TODO: a read-only kelvin property: K = C + 273.15.

    def __repr__(self) -> str:
        """Exact format: Temperature(<celsius to one decimal place>C)."""
        raise NotImplementedError

    def __eq__(self, other: object) -> bool:
        """Equal if both are Temperature and their celsius values differ by < 1e-9."""
        raise NotImplementedError

    def __lt__(self, other: "Temperature") -> bool:
        """Ordered by celsius value."""
        raise NotImplementedError
