# Activity: Dunder Dungeon

Every attribute you have ever read or written in Python -- `self.name`,
`Counter.count`, a decorator's `fn` -- is, underneath, a lookup into a
plain dictionary. This activity pulls that mechanism out into the open:
you will watch an object's own attribute dictionary (its `__dict__`)
start out empty and grow one key at a time, see where a class's methods
actually live, and watch an instance attribute "shadow" (hide) a class
attribute of the same name, then stop shadowing it the moment it is
deleted. From there it moves on to `__mro__` -- the exact, fully-ordered
list of classes Python searches through for a multi-parent ("diamond")
class hierarchy -- dynamic attribute access with `getattr`/`setattr`/
`hasattr`, the fact that a method is just a function object wrapped a
particular way, and `__slots__`, a class-level opt-out of the flexible
dictionary-backed storage every other snippet in this activity relies on.

## Concepts covered

- `__dict__`: the real dictionary backing an object's (or a class's) own
  attributes, and how it grows as attributes are assigned
- attribute lookup order: an object's own `__dict__` first, then the
  class's `__dict__`, with instance attributes shadowing class attributes
  of the same name
- `__mro__` (Method Resolution Order): the exact, precomputed search
  order Python uses for a class hierarchy, including a multi-parent
  ("diamond") shape
- dynamic attribute access with `getattr`, `setattr`, and `hasattr`,
  where the attribute name is a runtime string instead of literal syntax
- a method accessed through an instance versus through the class
  (bound method vs. plain function object)
- `vars(obj)` as a shortcut for `obj.__dict__`
- `__slots__`: opting a class out of per-instance `__dict__` storage
  entirely, in exchange for a fixed, declared set of attribute names

## How it works

The launcher shows you eight short Python programs, one at a time. Read
the code, predict exactly what it prints (entering each line separately
if the output has more than one line), and type your prediction. A
correct guess shows a short explanation and moves you on; a wrong guess
shows the actual output and, for many wrong answers, an explanation of
the specific misconception behind that particular guess. Every snippet
actually runs on your own Python interpreter -- nothing here is scripted
or faked.

## Getting started

```bash
python3 launch.py
```

## You will know you are done when...

You have correctly predicted the output of all eight snippets and the
launcher shows you a passphrase.

## Hints

<details>
<summary>Hint 1 -- when in doubt, ask "whose __dict__?"</summary>

Almost every snippet in this activity comes down to one question: is the
attribute you are looking at stored in the INSTANCE's own dictionary, or
the CLASS's dictionary? Assignment through an instance (`obj.x = ...`)
always writes to the instance's own dictionary, never the class's.

</details>

<details>
<summary>Hint 2 -- __mro__ reads left to right, and each class appears once</summary>

For the diamond-hierarchy snippet, remember two rules: a class always
appears before its own bases in `__mro__`, and a shared ancestor (reached
through more than one path) is only listed once, after ALL the classes
that lead to it.

</details>

<details>
<summary>Hint 3 -- a bound method remembers two things, not one</summary>

Accessing a method through an instance (`obj.method`) does not give you
the raw function -- it gives you a small wrapper that remembers both the
underlying function AND the specific instance, which is exactly why
calling it needs no explicit `self` argument.

</details>

## Going further

- Write a class with `__slots__` that also tries to define a class
  attribute with the same name as one of its slots. What happens, and
  why does that specific combination raise an error at class-definition
  time rather than at instance-creation time?
- Use `Class.__dict__` (not an instance's) on a class with a
  `@classmethod` and a `@staticmethod` defined on it. What do you see for
  each -- are they stored as plain function objects, or as something
  else?
- Predict, then verify, what `A.__mro__` looks like for a hierarchy where
  `class A(B, C, D):` has three direct bases instead of two. Does the
  "left to right" rule still explain the order?
