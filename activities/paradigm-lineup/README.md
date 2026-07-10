# Activity: Paradigm Lineup

Every program tells the computer what to do, but there is more than one
style in which that instruction can be phrased. A **programming paradigm**
is exactly that: a style of structuring programs, defined by what the code
treats as its basic building block. Some code reads like a recipe: do this,
then this, then this. Some reads like a blueprint of interacting objects.
Some reads like mathematics: combine small transformations into bigger
ones. And some barely reads like instructions at all -- it just describes
the result and lets an engine figure out the rest.

You will read short code snippets -- C++ where possible, plus a few
clearly-labeled Python, SQL, and Prolog-style examples you only need to
read, never write -- and identify which paradigm each one exemplifies.
(SQL, short for Structured Query Language, is the standard language for
asking databases questions; Prolog is a language where programs are written
as logical facts and rules. You need zero prior experience with either --
each snippet is explained as it appears.)

---

## Background

The four paradigms you will see here are the big ones.

### Imperative -- mutation plus sequencing

Imperative code is a sequence of statements that change program state one
step at a time. ("State" just means the current values of all the
program's variables at a given moment.) The two defining traits are
**mutation** (variables get reassigned -- their stored value is overwritten
with a new one) and **sequencing** (the order of statements matters
completely).

```cpp
int total = 0;
for (int i = 0; i < n; i++) {
    total += arr[i];
}
```

`total` starts at 0 and is overwritten on every iteration. Swap two
statements and the program breaks. This is the style you have written all
semester -- loops, counters, accumulators, in-place updates. It maps
directly onto what the CPU actually does, which is why C (and the imperative
core of C++) is so close to the machine.

### Object-oriented -- state encapsulated with behavior

Object-oriented code bundles data together with the operations allowed to
touch that data, and hides the data itself from the outside world.

```cpp
class BankAccount {
public:
    void deposit(double amt) { balance_ += amt; }
    double balance() const { return balance_; }
private:
    double balance_ = 0.0;
};
```

The mutation is still there (`balance_ += amt`), but it is controlled: the
`private` keyword makes `balance_` unreachable from outside the class, so
the only way anyone can change the balance is by sending the object a
message -- calling `deposit()`. The defining trait is this pairing of state
with the behavior that guards it. Larger object-oriented designs add
**inheritance** (defining a new class as an extension of an existing one)
and **virtual dispatch** (letting different kinds of objects respond to the
same method call each in their own way) -- both of which you will meet
properly in later activities.

### Functional -- pure functions plus composition

Functional code avoids mutation entirely. Instead of changing existing
values, it builds new ones by composing small transformations.

```python
# Python
doubled = list(map(lambda x: x * 2, numbers))
evens = list(filter(lambda x: x % 2 == 0, doubled))
```

`numbers` is never touched. Each step takes an input and returns a fresh
output. In this Python snippet, `map` applies a small function to every
element and returns the results; `filter` keeps only the elements that pass
a test; and `lambda x: x * 2` is just a tiny unnamed function written
inline ("given x, produce x * 2"). A function that always returns the same
output for the same input, and changes nothing outside itself (no **side
effects**), is called a **pure** function. Pure functions are easy to test,
safe to run in parallel, and easy to reason about in isolation, because
nothing about them depends on hidden context. The defining trait of the
functional style is pure functions plus **composition** -- feeding one
function's output into the next to build bigger transformations from
smaller ones.

### Declarative -- describe what, not how

Declarative code states the desired result and leaves the procedure to an
engine.

```sql
SELECT name, age FROM students WHERE age >= 18 ORDER BY name;
```

This SQL query asks a database for the name and age of every student who is
at least 18, sorted by name. There is no loop here, no counter, no
algorithm. The query says WHAT rows are wanted; the database's **query
optimizer** -- the component that picks the fastest way to actually fetch
the data -- decides HOW to scan, filter, and sort. Logic languages like
Prolog take the same idea further: you state facts ("alice is bob's
parent") and rules ("a grandparent is a parent's parent"), and the engine
searches for answers on its own. The defining trait is
describe-what-not-how.

### Paradigms are styles, not cages

Real languages mix paradigms freely. C++ in particular supports imperative
loops, full object-oriented class design, and (since the C++11 version of
the language standard) a genuinely functional style, using lambdas
(C++'s inline unnamed functions) together with the `<algorithm>` library of
ready-made operations. Even a single line can carry a paradigm's flavor:
`std::sort(arr.begin(), arr.end())` is declarative in spirit -- it names
the result you want (this range, sorted) and hides the entire algorithm.
Learning to recognize the style of a piece of code, independent of the
language it happens to be written in, is the actual skill this activity
trains.

---

## Concepts covered

- Imperative programming: mutation plus explicit sequencing of statements
- Object-oriented programming: encapsulating state with the behavior that
  guards it; virtual dispatch
- Functional programming: pure functions, no mutation, building results by
  composition (`map`, `filter`, `reduce`)
- Declarative programming: describing the desired result (SQL, Prolog) and
  letting an engine choose the procedure
- Multi-paradigm reality: how C++ supports imperative, object-oriented, and
  functional styles at once

---

## How it works

The launcher shows you nine questions. Each one displays a short code
snippet and asks which paradigm it exemplifies. Every prompt ends with an
explicit option list -- for example:

```
Type exactly one of: imperative / object-oriented / functional / declarative
```

Type your answer exactly as one of the listed options. A wrong answer gets
targeted feedback explaining which defining trait you missed, and you can
try again as many times as you need. A correct answer unlocks a full
explanation of the trait that gives the snippet away. Answer all nine
correctly and the launcher decrypts and prints the passphrase.

You do not need to write or run any of the snippet code. The Python, SQL,
and Prolog-style snippets are there to be read, not executed -- each is
labeled with its language.

---

## Getting started

```bash
python3 launch.py
```

Read each snippet slowly before answering. Ask yourself, in order: Is a
variable being mutated in a sequence of steps? Is state bundled inside a
class and guarded by methods? Are pure transformations being composed? Or
does the code only describe a result and leave the procedure to an engine?

---

## You will know you are done when...

The launcher prints `All correct.` followed by the passphrase between two
horizontal rules. Record the passphrase -- it is your proof of completion.

---

## Hints

<details>
<summary>Hint 1 -- one question to ask of every snippet</summary>

Find the answer to "where does the result come from?" If the result
accumulates in a variable that gets reassigned, you are looking at
imperative code. If it comes back from a method call on an object that
guards its own fields, that is object-oriented. If it is built by feeding
one transformation's output into the next, that is functional. If the code
never says how the result is computed at all, that is declarative.

</details>

<details>
<summary>Hint 2 -- mutation inside a class is not plain imperative</summary>

Several snippets contain mutation. The question is always what the snippet's
notable, defining structure is. A `+=` buried inside a private-field class
with controlled access is demonstrating encapsulation of state -- the
object-oriented trait -- even though the `+=` itself is a mutation.

</details>

<details>
<summary>Hint 3 -- functional vs declarative</summary>

Both avoid step-by-step mutation, so they are easy to confuse. The tell:
functional code still shows you explicit functions being composed over data
(`map`, `filter`, lambdas). Declarative code shows no functions and no data
flow at all -- just a description of the result (a SQL result set, a Prolog
rule) that an engine satisfies however it likes.

</details>

---

## Going further

- Rewrite the imperative sum-of-array snippet using `std::accumulate` from
  `<numeric>`. Which paradigm does your one-line version lean toward, and
  what did you have to give up (if anything)?
- Look up `std::ranges` (C++20) and rewrite the Python map/filter pipeline
  as a C++ ranges pipeline with `std::views::transform` and
  `std::views::filter`. Compare the readability.
- Find a real SQL query in any project or tutorial and write out, in
  pseudocode, the imperative loop the database engine might actually run to
  satisfy it. How many decisions did the optimizer make that the query never
  mentioned?
- Prolog is free to try online (SWI-Prolog has a browser version). Enter the
  `parent`/`grandparent` facts from this activity and query
  `grandparent(alice, Z).` -- watch the engine find the answer with no
  algorithm written by you.
