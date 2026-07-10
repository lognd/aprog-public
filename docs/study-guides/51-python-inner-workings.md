# Study Guide 51: Python Inner-Workings (__dict__, __mro__, etc.)

This module exposes the real machinery behind every Python attribute
access: `__dict__` as the literal dictionary backing an object's or
class's own attributes, `__mro__` as the precomputed multi-parent search
order, bound methods, monkey-patching, and `__slots__` as an opt-out of
dictionary-backed storage.

## Know before you start

- Instance vs. class attribute shadowing, and attribute-lookup-checks-
  instance-first [assumed: row 50 -- Python Classes]
- Bound methods and calling through an instance vs. through the class
  [assumed: row 50 -- Python Classes]
- Multiple inheritance and the diamond problem in general terms [assumed:
  row 22 -- Inheritance]

## Taught here

Concept: `__dict__` and attribute lookup
- Know every attribute access (`self.name`, `Counter.count`) is,
  underneath, a lookup into a plain dictionary -- `__dict__` is the real
  dictionary backing an object's (or a class's) own attributes, and
  `vars(obj)` is a shortcut for `obj.__dict__`.
- Know attribute lookup order: an object's own `__dict__` is checked
  first; only if the attribute is not found there does lookup fall back
  to the class's `__dict__` -- instance attributes shadow class
  attributes of the same name, and deleting the instance attribute
  un-shadows the class one again.
- Know assignment through an instance (`obj.x = ...`) always writes to
  the instance's own dictionary, never the class's, even when a class
  attribute of the same name already exists.
- Know lookup is never cached at object-construction time -- it happens
  fresh on every single attribute access, which is exactly why
  monkey-patching (reassigning a class's method from outside the class
  body) is immediately visible to every existing instance of that class.

Concept: method resolution order (MRO)
- Know `__mro__` is the exact, precomputed, fully-ordered list of classes
  Python searches through for a class hierarchy, including multi-parent
  ("diamond") shapes.
- Know a class always appears before its own bases in `__mro__`, and a
  shared ancestor reached through more than one path is listed only once,
  after ALL the classes that lead to it.
- Know method resolution walks `__mro__` in order and stops at the first
  class defining the needed name -- "leftmost base wins" when two
  unrelated bases define the same method name.
- Know `super()` means "whichever class comes next after the CURRENTLY
  RUNNING class in the `__mro__` of the object the whole call chain
  started from" -- not simply "my direct parent class," a distinction
  that only shows up once more than one base class is involved.

Concept: dynamic access and bound methods
- Know `getattr`, `setattr`, and `hasattr` perform attribute access with
  the attribute name as a runtime string, instead of literal `.` syntax.
- Know a method accessed through an instance (`obj.method`) is a BOUND
  method: a small wrapper remembering both the underlying function and
  the specific instance, which is exactly why calling it needs no
  explicit `self` argument -- accessed through the class instead
  (`ClassName.method`), it is the plain, unbound function object.
- Know `__slots__` is a class-level opt-out of per-instance `__dict__`
  storage, in exchange for a fixed, declared set of attribute names --
  trading flexibility for lower per-instance memory overhead and refusing
  any attribute not in the declared set.

Concept: CPython object internals
- Know every Python value is, under the hood, a C struct allocated on the
  heap -- `PyObject { Py_ssize_t ob_refcnt; PyTypeObject *ob_type; }` is the
  literal (simplified) struct every object starts with, from CPython's
  `Include/object.h`.
- Know `ob_refcnt` and `ob_type` are the two fields every PyObject carries:
  a reference count, and a pointer to the object's type.
- Know reference counting is the exact same shared-ownership mechanism as
  `std::shared_ptr`: incremented on each new reference, decremented on each
  lost reference, the object freed the instant the count hits zero --
  automated, by the interpreter, on every object, with no opt-in required.
- Know reference counting alone cannot free a reference cycle (two objects
  holding references to each other), and that CPython's separate cyclic
  garbage collector (the `gc` module) is what reclaims cycles refcounting
  cannot.
- Know `PyVarObject` adds one field, `ob_size`, for types whose size varies
  per instance (`list`, `tuple`, `str`) -- fixed-size types (`float`,
  `bool`) use plain `PyObject` with no `ob_size` at all.
- Know `PyListObject`'s `ob_item` is a `PyObject**` -- an array of
  POINTERS to the actual elements, not the elements themselves -- which is
  the literal C-level mechanism behind two names sharing (and mutating
  through) the same list.
- Know rebinding a name (`x = 5; x = "five"`) is a pointer swap plus
  refcount adjustments, never a conversion of the old value into the new
  one.
- Know `id()` returns a CPython implementation detail (the object's memory
  address), not a language-level guarantee, and that `sys.getrefcount()`
  should never be asserted against an exact number, since the call itself
  takes a temporary reference to its argument.

## Study checklist

- [ ] Trace an attribute read through instance __dict__ then class
      __dict__, predicting the result.
- [ ] Write out a diamond hierarchy's __mro__ by hand, left to right, each
      class once.
- [ ] Explain what super() actually consults, using a diamond example.
- [ ] Explain why monkey-patching a class affects instances created
      before the patch.
- [ ] Distinguish a bound method from a plain function object.
- [ ] Explain what __slots__ trades away and what it gains.
- [ ] Draw the PyObject fields every value carries, and explain what each
      one is for.
- [ ] Trace ob_refcnt through a small assignment/del sequence by hand.
- [ ] Explain why a reference cycle defeats plain refcounting, and what
      catches it instead.
- [ ] Explain why `ob_item[0]` on a list holds a pointer, not a value, and
      how that produces the aliasing behavior from python-culture-shock.

## Practiced in

`dunder-dungeon`, `lookup-court`, `pyobject-autopsy`
