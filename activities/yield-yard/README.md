# Activity: Yield Yard

C++ has no real equivalent to this until C++20 coroutines (`co_yield`),
and even there it is an advanced, rarely-touched corner of the language.
A Python generator function -- any function with a `yield` anywhere in
its body -- pauses and resumes on demand, remembering exactly where it
left off between calls, without you writing any of the state-machine
bookkeeping that would take by hand. This activity proves that pause-
and-resume behavior directly, by watching interleaved `print()` output:
you will see a generator function get called without running a single
line of its body, watch execution genuinely suspend between `next()`
calls, watch a generator run dry and raise `StopIteration`, and watch a
lazy generator expression defer its side effects until the moment
something actually asks it for a value.

## Concepts covered

- Calling a generator function returns a paused generator object without
  running any of the body
- `yield` suspends execution mid-function; the next `next()` call resumes
  exactly where it left off
- `StopIteration` as the signal a generator has nothing left to produce,
  and how a `for` loop catches it automatically
- Laziness: a generator expression's side effects happen on consumption,
  not on creation
- Exhaustion: a generator object cannot be rewound or reused once fully
  consumed
- Chaining (piping) one generator into another, and consuming an
  infinite generator safely with a bounded loop

## How it works

The launcher runs nine short Python programs on your own interpreter and
shows you each one's source code. Predict exactly what it prints
(entering each line separately when the output has more than one line),
then type your prediction. A correct guess shows a short explanation and
moves you on; a wrong guess shows the actual output and, for many wrong
answers, an explanation of the specific misconception behind that guess.

## Getting started

```bash
python3 launch.py
```

## You will know you are done when...

You have correctly predicted the output of all nine snippets and the
launcher shows you a passphrase.

## Hints

<details>
<summary>Hint 1 -- calling a generator function does nothing yet</summary>

`gen = some_generator_function()` never runs a single line of the
body -- it just builds a paused generator object. The body only starts
running on the first `next()` call (or the first iteration of a `for`
loop over it).

</details>

<details>
<summary>Hint 2 -- laziness means "on demand," not "eventually"</summary>

A generator expression's side effects (like a `print` inside the thing
being generated) happen exactly when a value is pulled out of it, one at
a time -- never earlier, and never all at once up front.

</details>

<details>
<summary>Hint 3 -- exhaustion is permanent for that one object</summary>

Once a generator object has been fully consumed, it stays empty forever.
Getting a fresh sequence of values means calling the generator function
again to build a brand-new generator object, not reusing the old one.

</details>

## Going further

- Write your own infinite generator (like `naturals()` in this activity)
  and pipe it through two more generator expressions before consuming it
  with a bounded loop. Does laziness still hold at every stage?
- Look up Python's `itertools.islice` and rewrite this activity's `take`
  helper using it. What is the qualitative difference between hand-
  rolling `take` and reaching for the standard library version?
- Read about C++20 `co_yield` and coroutines. What has to happen at the
  language level in C++ for a function to pause and resume the way every
  Python generator does automatically?
