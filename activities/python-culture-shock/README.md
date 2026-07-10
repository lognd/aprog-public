# Activity: Python Culture Shock

You already know how to program -- you have written real C++ with containers,
classes, templates, and exceptions. This activity is not about learning
programming from scratch; it is about un-learning a handful of assumptions
C++ trained into you that Python quietly breaks. Nine tiny programs, each
one or two lines, each with an output that will surprise you the first time
-- and each one teaching a rule you will rely on for the rest of the course.

## Concepts covered

- `/` (true division, always returns a float) vs. `//` (floor division, the
  C++-like truncating operator) -- Python splits what C++'s `int / int`
  does into two separate operators
- Python's `int` has no fixed width and never overflows
  (`pyobject-autopsy` shows the C-level reason: `PyLongObject`'s
  variable-length `ob_digit` array)
- names are labels bound to objects, not typed storage slots -- a name can
  be rebound to any type at any time
- assignment (`b = a`) shares one object between two names, closer to
  copying a C++ pointer than to copying a `std::vector`
- `is` (identity) vs. `==` (value equality) -- two different questions
- list slicing always copies, unlike a C++ `std::span` or pointer-offset view
- negative indexing (`a[-1]`), which has no `std::vector::operator[]`
  equivalent at all
- Python evaluates the whole right-hand side of an assignment before doing
  any of it, which is what makes `a, b = b, a` swap safely

## How it works

The launcher shows you nine short Python programs, one at a time. For each
one, read the code, predict exactly what it prints, and type your
prediction. If a program's output has more than one line, you will be asked
to enter each line separately. Get it right and you move on (with a short
explanation of why); get it wrong and you will see the actual output plus,
often, an explanation of the specific misconception behind that particular
wrong guess. Type the exact actual output to continue.

Every snippet in this activity is run with your own Python interpreter --
the same one you set up in the env-setup activities -- so what you see is
not scripted output, it is Python actually executing.

## Getting started

```bash
python3 launch.py
```

## You will know you are done when...

You have correctly predicted the output of all nine snippets and the
launcher shows you a passphrase.

## Hints

<details>
<summary>Hint 1 -- run the code yourself first</summary>

Nothing in this activity is a trick question with a "gotcha" answer that
contradicts the actual language rules. If you are unsure, copy the snippet
into a file and run `python3 that_file.py` yourself before typing a
prediction -- reading the *real* output and understanding *why* it is that
way is the actual point of the activity, not guessing correctly on the
first try.

</details>

<details>
<summary>Hint 2 -- watch for "copy" vs. "same object" language</summary>

Several snippets hinge on whether an operation makes a brand-new,
independent object or just hands out a second name for an *existing* one.
When you're stuck, ask yourself: "did this line build something new, or
did it just create another way to refer to something that already
existed?"

</details>

## Going further

- Predict, then check: what does `a[1:3]` print if `a` is a *string*
  instead of a list? Does slicing a string still copy?
- `2**100` never overflows -- but is it still fast? Time `2**100` vs.
  `2**10` in a loop of a million iterations each (`import time`) and see
  whether Python's unbounded integers cost anything when the numbers are
  small.
- Try `a is b` on two *small* integers created separately (e.g. `a = 200;
  b = 200; print(a is b)`) versus two *large* ones (`a = 200000; b =
  200000`). The result may differ -- and it is intentionally left out of
  this activity, because it depends on an implementation detail of CPython
  that is not part of the language guarantee. Read up on "small integer
  caching" to see why relying on `is` for number comparison is a mistake
  even when it happens to work.
