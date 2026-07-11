# Fraction Arithmetic

A class is a promise about what state is reachable. `Fraction` promises that
every instance you ever observe -- no matter which constructor built it or
which method last touched it -- represents a rational number in a single
canonical form (one standard way of writing the value, so that two fractions
which are mathematically equal are always stored identically). You will
implement that promise.

## Learning goals

- Implement a class with private data and a small, deliberate public
  interface (the set of methods and constructors code outside the class is
  allowed to call)
- Maintain invariants (facts about an object's data that must stay true no
  matter which constructor or method last touched it) across every
  constructor and every mutating-looking operation, even though `Fraction`
  itself never mutates after construction
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

## Examples at a glance

To make the invariants concrete, here is what every operation produces for
two representative fractions, `a = 3/6` and `b = 1/3`. Note that `3/6` is
constructed with the two-argument constructor and is expected to already
show up reduced -- that reduction is the whole point of the invariant.

| Expression | Result (`num`/`den`) | `to_string()` | Why |
|---|---|---|---|
| `Fraction(3, 6)` | `1`/`2` | `"1/2"` | `3/6` and `1/2` are the same rational number, so the constructor reduces by `gcd(3, 6) = 3` immediately -- there is no separate "unreduced" `Fraction` you can ever observe |
| `Fraction(3, -4)` | `-3`/`4` | `"-3/4"` | the denominator came in negative, so the constructor flips the sign of both numerator and denominator, moving the minus sign onto the numerator |
| `Fraction(-3, -4)` | `3`/`4` | `"3/4"` | two negatives cancel: flipping both signs (because the denominator was negative) turns `-3/-4` into `3/4` |
| `Fraction(0, 5)` | `0`/`1` | `"0"` | zero is always normalized to `0/1`, regardless of what denominator it was built with |
| `Fraction(6, 2)` | `3`/`1` | `"3"` | a whole number is a fraction whose denominator reduces to `1`; `to_string()` drops the `/1` entirely |
| `a.plus(b)` = `(3/6).plus(1/3)` | `5`/`6` | `"5/6"` | `1/2 + 1/3` cross-multiplies to `(1*3 + 1*2)/(2*3) = 5/6`, already in lowest terms |
| `a.minus(b)` | `1`/`6` | `"1/6"` | `1/2 - 1/3 = (1*3 - 1*2)/(2*3) = 1/6` |
| `a.times(b)` | `1`/`6` | `"1/6"` | `1/2 * 1/3 = 1/6`, numerators and denominators multiply directly |
| `a.dividedBy(b)` | `3`/`2` | `"3/2"` | `1/2 / (1/3)` is `1/2 * 3/1 = 3/2` -- dividing swaps `b`'s numerator and denominator before multiplying |
| `a.equals(Fraction(1, 2))` | -- | `true` | `3/6` reduces to `1/2` before comparison, so the raw digits `3` and `6` never even get compared |
| `b.lessThan(a)` | -- | `true` | `1/3 < 1/2` |
| `a.lessThan(b)` | -- | `false` | `1/2` is not less than `1/3` |
| `Fraction(-1, 2).lessThan(b)` | -- | `true` | a negative fraction is always less than a positive one |
| `Fraction(1, 2).dividedBy(Fraction(0))` | -- | unspecified | dividing by a zero-valued `Fraction` violates `dividedBy`'s precondition -- see Contract below |
| `Fraction(1, 0)` | -- | unspecified | a zero denominator violates the two-argument constructor's precondition -- see Contract below |

## Worked example: watch `1/4 + 1/6` reduce, step by step

This is the single most important thing to understand in the assignment:
`plus` never returns an already-reduced pair of numbers by luck -- reduction
happens because the result is built through the two-argument constructor,
the one place the invariant is enforced. Trace `Fraction(1, 4).plus(Fraction(1, 6))`:

| Step | What happens | Value | Why |
|------|---------------|-------|-----|
| 1 | Read `this`'s parts | `numerator_ = 1`, `denominator_ = 4` | `this` is `1/4` |
| 2 | Read `other`'s parts | `other.numerator_ = 1`, `other.denominator_ = 6` | `other` is `1/6` |
| 3 | Cross-multiply the numerator | `1*6 + 1*4 = 10` | this is the standard "common denominator" cross-multiply for `a/b + c/d = (a*d + c*b)/(b*d)` |
| 4 | Multiply the denominators | `4*6 = 24` | the common denominator before any reduction |
| 5 | Construct `Fraction(10, 24)` | -- | `plus` never touches `numerator_`/`denominator_` directly -- it hands the raw, unreduced pair to the constructor |
| 6 | Constructor checks sign | denominator `24` is already positive | no sign flip needed |
| 7 | Constructor checks for zero | numerator `10` is not `0` | skip the zero-normalization branch |
| 8 | Constructor computes `gcd(10, 24)` | `2` | `10 = 2*5`, `24 = 2*12`, and `5` and `12` share no more common factors |
| 9 | Divide both by the gcd | `10/2 = 5`, `24/2 = 12` | this is the reduction step -- the fraction is now in lowest terms |
| end | Result | `Fraction` with `num() == 5`, `den() == 12` | `1/4 + 1/6 = 3/12 + 2/12 = 5/12`, matching `to_string() == "5/12"` |

