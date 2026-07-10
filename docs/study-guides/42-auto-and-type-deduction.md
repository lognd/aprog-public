# Study Guide 42: auto & Type Deduction

This module drills one specific, learnable rule -- `auto` strips
reference-ness and top-level `const`, then you must re-add whichever of
those you actually wanted -- through pure type-naming questions and then
through programs where the rule visibly changes printed output.

## Know before you start

- `const` vs. top-level const vs. const-through-a-pointer [assumed: row
  13 -- Const]
- References vs. pointers vs. value copies [assumed: row 11 -- Pointers]
- `std::map` storing `std::pair<const K, V>` [assumed: row 33 -- Map & Set
  ADT]
- Range-for's desugaring into begin()/end()/operator*/operator++
  [assumed: row 35 -- Iterators]

## Taught here

Concept: the strip-then-requalify rule
- Know the core rule: `auto` deduces a stripped value type -- with any
  reference-ness and any top-level `const` removed -- no matter what the
  initializer expression's own type actually was; if a reference or the
  `const` is wanted, it must be written explicitly as `auto&` or
  `const auto&`, since `auto` never adds either back on its own.
- Know "top-level `const`" means a `const` applying directly to the
  variable itself (`const int cx`), as distinct from a `const` reached
  through a pointer/reference to something else (`const int* p` -- `p`
  itself is not const); only top-level `const` gets stripped by `auto`.
- Know `auto*` is used for pointer-typed declarations.
- Know `decltype(expr)` is a different tool: applied to a plain existing
  variable name, it reproduces that variable's EXACT declared type with
  nothing stripped -- the opposite instinct from `auto`.
- Know a double-quoted string literal like `"hi"` has type `const
  char[N]`, decaying to `const char*` -- `auto` never upgrades it to
  `std::string`, since `auto` only reports the initializer's actual type.
- Know `auto` on a function returning a reference drops the reference,
  producing an independent copy; `auto&` is the fix that keeps the live
  link to the original.
- Know range-for over a `std::map` deduces `std::pair<const K, V>` for
  its element type regardless of whether `&` is added, because that is
  literally what `std::map` stores -- the key half stays `const` either
  way.

Concept: observable consequences of auto's rules
- Know `auto` (copy) vs. `auto&` (reference) to the same original
  variable produce two independent storage locations from that point on
  except that the `auto&` one IS the original -- only the `auto&` one's
  mutation is visible through the original variable afterward.
- Know range-for over a `std::vector<int>` with plain `auto` mutates only
  a throwaway per-iteration copy (no effect on the vector); `auto&`
  mutates the vector's real elements in place.
- Know a numeric literal's exact type decides which arithmetic operation
  executes: `7 / 2` with both operands plain `int` performs integer
  division (truncates toward zero, giving `3`), while the moment either
  operand is floating-point the whole expression promotes to
  floating-point arithmetic and keeps the fractional result.
- Know the conditional operator `?:` requires one common result type for
  BOTH branches, computed at compile time, even though only one branch's
  value is ever actually selected at run time -- this can silently
  promote an int branch to match a double branch's type.
- Know `auto` on a string literal never gives you a `.size()` member
  (there is no `std::string` involved) -- `strlen` is the tool for a raw
  `const char*`'s length instead.

## Study checklist

- [ ] State the strip-then-requalify rule from memory and apply it to a
      new snippet.
- [ ] Distinguish top-level const from const-through-a-pointer, and know
      which one auto strips.
- [ ] Explain why auto never deduces std::string from a string literal.
- [ ] Predict output for an auto copy vs. an auto& reference after one is
      mutated.
- [ ] Explain why 7 / 2 differs from 7.0 / 2 and how auto reports the
      difference.
- [ ] Explain what std::map's range-for element type is under auto vs.
      auto&, and why the const K half never goes away.

## Practiced in

`deduction-detective`, `auto-consequences`
