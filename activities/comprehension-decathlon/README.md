# Activity: Comprehension Decathlon

A Python comprehension is not a different feature from the `for` loop you
already know -- it is a compact way of writing the exact same
loop-and-collect pattern, evaluated by the same rules underneath. This
activity walks through ten short programs that build that equivalence up
piece by piece: a comprehension placed directly next to the loop it
replaces, filtering with a trailing `if`, the syntax gotcha of an
if/else EXPRESSION (before the `for`, transforms every element) versus a
filtering `if` (after the `for`, can drop elements entirely), dict and
set comprehensions, a nested comprehension that flattens a 2D grid, a
generator expression that never builds a list in memory at all, and the
one genuine scoping difference between a comprehension's loop variable
and a plain `for` loop's.

## Concepts covered

- list comprehensions as a compact rewrite of an explicit `for` loop plus
  `append()`
- filtering with a trailing `if` versus transforming with an if/else
  expression positioned before the `for` -- two different mechanisms that
  look deceptively similar
- dict comprehensions (`{key: value for ...}`) and set comprehensions
  (`{value for ...}`, with automatic deduplication)
- a nested comprehension with two `for` clauses, read left to right like
  nested loops, for flattening a 2D structure
- generator expressions (`(...)` instead of `[...]`): lazy, one-value-
  at-a-time evaluation that never materializes a full list
- comprehension variable scoping: the loop variable stays private to the
  comprehension and does not leak into the surrounding code, unlike a
  plain `for` loop's variable
- using `zip()` inside a comprehension to walk two sequences together

## How it works

The launcher shows you ten short Python programs, one at a time. Read the
code, predict exactly what it prints (entering each line separately if
the output has more than one line), and type your prediction. A correct
guess shows a short explanation and moves you on; a wrong guess shows the
actual output and, for many wrong answers, an explanation of the specific
misconception behind that particular guess. Every snippet actually runs
on your own Python interpreter -- nothing here is scripted or faked.

## Getting started

```bash
python3 launch.py
```

## You will know you are done when...

You have correctly predicted the output of all ten snippets and the
launcher shows you a passphrase.

## Hints

<details>
<summary>Hint 1 -- unfold any comprehension into an explicit loop first</summary>

If a comprehension's output is not obvious, rewrite it by hand as a plain
`for` loop with `.append()` (or dictionary/set insertion). Every
comprehension in this activity is exactly equivalent to some explicit
loop -- the shorthand syntax is the only thing that changes.

</details>

<details>
<summary>Hint 2 -- position decides filter vs. transform</summary>

An `if` written AFTER the `for` clause is a filter (it can drop
elements). An `if`/`else` written BEFORE the `for` clause is an
expression (it keeps every element, choosing a value for each one). The
word "if" alone tells you nothing -- its position does.

</details>

<details>
<summary>Hint 3 -- two `for` clauses read left to right, outer first</summary>

`[x for a in outer for x in a]` nests exactly like
`for a in outer: for x in a: ...` -- the FIRST `for` clause you read is
the OUTERMOST loop.

</details>

## Going further

- Rewrite the nested-grid-flattening snippet so it produces column-major
  order instead of row-major order (hint: look up `zip(*grid)`). Compare
  the two outputs.
- Build a generator expression over a very large `range` (say,
  `range(10_000_000)`) and compare how long it takes to create versus how
  long the equivalent list comprehension takes to create, using
  `time.perf_counter()`. What does that tell you about when each is the
  right tool?
- Write a dict comprehension with a filtering `if` AND a transforming
  if/else expression in the same comprehension. Predict its output before
  running it.
