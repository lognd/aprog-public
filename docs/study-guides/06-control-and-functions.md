# Study Guide 6: Control & Functions

This module covers the mechanics of control flow (loops, conditionals,
scope) and function calls, plus the cost of algorithms as their input
grows. Students learn to read compiler warnings, benchmark output, and Big-O
behavior, then apply complexity-aware thinking to writing number-theory
functions with hard performance requirements.

## Know before you start

- Basic control-flow syntax (`if`, `for`, `while`) and function declarations
  [assumed: row 4 -- Command-Line & Compilation]
- A working `g++`/`make` build setup [assumed: row 2 -- Environment Setup]

## Taught here

Concept: Big-O complexity
- Know that O(...) ("big-O") notation describes how an algorithm's running
  time grows as its input size N grows: O(N) means cost grows in direct
  proportion to N, O(N^2) means cost grows proportional to N multiplied by
  itself.
- Know that calling a function N times does not make the total cost O(N) by
  itself -- if the called function itself does O(N) work per call, the
  total becomes O(N^2).
- Be able to read wall-clock benchmark timing output and identify which of
  several equivalent functions is asymptotically slower, distinguishing how
  code looks (nested loops, helper calls) from what it actually costs to
  execute.
- Be able to work out, for concrete small N, why a triangular-loop-style
  cost (1+2+...+N = N*(N+1)/2) grows quadratically: doubling N roughly
  quadruples the total work.

Concept: scope
- Know that every name in C++ has a scope: the region of the program where
  it is visible, determined by the curly braces `{ }` that contain its
  declaration.
- Know that a variable lives from the line where it is declared to the `}`
  that closes its containing block.
- Know that variable shadowing occurs when a declaration inside a nested
  block reuses the name of an outer variable, hiding the outer one for the
  rest of that block.
- Know that a `static` local variable is initialized only once (the first
  time the function runs) and retains its value across subsequent calls to
  the same function, unlike an ordinary local variable which is
  re-initialized every call.
- Know that a variable declared inside a `for` loop's body is a fresh
  variable on every iteration, distinct from a same-named variable declared
  outside the loop.
- Be able to read a compiler warning (for example from `-Wshadow`) as a
  diagnostic clue pointing at a real scope bug, not just noise.

Concept: control-flow operators
- Know that `&&` and `||` are short-circuiting: `&&` skips evaluating its
  right operand if the left is `false`, and `||` skips its right operand if
  the left is `true`.
- Know that `break` exits a loop immediately, and `continue` skips the rest
  of the current loop iteration's body without exiting the loop.
- Know De Morgan's law: `!(A && B)` is equivalent to `!A || !B`, and
  `!(A || B)` is equivalent to `!A && !B`.

Concept: number-theory algorithms under complexity constraints
- Be able to implement primality testing in O(sqrt(n)) using trial division
  up to the square root, rather than the naive O(n) loop that checks every
  divisor up to n.
- Know that the Euclidean algorithm computes the greatest common divisor by
  repeated division (rather than counting down from min(a, b)), and that it
  is asymptotically faster.
- Be able to write an iterative (loop-based) Fibonacci function to avoid
  the exponential call growth of a naive recursive version, where the
  number of calls roughly doubles at every step.

## Study checklist

- [ ] Explain why a function called N times, where each call does O(N)
      work, is O(N^2) overall, not O(N).
- [ ] Given a snippet with a `static` local variable, predict its value
      across multiple calls.
- [ ] Explain the difference between `break` and `continue`.
- [ ] State De Morgan's law and apply it to simplify a negated condition.
- [ ] Explain why trial division up to sqrt(n) is sufficient to test
      primality.

## Practiced in

`complexity-clock`, `scope-safari`, `control-gauntlet`, `number-toolkit`
