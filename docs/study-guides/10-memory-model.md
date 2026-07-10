# Study Guide 10: Memory Model (heap vs. stack, call stack, recursion)

This module builds the mental model of where a C++ variable actually lives
in memory (stack, heap, or static storage) and how the call stack grows and
shrinks as functions call each other, especially recursively. It ends with
building an entire arithmetic system out of nothing but recursive
successor calls.

## Know before you start

- Basic function calls and recursion syntax [assumed: row 6 -- Control &
  Functions]
- That `std::array` lives on the stack and `std::vector` lives on the heap,
  as a first informal introduction [assumed: row 7 -- Standard Library
  Types]

## Taught here

Concept: the four memory regions and storage duration
- Know the four categories used to classify any C++ variable declaration:
  stack/block-scoped, stack/function-scoped, static/program-duration
  (globals and `static` locals), and heap/manually-managed.
- Know that the stack holds function call frames; each call pushes a frame
  and each return pops one, with local variables and parameters living in
  the current frame.
- Know that block-scoped stack variables are released when their enclosing
  block ends, even though the containing function's frame is still active.
- Know that heap allocation (`new`/`delete`, `malloc`/`free`) gives the
  programmer explicit, manual control over an object's lifetime,
  independent of any function call frame.
- Know that static storage duration means a variable (a global, or a
  `static` local) lives for the entire program run; uninitialized ones go
  in the BSS segment (zero-initialized by the OS before `main` runs) and
  initialized ones go in the Data segment.
- Be able to classify any given C++ declaration into one of the four
  storage categories by reading its syntax (where it is declared and
  whether it uses `new`/`static`/neither).

Concept: the call stack and recursion mechanics
- Know that a stack frame is the block of memory holding one function
  call's local variables and return address.
- Know that recursion (a function calling itself, directly or through a
  chain of other functions) has both a time cost (how many calls happen)
  and a space cost (how many stack frames are alive simultaneously at the
  deepest point).
- Be able to trace a call tree by hand to count total calls and maximum
  simultaneous stack depth for a small recursive function.
- Know that naive recursion (like naive Fibonacci) exhibits exponential
  call growth, memoization (caching each result the first time it is
  computed so repeated inputs are looked up instead of recomputed) reduces
  that to linear growth, and an iterative rewrite avoids both the call-count
  explosion and the stack-depth growth entirely.
- Know that code written after a recursive call in the same function runs
  during stack unwinding -- on the way back out of the recursion, not on
  the way in.
- Know that a heap object created with `new` outlives the function that
  created it, unlike a stack local which is destroyed when its function
  returns.

Concept: reading a stack-overflow crash report
- Know that a stack trace lists every function active at the moment of a
  crash, with frame numbers, addresses, function names, and source lines.
- Know that AddressSanitizer (ASan), a compiler-inserted runtime checker,
  can detect a stack overflow -- the crash that happens when unbounded
  recursion exhausts the space reserved for stack frames.
- Know that a missing base case (the condition meant to stop recursion) is
  the classic cause of unbounded/infinite recursion, and that a program can
  survive thousands of recursive calls before crashing because the stack
  has a fixed but fairly large size limit.
- Know that compiling with `-g` embeds debug symbols (including source line
  numbers) into a binary, which is why a stack trace shows meaningful
  function names and lines only when the program was built with `-g`.

Concept: recursion as a substitute for iteration
- Be able to build arithmetic (addition, multiplication, exponentiation)
  entirely from a single recursive successor primitive, with no loops and
  no built-in arithmetic operators outside a designated primitive.
- Know the difference between a function's precondition (what must be true
  of its inputs before it is called) and an edge case (a boundary input,
  like zero, where bugs like to hide).
- Be able to identify the base case (the input handled directly, with no
  further recursive call) and the recursive case (every other input,
  handled by calling the function again on a smaller piece of the problem)
  for a recursively defined arithmetic function.
- Know the term "mutually recursive functions": functions that call each
  other in a chain (for example, `multiply` built from `add`, `add` built
  from `successor`), rather than a single function calling only itself.

## Study checklist

- [ ] Classify five example C++ declarations by storage location and
      lifetime.
- [ ] Trace the call tree of naive recursive `fib(5)` and count total calls
      and maximum stack depth.
- [ ] Explain why code placed after a recursive call runs during unwinding.
- [ ] Given an ASan stack-overflow report, identify that the cause is a
      missing base case.
- [ ] Define `add` in terms of `successor` and identify its base case.

## Practiced in

`stack-heap-bingo`, `recursion-unwind`, `call-stack-autopsy`, `stack-heap-safari`, `peano-math`