Every arithmetic method (`plus`, `minus`, `times`, `dividedBy`) follows this
same pattern: compute a raw, possibly-unreduced numerator/denominator pair
using ordinary fraction arithmetic, then hand that pair to the two-argument
constructor and let it re-establish the invariant. None of them ever
duplicate the reduction logic themselves.

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

### Per-method examples

**`Fraction()`** -- the default constructor.

- **Example (default value):** `Fraction().num() == 0`, `Fraction().den() ==
  1`, `Fraction().to_string() == "0"`.

**`Fraction(int n)`** -- a whole number.

- **Example (positive/zero/negative):** `Fraction(5).to_string() == "5"`;
  `Fraction(0).to_string() == "0"`; `Fraction(-5).num() == -5`.

**`Fraction(int numerator, int denominator)`** -- reduces and normalizes sign.

- **Example (reduces to lowest terms):** `Fraction(3, 6).num() == 1`,
  `Fraction(3, 6).den() == 2` -- **reduced by `gcd(3, 6) == 3`**.
- **Example (sign moves to numerator):** `Fraction(3, -4).num() == -3`,
  `Fraction(3, -4).den() == 4` -- **sign moved onto the numerator**.
- **Example (zero normalizes):** `Fraction(0, 5).to_string() == "0"` --
  **zero always normalizes to `0/1`**.
- **Error case (zero denominator):** `Fraction(1, 0)` violates the
  precondition (denominator must not be `0`) -- **behavior is
  unspecified**, see Contract below.

**`plus`/`minus`/`times`/`dividedBy`** -- return a new, already-reduced
`Fraction`; none of them mutate `*this` or `other`.

- **Example (`plus`):** `Fraction(3, 6).plus(Fraction(1, 3)).to_string() ==
  "5/6"`.
- **Example (`times`, sign):** `Fraction(-1, 2).times(Fraction(2,
  3)).to_string() == "-1/3"` -- **a negative times a positive stays
  negative**, and the result is still reduced.
- **Example (`dividedBy`, sign):** `Fraction(1, 2).dividedBy(Fraction(-1,
  3)).to_string() == "-3/2"` -- **dividing by a negative fraction flips the
  sign**.
- **Error case (divide by zero):** `Fraction(1, 2).dividedBy(Fraction(0))`
  violates `dividedBy`'s precondition (the argument must not be
  zero-valued) -- **behavior is unspecified**.

**`equals`/`lessThan`** -- compare by value, not by raw digits.

- **Example (`equals` after reduction):** `Fraction(2, 4).equals(Fraction(1,
  2)) == true` -- **both reduce to `1/2`** before comparison.
- **Example (`lessThan`):** `Fraction(1, 3).lessThan(Fraction(1, 2)) ==
  true`.
- **Example (negative vs. positive):** `Fraction(-1, 2).lessThan(Fraction(1,
  3)) == true` -- **any negative fraction is less than any positive one**.

**`to_string()`** -- renders the reduced value.

- **Example (whole number):** `Fraction(6, 2).to_string() == "3"` --
  **whole numbers drop the denominator**.
- **Example (negative):** `Fraction(3, -4).to_string() == "-3/4"`.
- **Example (zero):** `Fraction(0, 5).to_string() == "0"`.

### Contract

A function's contract is the set of conditions its caller must satisfy for
the function to behave as documented; a condition the caller must guarantee
before calling is called a precondition. Passing `denominator == 0` to the
two-argument constructor, or calling `dividedBy()` with a `Fraction` whose
value is zero, violates this contract. You do not need to handle these
cases -- behavior is unspecified and no test (visible or hidden) calls your
code this way.

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

- Learn about operator overloading (giving special meaning to operators like
  `+` and `==` when used with your own class) and rewrite `plus`, `equals`, and
  `lessThan` as `operator+`, `operator==`, and `operator<` so that
  `a + b == c` reads naturally. What has to change about the class for this
  to work, and what stays the same?
- Replace your hand-rolled GCD loop with `std::gcd` from `<numeric>`
  (C++17). Compare the two implementations.
- Add a function that renders a mixed number instead of an improper
  fraction -- `7/2` becomes `"3 1/2"`. Decide how to handle negative mixed
  numbers and fractions less than one.
