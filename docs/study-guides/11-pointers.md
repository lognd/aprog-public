# Study Guide 11: Pointers (pass modes, arrays as pointers, arithmetic)

This module teaches the three ways C++ hands a variable to a function
(value, reference, pointer), what an address and a dereference actually
are, and how to navigate arrays and matrices using pointer arithmetic
instead of subscript notation.

## Know before you start

- Function declarations and calls [assumed: row 6 -- Control & Functions]
- That heap objects created with `new` outlive the function that created
  them, and that stack locals do not [assumed: row 10 -- Memory Model]

## Taught here

Concept: the three pass modes
- Know that pass by value (`void f(int x)`) gives the function an
  independent copy in its own stack slot; changes inside the function never
  affect the caller's variable.
- Know that pass by reference (`void f(int& x)`) makes the parameter an
  alias for the caller's own storage -- not a copy -- so any modification
  inside the function is visible to the caller.
- Know that pass by pointer (`void f(int* p)`) gives the function a copy of
  an address; the pointer variable itself is a copy, but dereferencing it
  with `*p` reaches the caller's original storage.
- Know the critical distinction: reassigning a pointer parameter (`p =
  &other;`) only changes the function's local copy of the address and is
  invisible to the caller, while modifying the pointee (`*p = 99;`) writes
  through to the caller's actual object and is visible.
- Be able to explain why a function that swaps two `int*` parameters by
  reassigning them (`a = b; b = tmp;`) does not swap the caller's pointers,
  while dereferencing (`*a = *b; *b = tmp;`) does swap the caller's values.
- Be able to choose the right pass mode for a function's actual need: pass
  by value for small read-only types, `const T&` for large read-only types
  (avoids an unnecessary copy), and `T&`/`T*` only when the function must
  modify the caller's variable.

Concept: arrays as pointers
- Know that a function parameter written `int arr[]` is identical to `int*
  arr` -- no copying occurs; the function receives the address of the
  caller's first element and can modify the caller's array directly. This
  is called array-to-pointer decay.
- Know that `arr[i]` is exactly equivalent to `*(arr + i)`; the subscript
  operator is syntactic sugar that the compiler rewrites into pointer
  arithmetic, producing identical machine code.
- Be able to walk an array or C string using pointer increment/decrement
  (`p++`) instead of an index variable, and use the two-pointer technique
  (one pointer at the front, one at the back, moving toward each other) for
  in-place reversal.
- Be able to implement C-string utilities (`strlen`, `strcpy`, `strcmp`)
  from first principles using only pointer arithmetic, advancing a pointer
  until it reaches the null terminator (`'\0'`, the byte that marks where a
  C string's text ends).
- Know that returning `nullptr` is a standard way to signal "not found"
  from a pointer-returning search function, and that callers must check for
  it before dereferencing.

Concept: const with pointers and references
- Know the four combinations of `const` with a pointer, read right-to-left:
  `int*` (mutable pointer to mutable int), `const int*` (mutable pointer to
  const int -- "pointer to const"), `int* const` (const pointer to mutable
  int -- "const pointer"), and `const int* const` (both const).
- Know that `const int*` (or equivalently `int const*`) as a parameter type
  signals to callers "this function will only read your data, not modify
  it."
- Know that a reference has the same two layers of constness: `const int&`
  can only be read through, not written through.
- Know that a reference is an alias, not a pointer wrapper: it cannot be
  null, and once initialized it cannot be rebound to refer to a different
  object -- assigning to it writes through to the referred object instead.
- Know that the standard library forbids `vector<T&>` because references
  cannot be default-constructed or rebound the way vector elements require;
  `vector<T*>` or `vector<std::reference_wrapper<T>>` are the alternatives.

Concept: flat-array representation of 2D data
- Be able to derive and use the row-major offset formula for a 2D matrix
  stored in a flat 1D array: element (row r, column c) lives at offset `r *
  cols + c`.
- Know why a flat `int*` is usually better than an `int**` (array of
  pointers) for a dense matrix: one allocation instead of many, all
  elements contiguous in memory (better CPU cache behavior, since the CPU
  cache favors data that is physically close to recently accessed data),
  and no extra pointer-chasing indirection.
- Know that the out-parameter pattern (a function that fills in a result
  through a pointer parameter instead of returning it) is generally poor
  practice compared to simply returning the value.

## Study checklist

- [ ] Given a function signature using value, reference, or pointer,
      predict whether the caller's variable is modified.
- [ ] Explain why swapping two pointer parameters by reassignment does not
      swap the caller's pointers.
- [ ] Rewrite an `arr[i]` expression as explicit pointer arithmetic.
- [ ] Read right-to-left to classify `const int*` vs `int* const`.
- [ ] Derive the row-major offset formula for a non-square matrix and
      explain why transposing swaps rows and columns in that formula.

## Practiced in

`pass-mode-minefield`, `pointer-matrix`, `pointer-toolkit`
