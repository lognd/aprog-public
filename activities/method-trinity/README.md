# Activity: Method Trinity

Every method you have written in Python so far has probably taken `self`
as its first parameter, without much thought about why. Python actually
distinguishes three different kinds of method -- instance methods (which
receive `self`, the specific object called on), classmethods (which
receive `cls`, the class itself, letting them build the RIGHT class even
for subclasses), and staticmethods (which receive neither, and behave
like a plain function grouped inside a class for organization). Seven
short programs walk through all three, plus two related mechanics: how a
class-level attribute is shared until an instance attribute of the same
name shadows it, and how `@property` turns a method into a computed
attribute you access without parentheses.

## Concepts covered

- instance methods and the automatic `self` binding
- classmethods, `cls`, and alternate constructors that stay correct for
  subclasses
- staticmethods, and when a method needs neither `self` nor `cls`
- class attributes versus instance attributes, and the exact moment an
  instance attribute starts shadowing a class attribute of the same name
- `@property` getters (computed attributes, accessed with no parentheses)
  and `@x.setter` methods that can validate an assignment before it takes
  effect
- calling an instance method explicitly through the class
  (`ClassName.method(instance)`), the C++ pointer-to-member-function echo

## How it works

The launcher shows you seven short Python programs, one at a time. Read
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

You have correctly predicted the output of all seven snippets and the
launcher shows you a passphrase.

## Hints

<details>
<summary>Hint 1 -- ask what the method actually needs</summary>

For the classmethod and staticmethod snippets, ask: does this method's
body need to read or write ONE SPECIFIC object's data (instance method)?
Does it need to know which class it was called through, so it can build
the right one (classmethod)? Or does it need neither (staticmethod)?

</details>

<details>
<summary>Hint 2 -- attribute lookup checks the instance first, then the class</summary>

Reading `obj.attr` first checks whether `obj` itself has an attribute
named `attr` (in its own instance data). Only if it does not is the
class checked. ASSIGNING `obj.attr = value` always creates or overwrites
an attribute on the instance -- it never reaches into the class.

</details>

<details>
<summary>Hint 3 -- a property setter runs like any other method call</summary>

`obj.name = value` on a property-decorated attribute is not a plain
assignment -- it calls the setter method with `value` as an argument.
Trace through the setter's body exactly as you would trace through a call
to any other method.

</details>

## Going further

- Add a second alternate constructor to a class of your own design, using
  `@classmethod`, and confirm it still builds the right type when called
  through a subclass.
- Write a property whose getter computes a value from two other stored
  attributes (like `area` from `radius`), then add caching: only
  recompute the value if one of the underlying attributes has changed
  since the last read. What would you need to track to make that work?
- Look up `__slots__`. How does it interact with instance attributes, and
  why might a class use it instead of the default per-instance `__dict__`?
