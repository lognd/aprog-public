# Study Guide 50: Python Classes (instance, class, static)

This module distinguishes Python's three method kinds -- instance methods
(`self`), classmethods (`cls`, subclass-correct alternate constructors),
and staticmethods (neither) -- plus class vs. instance attribute
shadowing and `@property` getters/setters. `temperature-lab` combines all
of it into one validated class.

## Know before you start

- `__init__`/`self` as constructor/this, and class vs. static members
  [assumed: row 46 -- Python Syntax (including OOP)]
- Dynamic dispatch and no `virtual` keyword needed [assumed: row 46 --
  Python Syntax (including OOP)]
- `__eq__`'s default identity fallback and dunder methods generally
  [assumed: row 46 -- Python Syntax (including OOP)]
- Decorators as functions wrapping functions [assumed: row 49 -- Python
  Decorators]

## Taught here

Concept: the three method kinds
- Know instance methods take `self` (the specific object called on) as
  their automatic first parameter, and read/write that one object's data.
- Know classmethods take `cls` (the class itself, decorated with
  `@classmethod`) instead of `self`, most commonly used for alternate
  constructors that must build the RIGHT class even when called through a
  subclass -- they build and return `cls(...)`, never a hardcoded class
  name.
- Know staticmethods (decorated with `@staticmethod`) take neither `self`
  nor `cls`, behaving like a plain function grouped inside the class
  purely for organization -- used when a method's job needs neither one
  specific object's data nor knowledge of which class it was called
  through.
- Be able to choose the right kind by asking what the method's job
  actually requires: one specific object's data (instance), the class
  itself to build the right type (classmethod), or neither (staticmethod).

Concept: self, mechanically, and attribute lookup
- Know `self` is an ordinary parameter, not a keyword -- it is filled in
  automatically only by `instance.method(...)` syntax; calling through
  the class instead (`ClassName.method(...)`) gives back the plain,
  unbound function with nothing auto-filled, requiring every argument
  including what would have been `self` to be supplied by hand.
- Know reading `obj.attr` checks the instance's own data first, and only
  falls back to the class if the instance has no such attribute; ASSIGNING
  `obj.attr = value` always creates or overwrites an attribute on the
  instance, never reaching into the class -- this is the exact moment an
  instance attribute starts shadowing a class attribute of the same name.
- Know Python has no enforced private members: a single leading
  underscore (`_x`) is pure naming convention, never mangled or enforced;
  a double leading underscore (`__x`, but not `__x__`) triggers name
  mangling, a best-effort rename (not true access control) meant to avoid
  accidental collisions in subclasses.

Concept: `@property`
- Know `@property` turns a method into a computed attribute accessed with
  no parentheses (`obj.name`, not `obj.name()`).
- Know `@x.setter` defines a paired setter method that runs whenever code
  writes `obj.x = value` -- it is not a plain assignment, it is a method
  call that can validate the value (e.g. raising `ValueError`) before
  storing it or rejecting it.
- Be able to build a read-only computed property (getter only, no setter)
  versus a validated read-write property (getter plus a setter that
  enforces an invariant).
- Know a class attribute defined directly in the class body (not inside
  `__init__`) is shared by the class itself and every instance/subclass
  that does not override it.

## Study checklist

- [ ] Given a method's job description, pick instance/classmethod/
      staticmethod and justify it.
- [ ] Explain what self actually is and what ClassName.method() gives you
      without an instance.
- [ ] Predict when an instance attribute assignment starts shadowing a
      class attribute.
- [ ] Explain the difference between _x convention and __x name mangling.
- [ ] Write a validated @property with a raising setter.
- [ ] Explain why an alternate constructor must return cls(...), not a
      hardcoded class name, to stay correct for subclasses.

## Practiced in

`method-trinity`, `self-cls-court`, `temperature-lab`
