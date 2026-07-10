# Activity: Self/Cls Court

method-trinity showed you the three method kinds by running code. Self/Cls
Court puts the reasoning on trial: given a job description (an alternate
constructor, a pure stateless helper, per-object behavior), which method
kind actually fits, and why do the other two fail? It also settles two
questions that trip up C++ programmers specifically: what `self` actually
is, mechanically, and whether Python has anything resembling C++'s
`private` keyword (it does not -- only a naming convention and a
best-effort mangling trick).

## Concepts covered

- choosing between instance methods, classmethods, and staticmethods
  based on what a method's job actually requires
- what `self` is, mechanically: an ordinary parameter, not a keyword,
  filled in automatically by `instance.method(...)` syntax
- what happens calling an instance method through the class with no
  instance supplied at all
- Python's lack of enforced private members: the `_x` convention versus
  the `__x` name-mangling mechanism, and what `__x` actually gets renamed
  to
- what a classmethod can and cannot see (the class, never a specific
  instance's data)

## How it works

The launcher asks eight questions, one at a time, several with a short
code snippet and all with a hint. Type your answer in your own words (or
as the exact phrase, value, or line the question calls for) and press
Enter. A correct answer shows a full explanation and moves you to the
next question; a wrong answer -- if it matches a known misconception --
shows why that specific answer is wrong, and otherwise asks you to reread
the question and try again.

## Getting started

```bash
python3 launch.py
```

## You will know you are done when...

You have correctly answered all eight questions and the launcher shows
you a passphrase.

## Hints

<details>
<summary>Hint 1 -- ask what information the method needs, not what it currently uses</summary>

A method belongs to whichever kind matches what its JOB genuinely
requires -- one specific object's data, the class itself, or neither --
not just whichever parameters happen to appear unused in a rough draft.

</details>

<details>
<summary>Hint 2 -- accessing a method through the class never auto-binds anything</summary>

`instance.method()` auto-fills `self`. `ClassName.method()` does not --
it gives back the plain, unbound function, exactly as if you had written
the function outside the class entirely. Whatever it needs, you must
supply by hand.

</details>

<details>
<summary>Hint 3 -- name mangling only touches double-leading-underscore names</summary>

A single leading underscore (`_x`) is never mangled -- it is pure
convention. Name mangling only applies to names starting with two
underscores and ending with at most one (`__x`, but not `__x__`).

</details>

## Going further

- Write a class with a classmethod that intentionally tries to read an
  instance attribute without being passed an instance, and observe the
  exact error Python raises.
- Look up `__init_subclass__`. It is a special classmethod-like hook that
  runs automatically whenever a class is subclassed -- how does it relate
  to the "cls sees the class, not any instance" rule from this activity?
- Define a class with both `_internal` and `__mangled` attributes, then
  use `vars(instance)` to see exactly how each one is actually stored.
