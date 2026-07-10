# Activity: Pythonic or Not

Every snippet in this activity runs correctly. That is the point: coming
from C++, your instincts will produce Python code that *works* but does not
read the way an experienced Python programmer would write it. This activity
is eight small pieces of code, each written the way a C++ habit naturally
produces it, asking you to name whether it is idiomatic Python and, when it
is not, what the idiomatic replacement looks like.

## Concepts covered

- direct iteration (`for item in v`) vs. index-based iteration
  (`for i in range(len(v))`)
- `enumerate()` for the case where you genuinely need both the index and
  the value
- `sum()` vs. a hand-written accumulator loop
- `str.join()` vs. repeated `+=` string concatenation, and *why* it
  matters (Python strings are immutable, unlike a mutable `std::string`)
- Python has no `private`/`protected`/`public` -- a leading underscore is
  only a naming convention, not an enforced restriction
- `isinstance()` vs. duck typing, and the honest, non-absolute answer for
  when each is the right call
- truthiness vs. explicit comparison (`if flag:` vs. `if flag == True:`,
  `if not names:` vs. `if len(names) == 0:`)

## How it works

The launcher shows you a snippet of working Python code and a question
asking you to characterize it: is this idiomatic, and if not, what should
replace it? Type your answer in the expected phrasing; a wrong guess shows
an explanation of the specific misconception behind that guess and lets you
try again. A correct answer shows the full reasoning -- including, for the
`isinstance()` question, a genuinely nuanced answer rather than a blanket
rule -- before moving to the next question.

## Getting started

```bash
python3 launch.py
```

## You will know you are done when...

You have correctly answered all eight questions and the launcher shows you
a passphrase.

## Hints

<details>
<summary>Hint 1 -- "it works" is not the same question as "is it idiomatic"</summary>

None of these snippets are broken. If you find yourself trying to spot a
bug, you are answering the wrong question -- look instead for a place where
Python already gives you a more direct, built-in way to say the same thing.

</details>

<details>
<summary>Hint 2 -- read the explanation even when you got it right</summary>

The `isinstance()` vs. duck typing question in particular does not have a
one-line rule that always applies. Read its explanation carefully even
after answering correctly -- it will come up again once this course starts
using duck typing more heavily.

</details>

## Going further

- Time `str.join()` against repeated `+=` concatenation on a list of
  10,000 short strings (`import time`). How much does the difference
  actually matter at that size? At 100 strings?
- Look up Python's `@property` decorator. Rewrite the `Point` class from
  the getter/setter question so that `point.x` still works as a plain
  attribute, but assigning a negative value raises a `ValueError`.
- Find a real, small open-source Python project on GitHub and search its
  code for `range(len(`. Is it ever justified? What is different about the
  cases where it appears versus the cases in this activity?
