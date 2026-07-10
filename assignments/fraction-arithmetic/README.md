# Fraction Arithmetic

A class is a promise about what state is reachable. `Fraction` promises that
every instance you ever observe -- no matter which constructor built it or
which method last touched it -- represents a rational number in a single
canonical form. You will implement that promise.

## Learning goals

- Implement a class with private data and a small, deliberate public interface
- Maintain invariants across every constructor and every mutating-looking
  operation, even though `Fraction` itself never mutates after construction
- Use `const` member functions to express "this method reads but never
  changes the object"
- Practice returning new objects from arithmetic operations instead of
  mutating in place
- Reduce fractions to lowest terms using the greatest common divisor

## Background

Encapsulation means the private members of a class (`numerator_`,
`denominator_` here) are only ever touched through the class's own methods.
The payoff is that the class can guarantee something about its data that no
caller could guarantee on their own.

For `Fraction`, that guarantee is a set of invariants:

1. The fraction is always stored in lowest terms.
2. The denominator is always strictly positive -- sign lives in the
   numerator.
3. Zero is always normalized to `0/1`.

Why bother? Consider what happens if you *don't* enforce these invariants.
Suppose two fractions are "equal" only when their raw numerator and
denominator match exactly. Without reduction, `1/2` and `2/4` would compare
unequal even though they represent the same number -- every caller of
`equals` would need to remember to reduce first, and the bug would resurface
every time someone forgets. Suppose the sign could live on either the
numerator or the denominator. Then `-1/2` and `1/-2` would need special-casing
everywhere a fraction's sign is checked, and printing `to_string` would need
to guess which side the minus sign is on.

By enforcing both invariants inside the constructor -- the one place all
`Fraction` values are born -- every other method (`plus`, `equals`,
`to_string`, ...) can simply trust that the denominator is positive and the
fraction is already reduced. The invariant is established once and never
has to be re-checked.

This is also why `num()`, `den()`, `plus()`, `equals()`, and friends are all
marked `const`: they promise the caller they will not modify the `Fraction`
they are called on. Arithmetic methods do not mutate `*this`; they construct
and return a brand-new `Fraction`, which re-establishes the invariants for
the result through the same constructor.

## Task

Implement every method declared in `fraction.hpp` inside `fraction.cpp`.

```cpp
class Fraction {
public:
    Fraction();
    Fraction(int n);
    Fraction(int numerator, int denominator);

    int num() const;
    int den() const;

    Fraction plus(const Fraction& other) const;
    Fraction minus(const Fraction& other) const;
    Fraction times(const Fraction& other) const;
    Fraction dividedBy(const Fraction& other) const;

    bool equals(const Fraction& other) const;
    bool lessThan(const Fraction& other) const;

    std::string to_string() const;
    // ...
};
```

The two-argument constructor is the only place reduction and sign
normalization need to happen from scratch: divide both numerator and
denominator by their greatest common divisor, then flip the sign of both if
the denominator came in negative, so that the denominator ends up positive.
Every other constructor and method can be written in terms of this one.

`to_string()` renders `"3/4"` for a proper fraction, `"-3/4"` when negative,
and drops the denominator entirely for whole numbers -- `"5"`, not `"5/1"`
-- including `"0"` for zero.

### Contract

Passing `denominator == 0` to the two-argument constructor, or calling
`dividedBy()` with a `Fraction` whose value is zero, is a precondition
violation. You do not need to handle these cases -- behavior is unspecified
and no test (visible or hidden) calls your code this way.

## Files

| File | Purpose |
|------|---------|
| `fraction.hpp` | Declarations and invariant contract -- do not modify |
| `fraction.cpp` | Write your implementation here |
| `visible-tests/test_catch.cpp` | Visible Catch2 tests you can run locally |

## Compilation and Testing

Build and run the visible tests locally:

```bash
g++ -std=c++17 -Wall -Wextra -Werror \
    -I. fraction.cpp visible-tests/test_catch.cpp \
    -o fraction_tests
./fraction_tests
```

You will need Catch2 installed, or you can fetch it via CMake. The grader
uses CMake internally; see `visible-tests/CMakeLists.txt` for details.

## Constraints

- Do not modify `fraction.hpp`.
- Do not use inheritance, templates, or operator overloading -- use the named
  methods (`plus`, `minus`, `times`, `dividedBy`, `equals`, `lessThan`) instead.
- Do not throw exceptions.
- Do not use `new` or dynamic memory of any kind.
- The denominator returned by `den()` must always be strictly positive.
- Every fraction you produce must already be in lowest terms.

---

## Grading

| Component | Points |
|-----------|--------|
| Compilation | 0 (required to proceed) |
| No `throw` / `new` (source check) | 10 |
| Visible tests (Catch2) | 25 |
| Hidden tests (Catch2) | 65 |
| **Total** | **100** |

The compilation check is a gate: if your code does not compile, no further
tests run.

## Submission

Submit a single file named `fraction.cpp`. Do not rename it.

---

## Going further

- Learn about operator overloading and rewrite `plus`, `equals`, and
  `lessThan` as `operator+`, `operator==`, and `operator<` so that
  `a + b == c` reads naturally. What has to change about the class for this
  to work, and what stays the same?
- Replace your hand-rolled GCD loop with `std::gcd` from `<numeric>`
  (C++17). Compare the two implementations.
- Add a function that renders a mixed number instead of an improper
  fraction -- `7/2` becomes `"3 1/2"`. Decide how to handle negative mixed
  numbers and fractions less than one.
